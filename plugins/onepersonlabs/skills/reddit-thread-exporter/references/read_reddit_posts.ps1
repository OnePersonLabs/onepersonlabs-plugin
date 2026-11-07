[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Url,
    [string]$UrlFile,
    [string]$OutputDirectory,
    [string]$Name,
    [string]$RunTimestamp,
    [ValidateRange(1, 999999)]
    [int]$StartNumber = 1,
    [string]$Session = 'chrome',
    [ValidateRange(300, 3000)]
    [int]$MinActionDelayMilliseconds = 300,
    [ValidateRange(300, 3000)]
    [int]$MaxActionDelayMilliseconds = 3000,
    [ValidateRange(1, 10000)]
    [int]$MaxThreadPages = 1000,
    [ValidateRange(1, 20)]
    [int]$StablePasses = 3,
    [ValidateRange(3, 100)]
    [int]$MaxScrollPasses = 50,
    [ValidateRange(10, 5000)]
    [int]$MaxPageActions = 5000,
    [switch]$EnrichExisting,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($PSVersionTable.PSVersion.Major -lt 7) {
    throw 'Run this script with PowerShell 7 or newer. PowerShell 5.1 can corrupt scraped UTF-8 text.'
}
if ($MinActionDelayMilliseconds -gt $MaxActionDelayMilliseconds) {
    throw 'MinActionDelayMilliseconds must be less than or equal to MaxActionDelayMilliseconds.'
}
if ($EnrichExisting -and -not $OutputDirectory) {
    throw 'EnrichExisting requires OutputDirectory so the script updates only the selected corpus.'
}
if ($RunTimestamp -and $RunTimestamp -notmatch '^\d{12}$') {
    throw 'RunTimestamp must use the format yyyyMMddHHmm.'
}
if ($Name -and ([regex]::Replace($Name.ToLowerInvariant(), '[^a-z0-9]+', '-').Trim('-').Split('-').Count -gt 5)) {
    throw 'Name can contain no more than five words.'
}

$playwrightCommand = Get-Command playwright-cli -ErrorAction Stop
$playwrightExecutable = $playwrightCommand.Source
if (-not $playwrightExecutable) {
    $playwrightExecutable = $playwrightCommand.Name
}

if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path ([System.IO.Path]::GetTempPath()) 'reddit-thread-exporter'
}
$OutputDirectory = [System.IO.Path]::GetFullPath($OutputDirectory)
[System.IO.Directory]::CreateDirectory($OutputDirectory) | Out-Null

if (-not $RunTimestamp) {
    $RunTimestamp = Get-Date -Format 'yyyyMMddHHmm'
}

