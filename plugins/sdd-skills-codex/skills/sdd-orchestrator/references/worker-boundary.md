# Worker 공통 경계

`sdd-orchestrator`가 띄운 모든 worker가 자기 단계 계약과 함께 따른다.

- 사용자에게 질문하지 않는다. 필요한 결정은 합당한 해석으로 내리고 반환에 적는다. 진행할 수 없으면 BLOCKED와 사유를 반환한다.
- git 쓰기(commit·add·stash·checkout·reset 등)를 하지 않는다.
- 계약과 입력이 정한 대상 밖의 파일을 수정하지 않는다. 입력에 적힌, 동시에 실행 중인 다른 worker의 Target Files도 건드리지 않는다. 필요하면 수정하지 않고 반환에 적는다.
- state.md와 digest를 쓰지 않는다. 리뷰 worker(plan-review·implementation-review·simplicity)는 state.md를 읽지도 않는다.
- 다른 worker를 띄우지 않는다.
- 반환: 계약의 `반환` 형식을 따르고, 끝에 `digest 변경분` 블록을 붙인다(없으면 "없음"). 계약이 요구하는 항목만 짧게 쓴다 — 진행 서술과 요약은 쓰지 않는다.
