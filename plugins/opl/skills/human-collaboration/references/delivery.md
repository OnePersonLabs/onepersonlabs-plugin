## Delivery and phone access

The session hooks report outstanding submissions only to their owning root. They
are inactive without a project inbox, do not initialize one, do not invoke a
model, and never block Stop. `PostToolUse` deduplicates notices; startup/resume,
new user turns and Stop re-surface unresolved work. Notifications are not claims.

Enrollment persists. Invoke `$opl:human-collaboration` again to enroll a different
root or restart a stopped service. The service stays running when the agent turn
ends. Add `--wake-root` to `connect` only when queue notifications are requested.
On Windows, `connect` opens a visible terminal owned by the server process.
The terminal shows startup, incoming requests, response status, and shutdown.
It also prints the full pairing URL, including the GUID and bearer token.
Logs omit URL queries, authentication headers, and request bodies. Close the
terminal window or press Ctrl+C to stop the server.
Use `pause-for-refresh` and `resume-after-refresh` only for the [refresh lifecycle](../SKILL.md#local-plugin-refresh);
ordinary recovery does not stop or start the service.
`serve` still runs a foreground service for an individual workspace;
`serve --catalog <runtime-directory>` serves registered workspaces. The default is `127.0.0.1:8766`.
Report the pairing link only after the service responds. It contains a bearer token; keep it
private. `--host lan --allow-lan` selects an active physical Windows adapter,
preferring one with a gateway and then the lowest interface metric. On POSIX it
uses the default route's private IPv4 address. Discovery failure is an explicit
error; choose a literal bind address instead. Phone reachability depends on the
network and firewall; successful host readiness does not prove it. For a
specific LAN/VPN address, use that literal IP and `--allow-lan`. Do not change firewalls, expose public HTTP, install a
service, or change global Codex configuration merely to make this work.
HTTP is not encrypted; use a trusted local network or private VPN. This is a
single-user local service, not an Internet-facing multi-user application.

Each server start creates a new GUID, a random identifier in the pairing URL's
`guid` query parameter. Every request must include that GUID, including page,
asset, and API requests. Without the current GUID, the server sends no response
and holds the connection until the client disconnects or the server stops.
The browser and readiness helper carry it automatically. API requests also
require the bearer token. After a restart, open the new pairing link; an old
link cannot load the page. A held connection uses a request thread and socket
until it closes. Keep this service on the authorized trusted network.

The browser starts with a newest-first combined message feed. It can filter to
one session. Lists show available projects and sessions that have contributions,
including completed ones. Unavailable projects and empty sessions are omitted;
their stored history is retained. The session list puts sessions needing human input first, then
sessions awaiting agent outcomes, then sessions with neither. Counts distinguish
`need you`, `with agent`, assumed answers, and deferred work. The browser refreshes every three
seconds while visible and when it regains focus. Background refresh preserves
the open composer. These HTTP reads do not notify or invoke agents.
Human-initiated contributions must select a recipient when several sessions are
registered. Item requests include the workspace ID so identical H-numbers in
different projects cannot route a response to the wrong project.

`connect --wake-root`, `serve --wake-root`, or `submit --notify` requests one `codex queue` notification
using OPL's existing executable resolver. The receipt distinguishes attempting,
accepted, failed, and unknown. Acceptance does not prove delivery or integration.
The message carries identifiers and a path, not the reply text. On timeout,
inspect before an explicit `notify --retry`; do not start an agent polling loop.
Without this option, feedback remains durably available to hooks and recovery.
The server is not another chat model and does not impersonate the root.