function Get-RedditPostId {
    param([Parameter(Mandatory)][string]$Value)

    $uri = [uri]$Value
    if ($uri.Host -ne 'reddit.com' -and -not $uri.Host.EndsWith('.reddit.com', [StringComparison]::OrdinalIgnoreCase)) {
        throw "URL is not a Reddit URL: $Value"
    }
    $match = [regex]::Match($uri.AbsolutePath, '^/r/[^/]+/comments/(?<post>[^/]+)(?:/|$)', [Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if (-not $match.Success) {
        throw "URL is not a Reddit post or comment URL: $Value"
    }
    return $match.Groups['post'].Value
}

function ConvertTo-RedditPostUrl {
    param([Parameter(Mandatory)][string]$Value)

    $uri = [uri]$Value
    $postId = Get-RedditPostId -Value $Value
    $segments = @($uri.AbsolutePath.Trim('/').Split('/') | Where-Object { $_ })
    $postSegments = [System.Collections.Generic.List[string]]::new()
    for ($index = 0; $index -lt [Math]::Min(4, $segments.Count); $index++) {
        $postSegments.Add($segments[$index])
    }
    if ($segments.Count -ge 5 -and $segments[4] -ne 'comment') {
        $postSegments.Add($segments[4])
    }
    $postPath = '/' + ($postSegments -join '/') + '/'
    return [pscustomobject]@{
        Url = $uri.GetLeftPart([UriPartial]::Authority) + $postPath
        PostId = $postId
    }
}

function Get-CanonicalUrl {
    param([Parameter(Mandatory)][string]$Value)

    $uri = [uri]$Value
    $path = $uri.AbsolutePath.TrimEnd('/')
    return ('{0}://{1}{2}' -f $uri.Scheme.ToLowerInvariant(), $uri.Host.ToLowerInvariant(), $path)
}

function ConvertTo-SafeSlug {
    param(
        [Parameter(Mandatory)][string]$Value,
        [string]$Fallback = 'reddit-post'
    )

    $decoded = [Uri]::UnescapeDataString($Value).ToLowerInvariant()
    $words = @([regex]::Replace($decoded, '[^a-z0-9]+', '-').Trim('-').Split('-') | Where-Object { $_ } | Select-Object -First 5)
    if ($words.Count -eq 0) {
        return $Fallback
    }
    return $words -join '-'
}

function Get-UrlSlug {
    param([Parameter(Mandatory)][string]$Value)

    $uri = [uri]$Value
    $segments = @($uri.AbsolutePath.Trim('/').Split('/') | Where-Object { $_ })
    $titleSegment = if ($segments.Count -ge 5) { $segments[4] } else { 'reddit-post' }
    return ConvertTo-SafeSlug -Value $titleSegment
}

function Get-InputUrls {
    $values = [System.Collections.Generic.List[string]]::new()
    if ($Url) {
        foreach ($value in $Url) {
            if ($value) {
                $values.Add($value.Trim())
            }
        }
    }
    if ($UrlFile) {
        $resolvedUrlFile = (Resolve-Path -LiteralPath $UrlFile -ErrorAction Stop).Path
        foreach ($line in [System.IO.File]::ReadAllLines($resolvedUrlFile)) {
            $match = [regex]::Match($line, 'https?://[^\s|<>]+', [Text.RegularExpressions.RegexOptions]::IgnoreCase)
            if ($match.Success) {
                $values.Add($match.Value.TrimEnd('.', ',', ';', ')', ']'))
            }
        }
    }
    return $values
}

function Get-ExistingMarkdownPosts {
    param([Parameter(Mandatory)][string]$Directory)

    $posts = [System.Collections.Generic.List[object]]::new()
    foreach ($file in Get-ChildItem -LiteralPath $Directory -Filter '*.md' -File) {
        $content = [System.IO.File]::ReadAllText($file.FullName, [Text.Encoding]::UTF8)
        $match = [regex]::Match($content, '(?m)^- URL:\s*(https?://\S+)\s*$', [Text.RegularExpressions.RegexOptions]::IgnoreCase)
        if ($match.Success) {
            $post = ConvertTo-RedditPostUrl -Value $match.Groups[1].Value
            $posts.Add([pscustomobject]@{
                Url = $post.Url
                PostId = $post.PostId
                Path = $file.FullName
            })
        }
    }
    return $posts
}

$existingPosts = @()
$existingByPostId = @{}
$inputUrls = [System.Collections.Generic.List[string]]::new()

if ($EnrichExisting) {
    $existingPosts = @(Get-ExistingMarkdownPosts -Directory $OutputDirectory)
    if ($existingPosts.Count -eq 0) {
        throw "No Markdown exports with '- URL:' metadata were found in $OutputDirectory."
    }
    foreach ($post in $existingPosts) {
        $key = $post.PostId.ToLowerInvariant()
        if ($existingByPostId.ContainsKey($key)) {
            throw "More than one existing export has the same Reddit post ID: $($post.PostId)"
        }
        $existingByPostId[$key] = $post
    }
    $requested = @(Get-InputUrls)
    if ($requested.Count -gt 0) {
        $requestedIds = @{}
        foreach ($value in $requested) {
            $normalized = ConvertTo-RedditPostUrl -Value $value
            $requestedIds[$normalized.PostId.ToLowerInvariant()] = $true
        }
        foreach ($post in $existingPosts) {
            if ($requestedIds.ContainsKey($post.PostId.ToLowerInvariant())) {
                $inputUrls.Add($post.Url)
            }
        }
        $missing = @($requestedIds.Keys | Where-Object { -not $existingByPostId.ContainsKey($_) })
        if ($missing.Count -gt 0) {
            throw ("These requested post IDs do not have an existing export in {0}: {1}" -f $OutputDirectory, ($missing -join ', '))
        }
    }
    else {
        foreach ($post in $existingPosts) {
            $inputUrls.Add($post.Url)
        }
    }
}
else {
    foreach ($value in Get-InputUrls) {
        $normalized = ConvertTo-RedditPostUrl -Value $value
        $inputUrls.Add($normalized.Url)
    }
}

if ($inputUrls.Count -eq 0) {
    throw 'Provide one or more -Url values, a -UrlFile, or use -EnrichExisting with an output directory.'
}

$rootStates = [System.Collections.Generic.List[object]]::new()
$seenRoots = @{}
$nextNumber = $StartNumber
foreach ($value in $inputUrls) {
    $normalized = ConvertTo-RedditPostUrl -Value $value
    $rootUrl = $normalized.Url
    $rootKey = $normalized.PostId.ToLowerInvariant()
    if ($seenRoots.ContainsKey($rootKey)) {
        continue
    }
    $seenRoots[$rootKey] = $true

    $existingPath = $null
    if ($EnrichExisting) {
        $existingPath = $existingByPostId[$rootKey].Path
    }
    else {
        $slug = if ($Name) { ConvertTo-SafeSlug -Value $Name } else { Get-UrlSlug -Value $rootUrl }
        $fileName = '{0}_{1}_{2:D4}.md' -f $RunTimestamp, $slug, $nextNumber
        $existingPath = Join-Path $OutputDirectory $fileName
        if ((Test-Path -LiteralPath $existingPath) -and -not $Force) {
            throw "Output already exists: $existingPath. Use a new RunTimestamp, StartNumber, or -Force."
        }
        $nextNumber++
    }

    $rootStates.Add([pscustomobject]@{
        Url = $rootUrl
        PostId = $normalized.PostId
        OutputPath = $existingPath
        Existing = [bool]$EnrichExisting
        Post = $null
        Comments = @{}
        CommentOrder = [System.Collections.Generic.List[string]]::new()
        VisitedContinuationUrls = @{}
        ContinuationPages = 0
        PageCount = 0
        Warnings = [System.Collections.Generic.List[string]]::new()
    })
}

$driverTemplate = @'
async page => {
  const cfg = JSON.parse(atob("__CONFIG_BASE64__"));
  const pause = async () => {
    const span = cfg.maxDelay - cfg.minDelay;
    const milliseconds = cfg.minDelay + Math.floor(Math.random() * (span + 1));
    await page.waitForTimeout(milliseconds);
  };
  const canonical = value => {
    const url = new URL(value);
    return (url.protocol + "//" + url.host + url.pathname.replace(/\/+$/, "")).toLowerCase();
  };
  const currentUrl = page.url();
  let responseStatus = null;
  if (canonical(currentUrl) !== canonical(cfg.url)) {
    await pause();
    const response = await page.goto(cfg.url, { waitUntil: "domcontentloaded", timeout: cfg.navigationTimeout });
    responseStatus = response ? response.status() : null;
    if (responseStatus !== null && responseStatus >= 400) {
      return { httpStatus: responseStatus, pageUrl: page.url(), comments: [], links: [], post: null };
    }
  }

  const detectChallenge = async () => page.evaluate(() => {
    const title = document.title || "";
    const body = (document.body?.innerText || "").slice(0, 4000);
    const challengeElements = Array.from(document.querySelectorAll(
      'iframe[src*="captcha"], input[name*="captcha"], form[action*="challenge"], #captcha, [data-testid*="captcha"]'
    ));
    const isVisible = element => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== "none" &&
        style.visibility !== "hidden" &&
        Number(style.opacity || "1") > 0 &&
        rect.width > 0 &&
        rect.height > 0;
    };
    const visibleChallenge = challengeElements.some(isVisible);
    const blockedText = /verify you are human|complete the security check|you have been blocked|request has been blocked|unusual traffic from your computer/i;
    const visibleChallengeText = Array.from(document.querySelectorAll(
      '[role="dialog"], [id*="captcha"], [id*="challenge"], [class*="captcha"], [class*="challenge"]'
    )).some(element => isVisible(element) && blockedText.test(element.innerText || ""));
    const challengePath = /\/challenge(?:\/|$)|\/captcha(?:\/|$)/i.test(location.pathname);
    const textOnlyChallenge = !document.querySelector("shreddit-post") && blockedText.test(title + "\n" + body);
    return challengePath || visibleChallenge || visibleChallengeText || textOnlyChallenge
      ? { title, excerpt: body.slice(0, 500) }
      : null;
  });
  const initialChallenge = await detectChallenge();
  if (initialChallenge) {
    return { httpStatus: responseStatus, challenge: initialChallenge, pageUrl: page.url(), comments: [], links: [], post: null };
  }

  let expandedCount = 0;
  let actionCount = 0;
  let scrollPasses = 0;
  let stableCount = 0;
  let previousState = "";
  while (actionCount < cfg.maxPageActions) {
    const collapsedDetails = page.locator("shreddit-comment details:not([open])").first();
    if (await collapsedDetails.count()) {
      if (actionCount + 1 > cfg.maxPageActions) break;
      // Reddit marks collapsed comments with native details nodes. Set and verify
      // the open state so an ignored pointer click cannot keep this loop repeating.
      await pause();
      const expansion = await collapsedDetails.evaluate(detail => {
        const commentId = detail.closest("shreddit-comment")?.getAttribute("thingid") || "";
        detail.open = true;
        return { commentId, opened: detail.open };
      });
      actionCount++;
      if (!expansion.opened) {
        throw new Error("A collapsed comment details node did not open when its native open state was set.");
      }
      await pause();
      if (expansion.commentId) {
        const commentDetails = page.locator(`shreddit-comment[thingid="${expansion.commentId}"] details`);
        if (await commentDetails.count() && !(await commentDetails.first().evaluate(detail => detail.open))) {
          throw new Error(`Collapsed comment ${expansion.commentId} closed again after expansion.`);
        }
      }
      expandedCount++;
      stableCount = 0;
      scrollPasses = 0;
      previousState = "";
      await pause();
      continue;
    }

    const collapsedButtons = page.locator(
      'shreddit-comment button[aria-expanded="false"], shreddit-comment [role="button"][aria-expanded="false"]'
    );
    let expandTarget = null;
    for (let index = 0; index < await collapsedButtons.count(); index++) {
      const candidate = collapsedButtons.nth(index);
      const label = ((await candidate.getAttribute("aria-label")) || "") + " " + ((await candidate.innerText().catch(() => "")) || "");
      if (/comment|repl|thread|expand/i.test(label) && !/menu|award|share|vote|report/i.test(label)) {
        expandTarget = candidate;
        break;
      }
    }
    if (expandTarget) {
      const beforeState = await page.evaluate(() => {
        const selector = 'shreddit-comment button[aria-expanded="false"], shreddit-comment [role="button"][aria-expanded="false"]';
        const candidates = Array.from(document.querySelectorAll(selector));
        const expandableButtons = candidates.filter(element => {
          const label = (element.getAttribute("aria-label") || "") + " " + (element.innerText || "");
          return /comment|repl|thread|expand/i.test(label) && !/menu|award|share|vote|report/i.test(label);
        }).length;
        return {
          comments: document.querySelectorAll("shreddit-comment[thingid]").length,
          links: document.querySelectorAll("a.more-comments-link").length,
          collapsedDetails: document.querySelectorAll("shreddit-comment details:not([open])").length,
          expandableButtons
        };
      });
      await pause();
      await expandTarget.click({ timeout: 5000 });
      actionCount++;
      let expanded = false;
      let afterState = beforeState;
      for (let attempt = 0; attempt < 3; attempt++) {
        await pause();
        afterState = await page.evaluate(() => {
          const selector = 'shreddit-comment button[aria-expanded="false"], shreddit-comment [role="button"][aria-expanded="false"]';
          const candidates = Array.from(document.querySelectorAll(selector));
          const expandableButtons = candidates.filter(element => {
            const label = (element.getAttribute("aria-label") || "") + " " + (element.innerText || "");
            return /comment|repl|thread|expand/i.test(label) && !/menu|award|share|vote|report/i.test(label);
          }).length;
          return {
            comments: document.querySelectorAll("shreddit-comment[thingid]").length,
            links: document.querySelectorAll("a.more-comments-link").length,
            collapsedDetails: document.querySelectorAll("shreddit-comment details:not([open])").length,
            expandableButtons
          };
        });
        expanded = afterState.comments > beforeState.comments ||
          afterState.links > beforeState.links ||
          afterState.collapsedDetails > beforeState.collapsedDetails ||
          afterState.expandableButtons < beforeState.expandableButtons;
        if (expanded) break;
      }
      if (!expanded) {
        throw new Error("A collapsed comment button did not reveal more comments or change its expansion state after one click.");
      }
      expandedCount++;
      stableCount = 0;
      scrollPasses = 0;
      previousState = "";
      continue;
    }

    if (stableCount >= cfg.stablePasses) {
      break;
    }
    if (scrollPasses >= cfg.maxScrollPasses) {
      break;
    }
    await pause();
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    actionCount++;
    scrollPasses++;
    await pause();
    const state = await page.evaluate(() => ({
      comments: document.querySelectorAll("shreddit-comment[thingid]").length,
      links: document.querySelectorAll("a.more-comments-link").length,
      height: document.documentElement.scrollHeight
    }));
    const stateKey = JSON.stringify(state);
    if (stateKey === previousState) {
      stableCount++;
    } else {
      stableCount = 0;
      previousState = stateKey;
    }
  }

  const pageData = await page.evaluate(includePost => {
    const markdown = root => {
      if (!root) return "";
      const render = node => {
        if (node.nodeType === Node.TEXT_NODE) return node.nodeValue || "";
        if (node.nodeType !== Node.ELEMENT_NODE) return "";
        const tag = node.tagName.toLowerCase();
        if (tag === "br") return "\n";
        if (tag === "img") {
          const src = node.getAttribute("src") || node.getAttribute("data-src") || "";
          const alt = node.getAttribute("alt") || "Image";
          return src ? "![" + alt.replace(/]/g, "\\]") + "](" + src + ")" : "";
        }
        if (tag === "pre") {
          const fence = String.fromCharCode(96).repeat(3);
          return "\n\n" + fence + "\n" + (node.innerText || node.textContent || "").replace(/\s+$/, "") + "\n" + fence + "\n\n";
        }
        const children = Array.from(node.childNodes).map(render).join("");
        if (tag === "a") {
          const href = node.getAttribute("href") || "";
          const label = children.trim() || href;
          return href && label ? "[" + label + "](" + href + ")" : label;
        }
        if (tag === "strong" || tag === "b") return "**" + children.trim() + "**";
        if (tag === "em" || tag === "i") return "*" + children.trim() + "*";
        if (tag === "code") return String.fromCharCode(96) + children.trim() + String.fromCharCode(96);
        if (tag === "blockquote") {
          const quoted = children.trim().split(/\r?\n/).map(line => line ? "> " + line : ">").join("\n");
          return "\n\n" + quoted + "\n\n";
        }
        if (tag === "li") return "- " + children.trim() + "\n";
        if (tag === "ul" || tag === "ol") {
          return "\n" + Array.from(node.children).map(render).join("").trimEnd() + "\n\n";
        }
        if (/^h[1-6]$/.test(tag)) {
          const level = Number(tag[1]);
          return "\n\n" + "#".repeat(level) + " " + children.trim() + "\n\n";
        }
        if (["p", "div", "section", "article"].includes(tag)) return "\n\n" + children.trim() + "\n\n";
        if (tag === "hr") return "\n\n---\n\n";
        return children;
      };
      return Array.from(root.childNodes).map(render).join("")
        .replace(/\u00a0/g, " ")
        .replace(/[ \t]+\n/g, "\n")
        .replace(/\n[ \t]+/g, "\n")
        .replace(/\n{3,}/g, "\n\n")
        .trim();
    };

    const comments = Array.from(document.querySelectorAll("shreddit-comment[thingid]")).map(comment => {
      const body = comment.querySelector('[slot="comment"]');
      return {
        id: comment.getAttribute("thingid") || "",
        parentId: comment.getAttribute("parentid") || "",
        author: comment.getAttribute("author") || "[deleted]",
        created: comment.getAttribute("created") || "",
        score: comment.getAttribute("score") || "",
        body: markdown(body)
      };
    });
    const links = Array.from(document.querySelectorAll("a.more-comments-link")).map(link => {
      const parent = link.closest("shreddit-comment");
      return {
        href: link.href,
        parentId: parent?.getAttribute("thingid") || "",
        text: (link.innerText || "").trim()
      };
    });

    let post = null;
    if (includePost) {
      const element = document.querySelector("shreddit-post");
      if (element) {
        const titleElement = element.querySelector('[slot="title"]') || document.querySelector("h1");
        const bodyElement = element.querySelector('[slot="text-body"]');
        post = {
          title: element.getAttribute("post-title") || titleElement?.innerText?.trim() || "",
          author: element.getAttribute("author") || "",
          created: element.getAttribute("created-timestamp") || "",
          score: element.getAttribute("score") || "",
          body: markdown(bodyElement)
        };
      }
    }
    const match = location.pathname.match(/\/r\/[^/]+\/comments\/([^/]+)/i);
    return {
      pageUrl: location.href,
      postId: match?.[1] || "",
      comments,
      links,
      post
    };
  }, cfg.includePost);

  const finalChallenge = await detectChallenge();
  const remainingCollapsed = await page.locator("shreddit-comment details:not([open])").count();
  const stableReached = stableCount >= cfg.stablePasses;
  const finalState = await page.evaluate(() => ({
    comments: document.querySelectorAll("shreddit-comment[thingid]").length,
    links: document.querySelectorAll("a.more-comments-link").length,
    height: document.documentElement.scrollHeight
  }));
  return {
    httpStatus: responseStatus,
    pageUrl: pageData.pageUrl,
    postId: pageData.postId,
    comments: pageData.comments,
    links: pageData.links,
    post: pageData.post,
    expandedCount,
    remainingCollapsed,
    stableReached,
    actionCount,
    scrollPasses,
    stableCount,
    finalState,
    challenge: finalChallenge
  };
}
'@

