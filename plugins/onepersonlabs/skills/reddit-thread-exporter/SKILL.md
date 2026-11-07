---
name: reddit-thread-exporter
description: Export Reddit post pages as Markdown with nested comments, including replies exposed through inline More replies links. Use when a Reddit post or a supplied list of post URLs must be archived.
---

# Reddit thread exporter

Use this skill to save a Reddit post and its rendered comments as Markdown. Read [references/read_reddit_posts.ps1](references/read_reddit_posts.ps1) when you need to run or adapt the exporter.

The script requires PowerShell 7 and an available playwright-cli browser session. If a session is not attached to Chrome, use $opl:playwright-cli to connect to the user’s browser. Keep requests sequential.

## Run the exporter

Pass one post URL, several post URLs, or a text file that contains URLs:

~~~powershell
pwsh -File <skill-folder>\references\read_reddit_posts.ps1 -Url https://www.reddit.com/r/codex/comments/postid/title/ -Session chrome
pwsh -File <skill-folder>\references\read_reddit_posts.ps1 -UrlFile urls.txt -Session chrome
~~~

By default, the script writes Markdown files to the system temporary directory under reddit-thread-exporter. Use OutputDirectory to choose another folder.

Each new file uses this name:

~~~text
yyyyMMddHHmm_<url-title-slug>_####.md
~~~

The timestamp uses local time. The slug uses lowercase Windows- and WSL-safe characters, hyphens between words, and no more than five words. The four-digit sequence starts at 0001 and increases for each post in the run. Use Name, RunTimestamp, and StartNumber to override those parts. The script stops if a filename already exists unless Force is set.

To add full replies to existing export files, pass EnrichExisting and the folder that contains those files:

~~~powershell
pwsh -File <skill-folder>\references\read_reddit_posts.ps1 -EnrichExisting -OutputDirectory <existing-folder> -Session chrome
~~~

This mode finds Markdown files with Reddit URL metadata. It reads only the comment area from Reddit, preserves each file name and post body, and updates the nested comments and scrape counts.

## Comment handling

The script scrolls to the bottom repeatedly until the rendered comment list and page height stop changing. It expands collapsed comment nodes. It collects only Reddit’s inline a.more-comments-link continuation anchors for the same post. It inserts each continuation directly after the page that exposed it, then processes the queue in order. It does not follow post, profile, subreddit, or external links.

A continuation page is used only to collect comments. The script does not extract the post at the top of that page. It deduplicates comments by Reddit comment ID and nests replies under their parent comment ID. It stops if a reply has no parent in the collected tree.

The script waits a random 0.3 to 3 seconds before and after each navigation, scroll, and comment expansion. This pacing spreads requests and actions to reduce load on Reddit’s servers. The script does not run pages in parallel. It stops when Reddit returns an access challenge, HTTP 403, or HTTP 429. It retries one HTTP 5xx response after a 30-second wait.