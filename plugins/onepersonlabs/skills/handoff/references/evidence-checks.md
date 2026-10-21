# Check handoff evidence

Read this reference after writing a handoff and before reporting it complete.
Run the bundled `scripts/validate-doc-claims.py` against the saved document.
The check is mechanical evidence review. It cannot establish that a claim is
true, that a citation supports the sentence, or that a historical account is
complete. Adjudicate every reported flag against the project and the handoff.

Run it from the project root:

```powershell
$handoffPath = "C:\path\to\handoff.md"
python -B -X utf8 plugins/onepersonlabs/skills/handoff/scripts/validate-doc-claims.py $handoffPath --repo-root .
```

The repository root argument matters when the handoff is in a temporary
directory. Repo paths are checked from the repository root. Relative Markdown
links are checked from the saved handoff directory. Use the
same paths on other shells, with that platform's Python command.

The script checks the document body for backticked repository paths, commit
identifiers, relative Markdown links, and drafting scaffold such as `Learning 2`
or `{{placeholder}}`. It does not fetch the network. Classification uses local
Git refs and the current working tree. If freshness matters, check the relevant
remote claim separately.

## Adjudicate each result

Resolve a flag by fixing the citation, marking it historical, or confirming it
is intentional. Never edit a document automatically to silence a flag.

| Result | Meaning and action |
| --- | --- |
| Path is absent from the working tree, but tracked at `HEAD` | It may be a deleted file or an uncommitted removal. Read the handoff's claim. If it describes the old state, mark the citation as historical; otherwise restore or correct it. |
| Path is absent locally but present at the upstream default branch | The checkout may be stale. Verify against that source and qualify any state claim that differs. |
| Path is absent from both the working tree and known refs | It may be a typo or a historical path unavailable in this checkout. Verify it. Correct it or label the history clearly. |
| A commit-like phrase precedes a SHA that does not resolve | Verify the commit in this repository. Replace a false citation with a valid reference or remove it. |
| An unresolved hex token has no nearby commit cue (`NOTE`) | It may be a session ID or content hash. Inspect the sentence. Verify it only if the handoff presents it as a commit. |
| A SHA resolves, but only in local or upstream history | The handoff may describe an unmerged, rebased, or not-yet-present change. Qualify it and verify remote state when that matters. |
| A relative Markdown link does not resolve | Fix the target relative to the saved handoff location. |
| Drafting scaffold is flagged | Replace it with the real reference or remove it. |

Git can show that a path was tracked and is now absent. Only the writer can
establish whether the handoff describes that earlier state. A flag asks for
adjudication; it is not proof of fabrication. A clean script result is not
semantic verification. Read the
important source claims directly and preserve meaningful uncertainty in the
handoff.

Exit code `0` means no flags remain. Exit code `1` means one or more flags need
adjudication; it is not an automatic failure. Exit code `2` means invalid usage
or an unreadable handoff. The script prints a summary of the checks it performed.
