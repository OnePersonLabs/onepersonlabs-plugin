# Feedback on a running page

Use page feedback when the human needs to point at a visible control, layout,
state, or design variant. The root selects and prepares this adapter when the
authorized collaboration needs it. The human need not install an extension or
remember a command. Use ordinary inbox replies for conceptual discussion.

## Prepare the page

Enroll and connect this root through the existing human-collaboration procedure.
Use the available browser automation tool under its own access rules. Open the
paired inbox in that browser, then prepare its page-review bridge:

```javascript
window.onepersonlabsPageReview.prepare({
  url: "http://localhost:3000/checkout",
  session: "<enrolled session id>",
  sourceState: "<commit plus relevant dirty source or build identity>",
  variant: "<variant name when comparing designs>"
})
```

Get the exact session ID from `human.py list` or the inbox's enrolled sessions.
Keep the returned `channel`, `inboxOrigin`, `sourceState`, and `variant` object.
Click **Review a page** in the inbox. The named child window preserves its opener;
an unrelated tab cannot deliver the notes. Read the bundled `web/annotate.js`,
inject it into that child using supported browser automation, and call
`window.onepersonlabsAnnotate(options)` with the returned object. Do not copy the
adapter into production assets or put the inbox bearer token in the child page.
Verify that **Page feedback** is visible before inviting the human.

Use a browser surface that supports child windows and script evaluation. If the
page's opener isolation or the tool's access rules prevent attachment, use the
existing inbox with a screenshot and source context, and report that limit. Do
not weaken browser isolation or the product's security policy to attach controls.

## Capture and submit

The human pins an element, writes a note, and saves it. Each note retains the page
origin/path, timestamp, selector, text excerpt, viewport, scroll, rectangle, click
position, source state, and variant. URL query and fragment are omitted. Review
the captured context for private page text before sending it.

**Review in inbox** freezes the notes as a recoverable batch and opens an ordinary
contribution draft. The human can edit that draft and explicitly select **Send
contribution**. Only the existing authenticated contribution endpoint creates a
submission. Saving a note or moving it to the inbox does not authorize agent work.

Drafts and pending batches remain in browser storage. After a page reload, the
root reattaches `annotate.js` with the same options. After an inbox reload, click
**Review a page** to reconnect its named child, reattach the controls, then retry
**Review in inbox**. A lost HTTP response retains the frozen submission payload;
retry reconciles its request ID instead of creating another contribution. Keep
the pages open if device storage is unavailable. An acknowledged batch clears its
notes only after the inbox confirms a durable submission.

## Integrate and close

Use the ordinary `pending`, `show`, `claim`, and `outcome` protocol. Compare the
captured source state, selector, excerpt, and geometry with the current page;
selectors and coordinates are historical evidence, not instructions to click a
possibly changed element. Preserve the original note when a rerender or code
change moves its target. Inspect the matching current component before editing.

Exercise the changed page, then record what changed or why the note was not
adopted, evidence, and `source_review` in the outcome. A repeated receipt requires
checking the claim and recorded effect before applying work again. Remove the
overlay with **Hide** or `window.onepersonlabsAnnotation.close()` when finished.
