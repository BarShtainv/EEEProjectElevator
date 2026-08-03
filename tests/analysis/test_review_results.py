"""Independent SP-07.4 review tests."""
from __future__ import annotations
import ast, csv, hashlib, importlib.util, io, json, os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import pytest

ROOT=Path(__file__).resolve().parents[2]; SCRIPT=ROOT/"analysis/review_results.py"
@pytest.fixture(scope="module")
def review():
    spec=importlib.util.spec_from_file_location("sp074_review",SCRIPT); assert spec and spec.loader
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module);return module
@pytest.fixture(scope="module")
def outputs(review): return review.build_outputs()
def rows(data): return list(csv.DictReader(io.StringIO(data.decode("utf-8"))))
def destinations(review,root): return {key:root/(key+{"review_summary":".json","anomaly_register":".csv","validation_ledger":".csv","source_notes":".md"}[key]) for key in review.OUTPUT_KEYS}

def test_all_canonical_sources_manifest_and_outputs_validate(review,outputs):
    integrity=review.review_integrity(); assert integrity["source_count"]==29 and integrity["verified_hash_count"]==37 and integrity["mismatches"]==[]
    assert set(outputs)==set(review.OUTPUT_KEYS)

def test_malformed_utf8_json_duplicate_and_csv_schema_fail(review,tmp_path,monkeypatch):
    monkeypatch.setattr(review,"ROOT",tmp_path)
    (tmp_path/"bad").write_bytes(b"\xff")
    with pytest.raises(review.ReviewError,match="UTF-8"): review.read_text("bad")
    (tmp_path/"bad").write_text("{",encoding="utf-8")
    with pytest.raises(review.ReviewError,match="invalid JSON"): review.json_source("bad")
    (tmp_path/"bad").write_text('{"x":1,"x":2}',encoding="utf-8")
    with pytest.raises(review.ReviewError,match="duplicate"): review.json_source("bad")
    (tmp_path/"bad").write_text("x\n1\n",encoding="utf-8")
    with pytest.raises(review.ReviewError,match="schema"): review.csv_source("bad",("y",))

def test_substituted_source_changed_manifest_and_missing_figure_fail(review,tmp_path,monkeypatch):
    root=tmp_path/"copy"; root.mkdir()
    for source in review.SOURCES:
        target=root/source;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/source).read_bytes())
    monkeypatch.setattr(review,"ROOT",root)
    (root/review.SOURCES[0]).write_text("changed",encoding="utf-8")
    with pytest.raises(review.ReviewError,match="hash mismatch"): review.review_integrity()
    (root/review.SOURCES[0]).write_bytes((ROOT/review.SOURCES[0]).read_bytes())
    (root/"docs/figures/sp07_lookup_average_ns.svg").unlink()
    with pytest.raises(review.ReviewError): review.review_integrity()

def test_verification_requirements_inventory_exact(review):
    value=review.review_governance(); assert (value["collected"],value["passed"],value["pass_rate"])==(976,976,1.0)
    assert (value["requirements_total"],value["required_verified"],value["optional_deferred"])==(66,60,6)
    assert (value["inventory_total"],value["inventory_implemented"],value["inventory_optional_designed"])==(100,94,6)
    assert "not current" in value["snapshot_scope"]

def test_mixed_exact_rows_totals_checksums_environment(review):
    total,data=review.review_mixed(); assert total=={"rows":12,"processed":39000,"granted":15600,"denied":19500,"unauthorized_floor":7800,"disabled_credential":5850,"unknown_credential":5850,"invalid_frame":3900,"other_outcomes":0}; assert len(data)==12

@pytest.mark.parametrize("mutation,match",[(lambda x:x["results"][0]["denied_by_reason"].__setitem__("unauthorized_floor",199),"totals"),(lambda x:x["results"][1].__setitem__("request_checksum_sha256","0"*64),"checksum"),(lambda x:x["results"][0].__setitem__("environment_id","bad"),"environment")])
def test_mixed_mutations_fail(review,monkeypatch,mutation,match):
    original=review.json_source; changed=json.loads((ROOT/"results/scalability_results.json").read_text());mutation(changed)
    monkeypatch.setattr(review,"json_source",lambda path: changed if path=="results/scalability_results.json" else original(path))
    with pytest.raises(review.ReviewError,match=match):review.review_mixed()

def test_isolated_exact_totals_and_boundaries(review):
    total,data=review.review_isolated(); assert total["calls"]==24000 and total["correct_hits"]==total["correct_misses"]==6000
    assert (total["correct_grants"],total["correct_denials"],total["correct_errors"],total["incorrect_grants"],total["incorrect_denials"],total["other_mismatches"])==(4800,6000,1200,0,0,0);assert len(data)==24