function Invoke-RedditPage {
    param(
        [Parameter(Mandatory)][string]$PageUrl,
        [Parameter(Mandatory)][bool]$IncludePost
    )

    $config = [ordered]@{
        url = $PageUrl
        includePost = $IncludePost
        minDelay = $MinActionDelayMilliseconds
        maxDelay = $MaxActionDelayMilliseconds
        stablePasses = $StablePasses
        maxScrollPasses = $MaxScrollPasses
        maxPageActions = $MaxPageActions
        navigationTimeout = 60000
    }
    $json = ConvertTo-Json -InputObject $config -Compress
    $base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($json))
    $driverSource = $driverTemplate.Replace('__CONFIG_BASE64__', $base64)
    $driverPath = Join-Path ([System.IO.Path]::GetTempPath()) ('reddit-page-' + [guid]::NewGuid().ToString('N') + '.js')
    [System.IO.File]::WriteAllText($driverPath, $driverSource, [Text.UTF8Encoding]::new($false))

    try {
        for ($attempt = 1; $attempt -le 2; $attempt++) {
            $cliOutput = @(& $playwrightExecutable '--raw' "-s=$Session" 'run-code' "--filename=$driverPath" 2>&1)
            $exitCode = $LASTEXITCODE
            $raw = ($cliOutput | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
            if ($exitCode -ne 0) {
                throw "playwright-cli failed on $PageUrl with exit code $exitCode. Output: $raw"
            }
            try {
                $pageResult = $raw | ConvertFrom-Json -AsHashtable -ErrorAction Stop
            }
            catch {
                throw "playwright-cli returned invalid JSON on $PageUrl. Output: $raw"
            }

            if ($pageResult.httpStatus -ge 500 -and $pageResult.httpStatus -le 599) {
                if ($attempt -eq 1) {
                    Write-Warning "Reddit returned HTTP $($pageResult.httpStatus) for $PageUrl. Waiting 30 seconds before one retry."
                    Start-Sleep -Seconds 30
                    continue
                }
                throw "Reddit returned HTTP $($pageResult.httpStatus) twice for $PageUrl. Stopping this export."
            }
            if ($pageResult.httpStatus -ge 400) {
                throw "Reddit returned HTTP $($pageResult.httpStatus) for $PageUrl. The export stopped without retry."
            }
            if ($pageResult.challenge) {
                throw "Reddit presented an access challenge on $PageUrl. The export stopped without attempting to bypass it."
            }
            if ($pageResult.postId -and $pageResult.postId -ne (Get-RedditPostId -Value $PageUrl)) {
                throw "The page resolved to post $($pageResult.postId), but the requested URL belongs to another Reddit post: $PageUrl"
            }
            if (-not $pageResult.stableReached) {
                throw ("The comment list did not reach a stable lazy-load state after {0} page actions and {1} bottom-scroll passes (comments={2}, continuation links={3}, height={4}) on {5}. No Markdown was written for this post." -f $pageResult.actionCount, $pageResult.scrollPasses, $pageResult.finalState.comments, $pageResult.finalState.links, $pageResult.finalState.height, $PageUrl)
            }
            if ($pageResult.remainingCollapsed -gt 0) {
                throw "The page still has $($pageResult.remainingCollapsed) collapsed comment nodes on $PageUrl. No Markdown was written for this post."
            }
            return $pageResult
        }
    }
    finally {
        Remove-Item -LiteralPath $driverPath -Force -ErrorAction SilentlyContinue
    }
}

