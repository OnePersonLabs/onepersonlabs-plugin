# Interactive causal replay

## Forge the session

**Precondition -- is replay feasible here?** The forge-and-replay loop is the heart of this skill, but it only works when three things hold:

1. **The session is reachable.** The JSONL that produced the failure exists under `~/.codex/sessions/...` or `~/.claude/projects/...` and you can identify it by timestamp. A failure the user describes from memory, with no session on disk, can't be replayed.
2. **The failure is reproducible under replay.** It must reproduce from the forged cutpoint forward -- not depend on external state that has since changed (a file that's now fixed, a flag that's now set). If the world moved on, the replay tests against a world that no longer exists.
3. **The target agent CLI's full interactive environment is available.** On POSIX,
   use the Bash/tmux runner. On native Windows, use an observable manual replay
   in a native terminal as described below. Both routes must preserve the
   relevant skills, hooks, plugins, and permissions; print/exec mode is not a
   substitute for that interactive environment.

If any precondition fails, **do not fake it**: skip replay and develop the rule by reasoning instead, and tell the user the rule is **reasoned, not replay-tested** -- never present an untested rule as validated. Either way the source-backed causal analysis still stands.

Find the session that produced the failure. Codex sessions live in `~/.codex/sessions/YYYY/MM/DD/`; Claude Code sessions live in `~/.claude/projects/`. Use timestamp correlation with the slop entry to find the right JSONL file.

Analyze the session to find the **cutpoint** -- the assistant message just before
the failure. Resolve the scripts from the directory containing this loaded
`SKILL.md` and choose the current shell's commands.

In PowerShell:

```powershell
$unslopSkillDir = '<absolute directory containing this SKILL.md>'
python -X utf8 "$unslopSkillDir/scripts/forge-session.py" '<session.jsonl>' --analyze --agent auto
```

In a POSIX shell:

```bash
UNSLOP_SKILL_DIR="<absolute directory containing this SKILL.md>"
python3 -X utf8 "${UNSLOP_SKILL_DIR}/scripts/forge-session.py" "<session.jsonl>" --analyze --agent auto
```

Then forge a truncated copy:

In PowerShell:

```powershell
python -X utf8 "$unslopSkillDir/scripts/forge-session.py" '<session.jsonl>' '<cutpoint>' '<output-dir>' --agent auto --project-dir '<target-agent-session-dir>'
```

In a POSIX shell:

```bash
python3 -X utf8 "${UNSLOP_SKILL_DIR}/scripts/forge-session.py" "<session.jsonl>" "<cutpoint>" "<output-dir>" \
  --agent auto \
  --project-dir "<target-agent-session-dir>"
```

This truncates the JSONL at the cutpoint, rewrites the target agent's session id fields to a fresh UUID, and optionally places the forged session where the target agent can find it.

## Replay with candidate rules

**POSIX only:** the shipped `run-replay.sh` requires Bash and tmux. From an
existing POSIX environment, launch the forged session in its interactive runner:

```bash
bash "${UNSLOP_SKILL_DIR}/scripts/run-replay.sh" "<forged-session-id>" "<rule-file>" "<workspace-dir>" --agent <claude|codex>
```

For Codex, the runner defaults to Sol 6.1/medium. Use `--model` and `--effort`
to match the original session when that route remains available. Record a model
change as a causal limitation; do not call it equivalent reproduction.

Choose `--agent` from the target failure session, not from the worker. The script launches the matching interactive CLI inside a detached tmux session and captures output via `tmux capture-pane`.

**Native Windows:** use a manual interactive replay in a native PowerShell
terminal; keep the selected workspace and the original permission settings.
Read the candidate rule from its file, then run only the command matching the
target session:

```powershell
Set-Location -LiteralPath '<workspace-dir>'
$ruleText = Get-Content -LiteralPath '<rule-file>' -Raw
# Codex target:
codex fork '<forged-session-id>' "Rule under test: $ruleText"
# Claude Code target:
claude --resume '<forged-session-id>' --fork-session --append-system-prompt $ruleText
```

Continue the chosen session interactively and retain its resulting transcript
and observations for comparison. If direct terminal control is unavailable, the
user can run this replay and provide the trace. Keep each trial's evidence in a
distinct timestamped file under `.unslop/replay/`. If a usable interactive replay
or trace is unavailable, use the reasoning fallback from the replay preconditions and label the
rule **reasoned, not replay-tested**. Do not launch WSL or Git Bash to run the
POSIX helper from a native Windows workflow.

## Compare rule specificity

Start with the most general form of the corrective rule. If it fails, make it more concrete -- but never as specific as the exact scenario (that's overfitting). If it succeeds, try going slightly more general to find the widest effective rule.

**Too abstract** (agent ignores it): "Always assess task complexity before acting"
**Too specific** (overfits): "Don't use Agent tool when creating SKILL.md files"
**Sweet spot**: "Before exploring, ask: does the user's input already contain everything needed? If yes, start building. Exploration fills gaps in understanding, not confirms what you already know."

Compare a baseline with the smallest useful candidate. Add a broader or narrower
variant only when it can resolve a specific uncertainty about triggering or overfitting.

## Collect replay evidence

For each replay variant, record:

```json
{
  "variant": "broad | sweet-spot | narrow | baseline",
  "rule_text": "the candidate rule",
  "passed": true,
  "tool_calls_before_action": 4,
  "unnecessary_explorations": 0,
  "over_cautious": false,
  "notes": "3 targeted reads, then started writing"
}
```

A rule **passes** when the replayed agent avoids the original failure without introducing regressions:

- Over-caution (asking unnecessary questions, refusing valid actions)
- New failure modes (the rule causes a different kind of slop)
- Overfitting (only works for this exact scenario)

Prefer the broadest wording supported by the compared cases without losing
reliable triggering. Compare task outcomes and added effort; fewer tool calls
alone do not establish better reasoning or generalization.

Stop when evidence decides the change or further replay no longer earns its cost.
An inconclusive comparison does not establish that a hook is needed.

After the unslop workflow concludes and the final trace contains the evidence
needed to assess the result, the forged session files (including copies in
`.unslop/replay/`) and replay-generated sessions may be deleted. Keep them while
replays or comparisons are still in progress. Before deleting, identify the
synthetic session IDs and their descendants so the original failure session
and unrelated sessions remain untouched. "Never overwrite an existing trace"
and the instruction above to retain trial transcripts apply to the trace
and evidence during the workflow; they do not require permanent retention of
synthetic session rollouts.

## Present the rule

Show the user:

- The winning rule text
- The replay statistics table (variant, pass/fail, tool call count, notes)
- Whether the fix is a new rule or a rewrite of an existing instruction
- Where to insert it (AGENTS.md, rules file, skill, hook, or another project-level file)
- If it's an instruction rewrite, show the before/after diff

Apply instruction changes only within the authorized scope. If approval is
required, present the concrete change and evidence first. Additional replay
requires the same host permission and budget as the first comparison.