@pytest.mark.parametrize("mutation,match",[(lambda x:x["results"][0]["confusion_matrix"]["hit"].__setitem__("miss",1),"matrix"),(lambda x:x["results"][0].__setitem__("mismatch_count",1),"row count")])
def test_isolated_mutations_fail(review,monkeypatch,mutation,match):
    original=review.json_source;changed=json.loads((ROOT/"data/results/sp07_isolated_operation_results.json").read_text());mutation(changed)
    monkeypatch.setattr(review,"json_source",lambda path: changed if path=="data/results/sp07_isolated_operation_results.json" else original(path))
    with pytest.raises(review.ReviewError,match=match):review.review_isolated()

def test_isolated_repair_evidence_identity_is_enforced(review,monkeypatch):
    original=review.read_text
    monkeypatch.setattr(review,"read_text",lambda path:"unrelated record" if path=="audit/validation/subproject_07_02_timing_boundary_repair.md" else original(path))
    with pytest.raises(review.ReviewError,match="repair identity"):review.review_isolated()

def test_timing_all_twelve_recalculate_and_counts(review):
    _,mixed=review.review_mixed();_,isolated=review.review_isolated();table=review.review_timing(mixed,isolated)
    assert len(table)==12 and all(r["repetition_count"]=="3" for r in table)
    assert [r["calls_per_repetition"] for r in table[:4]]==["1000","1000","1000","10000"] and all(r["calls_per_repetition"]=="1000" for r in table[4:])
    assert all("pooled" not in r["interpretation"].lower() for r in table)

def test_altered_timing_median_and_p95_fail(review,monkeypatch):
    _,mixed=review.review_mixed();_,isolated=review.review_isolated();original=review.csv_source
    table=original("data/results/sp07_table_timing_summary.csv",review.TIMING_COLUMNS);table[0]["average_ns_median"]="1";table[1]["p95_ns_max"]="1"
    monkeypatch.setattr(review,"csv_source",lambda path,columns:table if path.endswith("timing_summary.csv") else original(path,columns))
    with pytest.raises(review.ReviewError,match="statistic mismatch"):review.review_timing(mixed,isolated)

def test_figures_reconcile_points_medians_whiskers_axes_units(review):
    _,mixed=review.review_mixed();_,isolated=review.review_isolated();figures=review.review_figures(mixed,isolated)
    assert len(figures)==3 and all(x["points"]==12 and x["medians"]==x["whiskers"]==4 for x in figures)

def test_altered_svg_point_fails(review,tmp_path,monkeypatch):
    root=tmp_path/"copy";root.mkdir()
    for p in review.SOURCES:
        t=root/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes((ROOT/p).read_bytes())
    p=root/"docs/figures/sp07_lookup_average_ns.svg";p.write_text(p.read_text().replace('data-value="297.496"','data-value="1"',1),encoding="utf-8")
    monkeypatch.setattr(review,"ROOT",root);_,mixed=review.review_mixed();_,isolated=review.review_isolated()
    with pytest.raises(review.ReviewError,match="plotted values"):review.review_figures(mixed,isolated)

def test_claim_ledger_schema_ids_sources_statuses_and_limits(review,outputs):
    ledger=rows(outputs["validation_ledger"]);assert tuple(ledger[0])==review.LEDGER_COLUMNS and len(ledger)==39
    assert [r["claim_id"] for r in ledger]==[f"CLM-{n:03d}" for n in range(1,40)]
    assert all(r["evaluation_status"] in {"supported","supported_with_limit"} and r["blocking_issue"]=="no" for r in ledger)
    assert all(r["required_limitations"] for r in ledger if r["claim_category"]=="timing")
    for row in ledger:
        for p in row["source_artifacts"].split(";"):assert (ROOT/p).exists()
    supported=" ".join(r["claim_text"].lower() for r in ledger);assert "branch coverage was measured" not in supported

def test_anomaly_register_required_entries_derived_and_nonblocking(review,outputs):
    anomalies=rows(outputs["anomaly_register"]);assert tuple(anomalies[0])==review.ANOMALY_COLUMNS and len(anomalies)==14
    assert all(r["blocking"]=="no" and r["report_implication"] for r in anomalies)
    text=" ".join(r["observation"].lower() for r in anomalies)
    for phrase in ("non-monotonic","greater than smaller","three measured repetitions","one recorded host","raw per-call","10000 requests","branch coverage","physical rfid"):assert phrase in text
    assert all("software defect" not in r["observation"].lower() for r in anomalies)

def test_summary_exact_order_counts_authorized_and_prohibited(outputs):
    value=json.loads(outputs["review_summary"]);assert tuple(value)==("schema_version","review_id","source_artifacts","artifact_integrity","verification_reconciliation","mixed_controller_reconciliation","isolated_operation_reconciliation","timing_table_reconciliation","figure_reconciliation","claim_review_summary","anomaly_summary","validity_threats","authorized_conclusions","prohibited_conclusions","report_handoff","readiness")
    assert value["review_id"]=="SP07_INDEPENDENT_REVIEW_V1" and value["claim_review_summary"]=={"total_ledger_rows":39,"supported":0,"supported_with_limit":39,"unresolved":0,"not_supported":0,"blocking_rows":0}
    assert value["anomaly_summary"]["total_anomalies"]==14 and value["anomaly_summary"]["blocking_anomaly_count"]==0
    assert "constant-time guarantee" in value["prohibited_conclusions"] and value["readiness"]=="READY FOR HUMAN REVIEW"

