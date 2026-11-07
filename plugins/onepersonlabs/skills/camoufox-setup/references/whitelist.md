# Website whitelist

## Select the mechanism

For a simple website whitelist, use the browser's supported Firefox enterprise policy or an established Firefox extension. The native [WebsiteFilter policy](https://github.com/mozilla/policy-templates/blob/master/docs/index.md#websitefilter) can block navigation by default and allow selected sites. uBlock Origin supplies separate ad blocking.

WebsiteFilter controls documents and embedded pages. It does not restrict every script, image, fetch, or other network request. It does not provide approve-once, approve-always, deny-once, or deny-always prompts. If those prompts or full request filtering are required, select a mechanism that implements them and describe its enforcement boundary.

Do not import a general adblock exception list as a website access policy. Such lists can include advertising, tracking, and referral hosts. Use a maintained list only after checking its purpose and entries against the requested access.

## Configure native policy

Store policy at `distribution/policies.json` under the actual Firefox-based browser installation directory on either Windows or Linux. If multiple installations share a cache, use an owned browser bundle to avoid changing their policies. Merge this setting with existing vendor policies:

```json
{
  "policies": {
    "WebsiteFilter": {
      "Block": ["<all_urls>"],
      "Exceptions": [
        "*://example.com/*",
        "*://*.example.com/*"
      ]
    }
  }
}
```

The second pattern allows all subdomains. Omit it when only the exact host should be allowed. Check the current policy limits and match-pattern rules before generating a large list. Restart the browser after a policy change.

Keep allowed domains in a readable configuration file. Validate each entry as a domain or host before converting it to a match pattern. Do not accept a URL, credential, port, or path as a domain entry.

## Service domains

For this user's research setup, the requested service families are Google, Microsoft, Facebook, Instagram, X, YouTube, NotebookLM, Azure, OpenAI, and `onepersonlabs.com`. Preserve additional sites already authorized for the task, such as Reddit and GitHub. Do not apply this user's choices to another user's setup without a request.

Start with the service's main domain. Add login, static asset, and content domains from current official vendor documentation or an observed blocked navigation. Examples of main roots include `google.com`, `microsoft.com`, `facebook.com`, `instagram.com`, `x.com`, `youtube.com`, `azure.com`, `openai.com`, and `chatgpt.com`. Check current NotebookLM destinations because domains and redirects can change.

Allowing all subdomains of shared hosting roots such as `github.io`, `azurewebsites.net`, or `windows.net` also permits unrelated tenant content. Use specific tenant hosts when the requested scope permits them. Do not claim that a service-family list proves who controls all allowed page content.

Use [Microsoft's endpoint documentation](https://learn.microsoft.com/microsoft-365/enterprise/urls-and-ip-address-ranges) and [OpenAI's network recommendations](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps) for relevant dependencies. Import only entries needed for the selected services and enforcement mechanism.
