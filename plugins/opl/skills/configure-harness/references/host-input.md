# Host question tool diagnosis

Read this branch after an observed `request_user_input` failure. Preserve the
question, originating task, settled decisions, and action withheld. Read the
actual error and live tool contract; distinguish a non-root restriction, an
exec host limitation, an unsupported mode, and a configuration problem.

A non-root agent routes its question through `$opl:route-agent-question`.
When the host cannot show the question, use the permitted chat channel at the
required time. Do not force a mode change or repeat the same failed call.

For an explicit request to diagnose future-session support, inspect the installed
Codex version, executable help, `codex features list`, and effective config.
Check current official documentation when local evidence is insufficient. The
presence or absence of a feature in another version does not establish this
host's support. Do not declare the input feature retired from one failed call.

Show the supported configuration change and its scope before applying it under
existing authority. Preserve unrelated configuration and verify the resulting
state. A config write does not retrofit the current tool surface. If a new
session is needed, offer `$opl:handoff` with the unresolved question and next
step; do not claim to have started that session.
