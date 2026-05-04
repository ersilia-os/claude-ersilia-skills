---
name: test-skill
description: >
  A minimal test skill to verify that the ersilia-skills repository and local
  setup (symlinks, git hook) are working correctly. Use this skill to confirm
  that skill loading, slash commands, and the setup.sh workflow are functioning
  as expected. Trigger on phrases like "run test skill", "check skill setup",
  or "verify ersilia skills".
allowed-tools: [Read, Bash]
---

# Test Skill

This is a placeholder skill used to verify the ersilia-skills repository setup.

## What this skill does

1. Confirm the skill was loaded correctly by reporting its name and location.
2. Check that `~/.claude/skills/test-skill` is a symlink pointing into the repo.
3. Print a success message.

## Steps

**Step 1 — Report skill identity**

Tell the user:
> "test-skill loaded successfully from the ersilia-skills repository."

**Step 2 — Verify symlink**

Run:
```bash
ls -la ~/.claude/skills/test-skill
```

If the output shows a symlink (`->`) pointing to the cloned repo path, tell the user the setup is working correctly. If it is a plain directory (not a symlink), advise them to run `bash setup.sh` from the repo root.

**Step 3 — Done**

Tell the user:
> "Skill setup verified. You can now delete or ignore this test-skill folder."
