# Experiments

## Pending
- [ ] 규범 항목별 횡단 census를 38개 Claude/Codex 진입 표면에 병행하면 기존 5쌍 리뷰가 보지 않은 P1/P2의 반복 지시와 reference 로드 누락을 찾을 수 있다. | 검증: `rg -n 'NORM-(HOME|JUDGMENT|DISCLOSURE|REFERENCE|INTERFACE|HARD-GATE).*PASS' _sdd/goal/2026-08-07_skill_authoring_norms_core_rollout/report.md` → 6종 rubric 전부 `PASS`
- [ ] 수정 전 mirror delta를 먼저 기록하고 3-way merge하면 다이어트 중 Codex runtime 적응과 Claude 고유 계약 손실을 막을 수 있다. | 검증: `python3 -c 'import glob,tomllib; fs=glob.glob(".codex/agents/*.toml"); [tomllib.load(open(f,"rb")) for f in fs]; print("TOML_OK",len(fs))'` → `TOML_OK 5`, 그리고 최종 mirror census `PASS`

## Done
- [x] 권장 — P0 세로 슬라이스를 기존 draft 순서대로 각각 full SDD chain으로 닫으면 계약 drift 없이 가장 빨리 핵심 경로를 안정화할 수 있다. | 결과: 5/5 feature·12/12 component `AUDITED`, 11 UPDATED + 1 NO_CHANGE; v4.6.44~v4.6.48 implemented sync 완료