function Add-PageComments {
    param(
        [Parameter(Mandatory)]$State,
        [Parameter(Mandatory)]$PageResult
    )

    foreach ($comment in $PageResult.comments) {
        $id = [string]$comment.id
        if (-not $id) {
            continue
        }
        if (-not $State.Comments.ContainsKey($id)) {
            $State.Comments[$id] = [pscustomobject]@{
                Id = $id
                ParentId = [string]$comment.parentId
                Author = [string]$comment.author
                Created = [string]$comment.created
                Score = [string]$comment.score
                Body = [string]$comment.body
                Children = [System.Collections.Generic.List[object]]::new()
            }
            $State.CommentOrder.Add($id)
        }
        elseif (-not $State.Comments[$id].Body -and $comment.body) {
            $State.Comments[$id].Body = [string]$comment.body
        }
    }
}

function ConvertTo-ValidContinuation {
    param(
        [Parameter(Mandatory)][string]$Value,
        [Parameter(Mandatory)][string]$PostId
    )

    try {
        $uri = [uri]$Value
    }
    catch {
        return $null
    }
    if ($uri.Host -ne 'reddit.com' -and -not $uri.Host.EndsWith('.reddit.com', [StringComparison]::OrdinalIgnoreCase)) {
        return $null
    }
    $match = [regex]::Match($uri.AbsolutePath, '^/r/[^/]+/comments/(?<post>[^/]+)/comment/(?<comment>[^/]+)/?$', [Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if (-not $match.Success -or $match.Groups['post'].Value -ne $PostId) {
        return $null
    }
    return $uri.AbsoluteUri
}

function Format-CommentDate {
    param([string]$Value)

    if (-not $Value) {
        return 'Not available in the rendered page'
    }
    try {
        $date = [DateTimeOffset]::Parse($Value, [Globalization.CultureInfo]::InvariantCulture).ToUniversalTime()
        return $date.ToString('yyyy-MM-dd HH:mm:ss UTC', [Globalization.CultureInfo]::InvariantCulture)
    }
    catch {
        return 'Not available in the rendered page'
    }
}

function Format-CommentVotes {
    param([string]$Value)

    if ($Value -match '^-?\d+$') {
        return $Value
    }
    return 'Not available in the rendered page'
}

function Build-CommentTree {
    param([Parameter(Mandatory)]$State)

    $roots = [System.Collections.Generic.List[object]]::new()
    foreach ($id in $State.CommentOrder) {
        $comment = $State.Comments[$id]
        $parentId = $comment.ParentId
        if ($parentId -match '^t1_') {
            if (-not $State.Comments.ContainsKey($parentId)) {
                throw "Comment $id has parent $parentId, but the parent was not found in the root or continuation pages for $($State.Url)."
            }
            $State.Comments[$parentId].Children.Add($comment)
        }
        else {
            $roots.Add($comment)
        }
    }
    return $roots
}

function Add-RenderedComment {
    param(
        [Parameter(Mandatory)]$Comment,
        [Parameter(Mandatory)][int]$Depth,
        [Parameter(Mandatory)][System.Text.StringBuilder]$Builder
    )

    $indent = '  ' * $Depth
    $author = if ($Comment.Author) { $Comment.Author } else { '[deleted]' }
    $date = Format-CommentDate -Value $Comment.Created
    $votes = Format-CommentVotes -Value $Comment.Score
    $Builder.AppendLine($indent + '- **' + $author + '** -- ' + $date + ' -- votes: ' + $votes) | Out-Null

    $body = [string]$Comment.Body
    if (-not $body) {
        $body = 'Comment body was not available in the rendered page.'
    }
    foreach ($line in ($body -split '\r?\n')) {
        $Builder.AppendLine($indent + '  ' + $line) | Out-Null
    }
    $Builder.AppendLine() | Out-Null

    foreach ($child in $Comment.Children) {
        Add-RenderedComment -Comment $child -Depth ($Depth + 1) -Builder $Builder
    }
}

function New-CommentsMarkdown {
    param([Parameter(Mandatory)]$State)

    $roots = Build-CommentTree -State $State
    $builder = [System.Text.StringBuilder]::new()
    foreach ($comment in $roots) {
        Add-RenderedComment -Comment $comment -Depth 0 -Builder $builder
    }
    return $builder.ToString().TrimEnd([char[]]@([char]13, [char]10))
}

function New-ExtractionNotesMarkdown {
    param([Parameter(Mandatory)]$State)

    $missingVotes = @(
        foreach ($id in $State.CommentOrder) {
            if ($State.Comments[$id].Score -notmatch '^-?\d+$') {
                '- Comment ' + $id + ' has no rendered votes.'
            }
        }
    )
    if ($missingVotes.Count -eq 0) {
        return ''
    }
    return ('## Extraction notes' + [Environment]::NewLine + [Environment]::NewLine + ($missingVotes -join [Environment]::NewLine))
}

function Write-Utf8Atomically {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Content
    )

    $tempPath = Join-Path (Split-Path -Parent $Path) ('.reddit-export-' + [guid]::NewGuid().ToString('N') + '.tmp')
    try {
        [System.IO.File]::WriteAllText($tempPath, $Content, [Text.UTF8Encoding]::new($false))
        Move-Item -LiteralPath $tempPath -Destination $Path -Force
    }
    finally {
        if (Test-Path -LiteralPath $tempPath) {
            Remove-Item -LiteralPath $tempPath -Force
        }
    }
}

function Update-ExistingMarkdown {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][AllowEmptyString()][string]$CommentMarkdown,
        [Parameter(Mandatory)][AllowEmptyString()][AllowNull()][string]$NotesMarkdown,
        [Parameter(Mandatory)][int]$CommentCount,
        [Parameter(Mandatory)][int]$ContinuationCount
    )

    $content = [System.IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
    $newline = [Environment]::NewLine
    $commentsPattern = '(?ms)^## Comments[ \t]*\r?\n.*?(?=^## |\z)'
    if (-not [regex]::IsMatch($content, $commentsPattern)) {
        throw "The existing export has no '## Comments' section: $Path"
    }
    $section = '## Comments' + $newline + $newline
    if ($CommentMarkdown) {
        $section += ($CommentMarkdown -replace '\r?\n', $newline) + $newline + $newline
    }
    else {
        $section += '_No comments were rendered on this page._' + $newline + $newline
    }
    $content = [regex]::Replace($content, $commentsPattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($match) $section })

    $content = [regex]::Replace($content, '(?m)^- Comments scraped:\s*.*$', "- Comments scraped: $CommentCount")
    $continuationLine = "- Comment continuation pages scraped: $ContinuationCount"
    if ([regex]::IsMatch($content, '(?m)^- (?:Inline comment expansions|Comment continuation pages scraped):\s*.*$')) {
        $content = [regex]::Replace($content, '(?m)^- (?:Inline comment expansions|Comment continuation pages scraped):\s*.*$', $continuationLine)
    }
    else {
        $content = [regex]::Replace($content, '(?m)^- Comments scraped:\s*.*$', '$0' + $newline + $continuationLine)
    }

    $notesPattern = '(?ms)^## Extraction notes[ \t]*\r?\n.*?(?=^## |\z)'
    if ([regex]::IsMatch($content, $notesPattern)) {
        $notesMatch = [regex]::Match($content, $notesPattern)
        $preservedNotes = @(
            $notesMatch.Value -split '\r?\n' |
                Where-Object {
                    $_ -notmatch '^\s*-\s*Comment t\d+_[a-z0-9]+ has no rendered votes\.\s*$' -and
                    $_ -notmatch '^## Extraction notes\s*$'
                }
        )
        if ($NotesMarkdown -or $preservedNotes.Count -gt 0) {
            $noteLines = [System.Collections.Generic.List[string]]::new()
            $noteLines.Add('## Extraction notes')
            $noteLines.Add('')
            foreach ($line in $preservedNotes) {
                if ($line) {
                    $noteLines.Add($line)
                }
            }
            if ($NotesMarkdown) {
                foreach ($line in ($NotesMarkdown -split '\r?\n' | Select-Object -Skip 2)) {
                    $noteLines.Add($line)
                }
            }
            $notesSection = ($noteLines -join $newline) + $newline + $newline
            $content = [regex]::Replace($content, $notesPattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($match) $notesSection })
        }
        else {
            $content = [regex]::Replace($content, $notesPattern, '')
        }
    }
    elseif ($NotesMarkdown) {
        $content = $content.TrimEnd() + $newline + $newline + $NotesMarkdown + $newline
    }
    Write-Utf8Atomically -Path $Path -Content $content
}

