"""SP-06.3 credential repository tests."""

from dataclasses import FrozenInstanceError

import pytest

from elevator_access_sim import CredentialRepository
from elevator_access_sim.models import CredentialDataError, CredentialKey, CredentialRecord, DuplicateCredentialError, RepositoryLookup, StateInvariantError


def rec(facility: object = 1, credential: object = 100, enabled: object = True, mask: object = 65535, label: object = None) -> CredentialRecord:
    return CredentialRecord(facility, credential, enabled, mask, label)  # type: ignore[arg-type]


def test_empty_multiple_order_length_known_unknown_and_immutability() -> None:
    assert len(CredentialRepository.from_records([])) == 0
    source = [rec(), rec(2, 99, label="two")]
    repository = CredentialRepository.from_records(source)
    assert len(repository) == 2 and repository.records() == tuple(source)
    assert repository.lookup(CredentialKey(1, 100)) == RepositoryLookup(source[0])
    assert repository.lookup(CredentialKey(2, 99)) == RepositoryLookup(source[1])
    assert repository.lookup(CredentialKey(3, 98)) == RepositoryLookup(None)
    observed = repository.records() + (rec(3, 98),)
    assert len(observed) == 3 and len(repository) == 2 and source == [rec(), rec(2, 99, label="two")]
    with pytest.raises(FrozenInstanceError): repository.records()[0].enabled = False  # type: ignore[misc]


def test_tst_crd_001_colliding_sums_are_distinct_and_duplicates_fail() -> None:
    assert len(CredentialRepository.from_records([rec(), rec(2, 99)])) == 2
    with pytest.raises(DuplicateCredentialError): CredentialRepository.from_records([rec(), rec(label="again")])


@pytest.mark.parametrize("value", [rec(-1), rec(256), rec(True), rec(credential=-1), rec(credential=65536), rec(credential=False), rec(enabled=1), rec(mask=-1), rec(mask=65536), rec(mask=True), rec(label=""), rec(label="  "), rec(label=1), rec(label="\ud800")])
def test_invalid_record_fields_at_programmatic_boundary(value: CredentialRecord) -> None:
    with pytest.raises(CredentialDataError): CredentialRepository.from_records([value])


@pytest.mark.parametrize("position", [0, 1, 2])
def test_tst_crd_005_invalid_beginning_middle_end_does_not_change_existing(position: int) -> None:
    existing = CredentialRepository.from_records([rec()])
    values = [rec(2, 2), rec(3, 3), rec(4, 4)]
    values[position] = rec(9, 9, mask=-1)
    with pytest.raises(CredentialDataError): CredentialRepository.from_records(values)
    assert existing.records() == (rec(),)


@pytest.mark.parametrize("value", ["x", b"x", {"x": rec()}, {rec()}, (item for item in [rec()]), iter([rec()]), object()])
def test_malformed_sequence_inputs(value: object) -> None:
    with pytest.raises(CredentialDataError): CredentialRepository.from_records(value)  # type: ignore[arg-type]


def test_nonrecord_member_and_lookup_misuse() -> None:
    with pytest.raises(CredentialDataError): CredentialRepository.from_records([rec(), object()])  # type: ignore[list-item]
    repository = CredentialRepository.from_records([rec()])
    for key in (None, (1, 100), CredentialKey(True, 100), CredentialKey(-1, 100), CredentialKey(1, False), CredentialKey(1, 65536)):
        with pytest.raises(StateInvariantError): repository.lookup(key)  # type: ignore[arg-type]
