#!/usr/bin/env python3
"""Structural validator for sdd-autopilot orchestrators.

Usage: python3 validate_orchestrator.py <orchestrator.md>
Exit codes: 0 = PASS, 1 = FAIL (findings printed), 2 = usage/IO error.

This script checks mechanically verifiable structure only. Philosophy and
quality review is delegated to the plan-review agent (Orchestrator Review
Mode) at autopilot Step 5.2.
"""

import re
import sys

# Runtime constants. The Claude variant of this script differs only here.
AGENT_FIELD = "Codex agent_type"
AGENT_PREFIX = ""

ALLOWED_BASE_AGENTS = {
    "feature-draft-agent",
    "spec-sync-agent",
    "implementation-plan-agent",
    "plan-review-agent",
    "implementation-agent",
    "implementation-review-agent",
    "simplicity-review-agent",
    "spec-review-agent",
    "ralph-loop-init-agent",
}
ALLOWED_AGENTS = {AGENT_PREFIX + name for name in ALLOWED_BASE_AGENTS}

REQUIRED_SECTIONS = [
    "기능 설명",
    "Acceptance Criteria",
    "Reasoning Trace",
    "Pipeline Steps",
    "Review-Fix Loop",
    "Test Strategy",
    "Error Handling",
]

VALID_INTERACTION_MODES = {"autonomous-no-input", "interactive-ok"}


def check(text):
    findings = []

    # 1. Required sections and metadata
    for section in REQUIRED_SECTIONS:
        if not re.search(
            r"^#{1,3}\s+.*" + re.escape(section), text, re.M
        ):
            findings.append(f"required section missing: '{section}'")
    if "**생성일**" not in text:
        findings.append("metadata missing: '**생성일**'")

    # 2. Per-step checks
    step_blocks = re.findall(
        r"^### Step[^\n]*\n(?:(?!^### ).*\n?)*", text, re.M
    )
    phase_iterative_declared = False
    for block in step_blocks:
        header = block.splitlines()[0]
        agent_match = re.search(
            r"\*\*" + re.escape(AGENT_FIELD) + r"\*\*:\s*`([^`]+)`", block
        )
        if agent_match:
            agent = agent_match.group(1).strip()
            if agent not in ALLOWED_AGENTS:
                findings.append(
                    f"{header}: non-canonical agent name '{agent}' "
                    f"(legacy alias → reject/regenerate)"
                )
            for field in ("입력 파일", "출력 파일", "프롬프트"):
                if f"**{field}**" not in block:
                    findings.append(f"{header}: required field missing: '{field}'")

        if re.search(r"\*\*Execution Mode\*\*:\s*`?phase-iterative`?", block):
            phase_iterative_declared = True
            src_match = re.search(r"\*\*Phase Source\*\*:\s*`([^`]+)`", block)
            if not src_match:
                findings.append(
                    f"{header}: 'Execution Mode: phase-iterative' requires 'Phase Source'"
                )
            else:
                src = src_match.group(1)
                if "feature_draft" in src:
                    findings.append(
                        f"{header}: Phase Source must not be a feature-draft artifact: {src}"
                    )
                elif "implementation_plan" not in src:
                    findings.append(
                        f"{header}: Phase Source must be an implementation-plan output: {src}"
                    )

        for mode_match in re.finditer(
            r"\*\*Interaction Mode\*\*:\s*`([^`]+)`", block
        ):
            mode = mode_match.group(1).strip()
            if mode not in VALID_INTERACTION_MODES:
                findings.append(f"{header}: invalid Interaction Mode '{mode}'")

    # 3. Review-fix gate fields (searched document-wide: gates may be inline in steps)
    scope_match = re.search(r"`?scope`?\s*[:=]\s*`?(global|per-group)`?", text)
    if not scope_match:
        findings.append("review-fix gate: 'scope' (global|per-group) not found")
    if not re.search(r"max_rounds", text):
        findings.append("review-fix gate: 'max_rounds' not found")
    if not re.search(
        r"critical\s*=\s*0\s*AND\s*high\s*=\s*0\s*AND\s*medium\s*=\s*0", text
    ):
        findings.append(
            "review-fix gate: exit_condition 'critical = 0 AND high = 0 AND medium = 0' not found"
        )

    def mapped_agents(role):
        pattern = r"(?<![\w-])" + re.escape(role) + r"\s*=\s*`?([A-Za-z0-9:_-]+)"
        return [m.strip() for m in re.findall(pattern, text)]

    # review/re-review must declare BOTH reviewers (correctness + simplicity);
    # fix maps to a single implementation-agent.
    for role in ("review", "re-review"):
        mapped = mapped_agents(role)
        if not mapped:
            findings.append(f"agent_mapping: '{role} = ...' not found")
            continue
        for expected_base in (
            "implementation-review-agent",
            "simplicity-review-agent",
        ):
            if AGENT_PREFIX + expected_base not in mapped:
                findings.append(
                    f"agent_mapping: '{role}' must map to "
                    f"'{AGENT_PREFIX}{expected_base}'"
                )

    fix_mapped = mapped_agents("fix")
    if not fix_mapped:
        findings.append("agent_mapping: 'fix = ...' not found")
    elif fix_mapped != [AGENT_PREFIX + "implementation-agent"]:
        findings.append(
            f"agent_mapping: 'fix' must map only to "
            f"'{AGENT_PREFIX}implementation-agent', got {fix_mapped}"
        )

    fix_targets_match = re.search(r"fix_targets`?\s*[:=]\s*`?([^\n`]+)", text)
    if fix_targets_match and re.search(r"\blow\b", fix_targets_match.group(1)):
        findings.append(
            "review-fix gate: 'low' must not be in fix_targets (low findings are advisory)"
        )

    # 4. per-group extras
    if scope_match and scope_match.group(1) == "per-group":
        for required in ("group exit criteria", "carry-over", "group boundary"):
            if required not in text:
                findings.append(f"per-group gate: '{required}' not declared")
        if not phase_iterative_declared:
            findings.append(
                "per-group gate requires a step with 'Execution Mode: phase-iterative'"
            )

    return findings


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"ERROR: cannot read {sys.argv[1]}: {e}", file=sys.stderr)
        return 2

    findings = check(text)
    if findings:
        print(f"FAIL: {len(findings)} structural finding(s)")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print("PASS: orchestrator structure conforms to contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