function New-PostMarkdown {
    param(
        [Parameter(Mandatory)]$State,
        [Parameter(Mandatory)][AllowEmptyString()][string]$CommentMarkdown,
        [Parameter(Mandatory)][AllowEmptyString()][AllowNull()][string]$NotesMarkdown
    )

    if (-not $State.Post) {
        throw "The root page did not provide post metadata: $($State.Url)"
    }
    $post = $State.Post
    $title = if ($post.title) { [string]$post.title } else { 'Title unavailable in the rendered page' }
    $author = if ($post.author) { [string]$post.author } else { 'Not available in the rendered page' }
    $date = Format-CommentDate -Value ([string]$post.created)
    $votes = Format-CommentVotes -Value ([string]$post.score)
    $body = [string]$post.body
    if (-not $body) {
        $body = '_Post body was not available in the rendered page._'
    }

    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add('# ' + $title)
    $lines.Add('')
    $lines.Add('- URL: ' + $State.Url)
    $lines.Add('- User: ' + $author)
    $lines.Add('- Date: ' + $date)
    $lines.Add('- Votes: ' + $votes)
    $lines.Add('- Comments scraped: ' + $State.Comments.Count)
    $lines.Add('- Comment continuation pages scraped: ' + $State.ContinuationPages)
    $lines.Add('')
    $lines.Add('## Post body')
    $lines.Add('')
    $lines.Add($body)
    $lines.Add('')
    $lines.Add('## Comments')
    $lines.Add('')
    if ($CommentMarkdown) {
        $lines.Add($CommentMarkdown)
    }
    else {
        $lines.Add('_No comments were rendered on this page._')
    }
    if ($NotesMarkdown) {
        $lines.Add('')
        $lines.Add($NotesMarkdown)
    }
    $lines.Add('')
    return $lines -join [Environment]::NewLine
}