def test_source_notes_sections_boundaries_and_map(outputs):
    text=outputs["source_notes"].decode();assert text.startswith("# SP-07 Results and Discussion Source Notes\n")
    assert "not final report prose" in text and "human technical review" in text and "host-software observations" in text
    for n in range(1,15):assert f"## {n}." in text
    for p in ("data/results/sp07_table_experiment_coverage.csv","data/results/sp07_table_correctness.csv","data/results/sp07_table_timing_summary.csv","docs/figures/sp07_mixed_controller_average_ns.svg","docs/figures/sp07_lookup_average_ns.svg","docs/figures/sp07_authorization_average_ns.svg"):assert p in text
    assert "do not claim monotonic scaling" in text and "not a persistent-database query" in text and "not a zero field error rate" in text

def test_two_builds_serializations_and_successful_publication(review,outputs,tmp_path):
    assert review.build_outputs()==outputs
    dest=destinations(review,tmp_path);review.publish(dest,outputs);assert all(dest[k].read_bytes()==outputs[k] for k in dest);assert not list(tmp_path.rglob("*.tmp"))

def test_publication_failure_restores_all(review,outputs,tmp_path,monkeypatch):
    dest=destinations(review,tmp_path);[p.write_bytes(b"old") for p in dest.values()];original=review.os.replace;calls=0
    def fail(source,destination):
        nonlocal calls;calls+=1
        if calls==3:raise OSError("injected")
        return original(source,destination)
    monkeypatch.setattr(review.os,"replace",fail)
    with pytest.raises(review.ReviewError,match="preserved"):review.publish(dest,outputs)
    assert all(p.read_bytes()==b"old" for p in dest.values()) and not list(tmp_path.rglob("*.tmp"))

def test_incomplete_rollback_retains_recoverable_backup(review,outputs,tmp_path,monkeypatch):
    dest=destinations(review,tmp_path);[p.write_bytes(b"old") for p in dest.values()];original=review.os.replace;publication_count=0
    def fail(source,destination):
        nonlocal publication_count
        source=Path(source);destination=Path(destination)
        if destination in dest.values() and ".backup." not in source.name:
            publication_count+=1
            if publication_count==3:raise OSError("publication injected")
        if ".backup." in source.name and destination==dest["review_summary"]:raise OSError("restore injected")
        return original(source,destination)
    monkeypatch.setattr(review.os,"replace",fail)
    with pytest.raises(review.ReviewError,match="recovery backups retained"):review.publish(dest,outputs)
    retained=list(tmp_path.rglob("*.backup.*"));assert len(retained)==1 and retained[0].read_bytes()==b"old"
    assert dest["anomaly_register"].read_bytes()==b"old" and dest["validation_ledger"].read_bytes()==b"old" and dest["source_notes"].read_bytes()==b"old"

def test_cli_success_failure_and_required_arguments(review,tmp_path,capsys):
    dest=destinations(review,tmp_path);args=[]
    for key in review.OUTPUT_KEYS:args += ["--"+key.replace("_","-")+"-output",str(dest[key])]
    assert review.main(args)==0 and "blocking=0" in capsys.readouterr().out
    with pytest.raises(SystemExit) as raised:review.main([])
    assert raised.value.code==2
    assert len([a for a in review.parser()._actions if a.required])==4

def test_cli_handled_failure_is_one_error_line(review,tmp_path,monkeypatch,capsys):
    dest=destinations(review,tmp_path);args=[]
    for key in review.OUTPUT_KEYS:args += ["--"+key.replace("_","-")+"-output",str(dest[key])]
    def fail():raise review.ReviewError("injected")
    monkeypatch.setattr(review,"build_outputs",fail)
    assert review.main(args)==1
    captured=capsys.readouterr();assert captured.out=="" and captured.err=="error: injected\n"

def test_ast_independence_and_standard_library_boundary():
    tree=ast.parse(SCRIPT.read_text());imports=set()
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):imports.update(a.name.split('.')[0] for a in n.names)
        elif isinstance(n,ast.ImportFrom) and n.module:imports.add(n.module.split('.')[0])
    assert imports <= {"__future__","argparse","csv","hashlib","io","json","math","os","pathlib","statistics","sys","tempfile","xml"}
    assert imports.isdisjoint({"analysis","scripts","elevator_access_sim","subprocess","requests","socket","sqlite3","threading","asyncio","multiprocessing","random","time","numpy","pandas","matplotlib"})
    calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)]
    assert not any(isinstance(c.func,ast.Attribute) and c.func.attr in {"submit","sleep"} for c in calls)
