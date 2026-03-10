# Sample Session: /git status

단순 상태 확인만 수행하는 예제.

## Session Flow

```
User: /git status

Claude:
📊 Git Status Dashboard
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feat/pt2i_to_face_swap_train → origin/feat/pt2i_to_face_swap_train
📡 Sync:   0 ahead, 0 behind  ✅
📈 Graph:  clean

📁 Changes:
  Unstaged (1):
    M  examples/flux2/model_training/lora/FLUX.2-klein-base-4B-true-face-swap.sh  (+36, -14)
  Staged: none
  Untracked: none
━━━━━━━━━━━━━━━━━━━━━━
```

`/git status`는 Phase 1 (ASSESS)만 수행하고 종료한다. 커밋/푸시 없음.
