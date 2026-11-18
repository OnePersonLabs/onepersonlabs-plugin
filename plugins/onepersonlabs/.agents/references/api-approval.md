# External API approval

Consider a credentialed external API in three cases:

- The user needs an API integration.
- The job requires its own credentials and billing.
- The task needs a specific capability available only through the API.

If the API offers no concrete advantage for the task and an existing
subscription can do the work, use the subscription without asking.

## Ask before choosing the API

Name the provider, the task or integration, the intended calls, and any expected
charges. Explain why the API is relevant now. Offer three choices, with your
recommendation first:

- Approve the named provider for the stated scope.
- Use the subscription or a concrete API-free path if one is viable. Otherwise
  offer **Explore alternatives**.
- Defer the decision.

When both paths are viable, give the tradeoff in plain language and show a
realistic case. Recommend the subscription when the API advantage is weak.
For example, a Codex session can classify a one-time batch on the subscription.
A nightly job with its own credentials sends the batch automatically and can
incur a charge each time it runs.

If the user chooses **Explore alternatives**, ask which outcomes matter most
before researching. Compare viable options against those priorities. Where
relevant, compare quality on representative inputs, minimum acceptable speed,
and cost at realistic usage levels. Label claims as measured, provider-reported,
estimated, or unknown. Offer **Back to previous question** as the last choice.
Get explicit authority for the named provider and trial scope before any paid
trial. State the expected charge or cap in that request.

An approval covers the named provider and the agreed scope. Include related calls
needed to complete that scope in the same request when they can be stated
coherently. Get separate approval for new providers or uses outside the agreed
scope. Access to credentials or a general instruction to proceed does not grant
API approval.

## Set the approval lifetime

After each provider approval, ask how long to keep it. Offer
**30 days (Recommended)** first, then **Set a specific expiry** and **Indefinite**.
Wait for the lifetime decision before making live requests. Show the exact
calendar date and time zone for the recommended expiry. Confirm
the exact cutoff chosen for any dated option. Explain that the approval permits
covered use until the cutoff and prompts again on the next use after expiry.
Indefinite approval covers the agreed scope until the user changes it.

On the next requested use after expiry, pause before the covered action. Show
when the approval expired and the requested use. Offer these four choices:

- Leave it expired for now. Covered development calls stay blocked.
- Renew for 30 days. Show the new cutoff date and time zone.
- Change the API configuration. Return to the original approval questions.
- Allow the current configuration indefinitely. Remove the development cutoff
  for the same approved scope.

Record the provider, approved scope, approval evidence, and expiry in an
existing task or project record. Record only non-secret information and keep
keys in the project's existing secret source, outside the repository.

## Keep development approval out of shipped behavior

For a dated approval, put the check in the development or evaluation entry
point before the provider call. At or after the cutoff, fail and name the
expired approval so the user can make a renewal decision. Keep the check out
of released software.
