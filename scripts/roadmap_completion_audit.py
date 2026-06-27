#!/usr/bin/env python3
"""Audit roadmap completion claims against lesson contract evidence."""
from __future__ import annotations
import argparse, json, re, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from dataclasses import asdict, dataclass
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PHASES_DIR = ROOT / "phases"
ROADMAP_PATH = ROOT / "ROADMAP.md"
DIR_RE = re.compile(r"^\d{2}-")
IGNORED_CODE_NAMES = {"README.md", "AGENTS.md", ".gitkeep", ".DS_Store"}
@dataclass(frozen=True)
class LessonFinding:
    phase: str; lesson: str; path: str; missing_docs: bool; missing_quiz: bool; empty_code: bool; missing_tests: bool
    @property
    def complete(self) -> bool:
        return not (self.missing_docs or self.missing_quiz or self.empty_code or self.missing_tests)
@dataclass(frozen=True)
class PhaseSummary:
    phase: str; lessons: int; complete: int; missing_docs: int; missing_quiz: int; empty_code: int; missing_tests: int; recommended_status: str; roadmap_heading_status: str | None
def has_meaningful_code(code_dir: Path) -> bool:
    return code_dir.is_dir() and any(p.is_file() and p.name not in IGNORED_CODE_NAMES for p in code_dir.rglob("*"))
def has_tests(code_dir: Path) -> bool:
    tests_dir = code_dir / "tests"
    return tests_dir.is_dir() and any(p.is_file() for p in tests_dir.rglob("*"))
def roadmap_phase_statuses() -> dict[str, str | None]:
    if not ROADMAP_PATH.is_file(): return {}
    text = ROADMAP_PATH.read_text(encoding="utf-8")
    return {f"{int(m.group(1)):02d}": m.group(2) for m in re.finditer(r"^## Phase (\d+):[^\n]*?—\s*([✅🚧⬚])", text, re.MULTILINE)}
def audit() -> tuple[list[LessonFinding], list[PhaseSummary]]:
    heading_statuses = roadmap_phase_statuses(); findings=[]; summaries=[]
    for phase in sorted(p for p in PHASES_DIR.iterdir() if p.is_dir() and DIR_RE.match(p.name)):
        phase_findings=[]
        for lesson in sorted(p for p in phase.iterdir() if p.is_dir() and DIR_RE.match(p.name)):
            code_dir = lesson / "code"
            f = LessonFinding(phase.name, lesson.name, lesson.relative_to(ROOT).as_posix(), not (lesson/"docs"/"en.md").is_file(), not (lesson/"quiz.json").is_file(), not has_meaningful_code(code_dir), not has_tests(code_dir))
            findings.append(f); phase_findings.append(f)
        complete=sum(f.complete for f in phase_findings); lessons=len(phase_findings); phase_num=phase.name.split("-",1)[0]
        summaries.append(PhaseSummary(phase.name, lessons, complete, sum(f.missing_docs for f in phase_findings), sum(f.missing_quiz for f in phase_findings), sum(f.empty_code for f in phase_findings), sum(f.missing_tests for f in phase_findings), "✅" if complete == lessons else ("🚧" if complete else "⬚"), heading_statuses.get(phase_num)))
    return findings, summaries
def render_text(findings, summaries) -> str:
    total=len(findings); complete=sum(f.complete for f in findings)
    out=[f"roadmap_completion_audit.py - {complete}/{total} lessons complete by strict contract", "", "Phase summary:"]
    for s in summaries:
        drift = f" (roadmap says {s.roadmap_heading_status})" if s.roadmap_heading_status and s.roadmap_heading_status != s.recommended_status else ""
        out.append(f"  {s.phase}: {s.complete}/{s.lessons} complete, missing_quiz={s.missing_quiz}, missing_tests={s.missing_tests}, empty_code={s.empty_code}, recommended={s.recommended_status}{drift}")
    incomplete=[f for f in findings if not f.complete]
    if incomplete:
        out += ["", f"Incomplete lessons: {len(incomplete)}"]
        for f in incomplete[:200]:
            gaps=[name for name,missing in (("docs",f.missing_docs),("quiz",f.missing_quiz),("code",f.empty_code),("tests",f.missing_tests)) if missing]
            out.append(f"  {f.path}: missing {', '.join(gaps)}")
        if len(incomplete)>200: out.append(f"  ... {len(incomplete)-200} more")
    return "\n".join(out)+"\n"
def main(argv):
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--json", action="store_true"); args=parser.parse_args(argv)
    findings,summaries=audit(); incomplete=[f for f in findings if not f.complete]
    if args.json:
        json.dump({"ok": not incomplete, "totals": {"lessons": len(findings), "complete": len(findings)-len(incomplete), "incomplete": len(incomplete)}, "phases": [asdict(s) for s in summaries], "incomplete_lessons": [asdict(f) for f in incomplete]}, sys.stdout, indent=2); sys.stdout.write("\n")
    else: sys.stdout.write(render_text(findings,summaries))
    return 1 if incomplete else 0
if __name__ == "__main__": raise SystemExit(main(sys.argv[1:]))