$jobs = [System.Collections.Generic.List[object]]::new()
foreach ($state in $rootStates) {
    $jobs.Add([pscustomobject]@{
        State = $state
        Url = $state.Url
        IsRoot = $true
        ParentCommentId = ''
    })
}

$jobIndex = 0
while ($jobIndex -lt $jobs.Count) {
    $job = $jobs[$jobIndex]
    $state = $job.State
    if (-not $job.IsRoot -and $state.ContinuationPages -ge $MaxThreadPages) {
        throw "Thread page limit $MaxThreadPages was reached for $($state.Url). No partial Markdown was written for this post."
    }

    $includePost = $job.IsRoot -and -not $state.Existing
    $pageResult = Invoke-RedditPage -PageUrl $job.Url -IncludePost $includePost
    $state.PageCount++
    if (-not $job.IsRoot) {
        $state.ContinuationPages++
    }
    if ($pageResult.expandedCount -gt 0) {
        $state.Warnings.Add("Expanded $($pageResult.expandedCount) collapsed comment nodes on $($job.Url).")
    }
    if ($job.IsRoot -and $includePost) {
        $state.Post = $pageResult.post
        if (-not $state.Post -or -not $state.Post.title) {
            throw "The root page did not expose post title, author, date, votes, and body metadata: $($state.Url)"
        }
    }

    Add-PageComments -State $state -PageResult $pageResult
    if (-not $job.IsRoot -and $job.ParentCommentId -and -not $state.Comments.ContainsKey($job.ParentCommentId)) {
        throw "Continuation page $($job.Url) did not include its linked parent comment $($job.ParentCommentId)."
    }

    $newJobs = [System.Collections.Generic.List[object]]::new()
    foreach ($link in $pageResult.links) {
        $continuationUrl = ConvertTo-ValidContinuation -Value ([string]$link.href) -PostId $state.PostId
        if (-not $continuationUrl) {
            continue
        }
        if (-not $link.parentId) {
            $state.Warnings.Add("Skipped a continuation link without a parent comment ID on $($job.Url).")
            continue
        }
        $continuationKey = Get-CanonicalUrl -Value $continuationUrl
        if ($state.VisitedContinuationUrls.ContainsKey($continuationKey)) {
            continue
        }
        $state.VisitedContinuationUrls[$continuationKey] = $true
        $newJobs.Add([pscustomobject]@{
            State = $state
            Url = $continuationUrl
            IsRoot = $false
            ParentCommentId = [string]$link.parentId
        })
    }
    for ($insertIndex = $newJobs.Count - 1; $insertIndex -ge 0; $insertIndex--) {
        $jobs.Insert($jobIndex + 1, $newJobs[$insertIndex])
    }

    $status = 'root'
    if (-not $job.IsRoot) {
        $status = 'continuation'
    }
    Write-Output ("[{0}/{1}] {2} page, {3} comments, {4} continuation pages: {5}" -f ($jobIndex + 1), $jobs.Count, $status, $state.Comments.Count, $state.ContinuationPages, $job.Url)
    $jobIndex++

    $unfinishedForState = $false
    for ($pendingIndex = $jobIndex; $pendingIndex -lt $jobs.Count; $pendingIndex++) {
        if ([object]::ReferenceEquals($jobs[$pendingIndex].State, $state)) {
            $unfinishedForState = $true
            break
        }
    }
    if (-not $unfinishedForState) {
        $commentMarkdown = New-CommentsMarkdown -State $state
        $notesMarkdown = New-ExtractionNotesMarkdown -State $state
        if ($state.Existing) {
            Update-ExistingMarkdown -Path $state.OutputPath -CommentMarkdown $commentMarkdown -NotesMarkdown $notesMarkdown -CommentCount $state.Comments.Count -ContinuationCount $state.ContinuationPages
        }
        else {
            $postMarkdown = New-PostMarkdown -State $state -CommentMarkdown $commentMarkdown -NotesMarkdown $notesMarkdown
            if ((Test-Path -LiteralPath $state.OutputPath) -and -not $Force) {
                throw "Output appeared during the run: $($state.OutputPath). Use a new RunTimestamp, StartNumber, or -Force."
            }
            Write-Utf8Atomically -Path $state.OutputPath -Content $postMarkdown
        }
        foreach ($warning in $state.Warnings) {
            Write-Warning $warning
        }
        Write-Output ("Saved {0} comments from {1} pages to {2}" -f $state.Comments.Count, $state.PageCount, $state.OutputPath)
    }
}

Write-Output ("Finished {0} Reddit post(s) in {1}." -f $rootStates.Count, $OutputDirectory)
