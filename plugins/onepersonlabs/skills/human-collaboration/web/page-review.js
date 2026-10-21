// The inbox owns submission. The reviewed page can only propose a draft.
export function pageReview({button, sessions, contribute, notice}) {
  const key = 'onepersonlabs-human:page-review'
  let config, target
  try { config = JSON.parse(localStorage.getItem(key)) } catch { /* No saved review. */ }
  const save = () => {
    try { localStorage.setItem(key, JSON.stringify(config)) }
    catch { notice('Device storage is unavailable. Keep this inbox open until submitted.') }
  }
  const validUrl = (value) => {
    const url = new URL(value)
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.origin === location.origin) {
      throw new Error('Choose an HTTP page outside the inbox, without URL credentials.')
    }
    return url
  }
  const options = () => ({channel: config.channel, inboxOrigin: location.origin,
    sourceState: config.sourceState, variant: config.variant})
  const open = () => {
    if (!config) { notice('Ask the agent to prepare the page you want to review.'); return }
    validUrl(config.url)
    target = window.open(config.url, `onepersonlabs-review-${config.channel}`)
    if (!target) throw new Error('Allow this inbox to open the review page.')
    notice('The review page is open. The agent attaches its feedback controls.')
    return options()
  }
  button.addEventListener('click', () => { try { open() } catch (error) { notice(error.message) } })
  window.addEventListener('message', async (event) => {
    const data = event.data
    if (!config || !target || event.source !== target || event.origin !== new URL(config.url).origin ||
        !data || data.type !== 'onepersonlabs:page-notes' || data.channel !== config.channel) return
    const batch = data.batch
    if (!batch || typeof batch.id !== 'string' || !/^[a-zA-Z0-9-]{1,80}$/.test(batch.id) ||
        typeof batch.body !== 'string' || batch.body.length > 100000 || !batch.body.trim()) return
    const receiptKey = `onepersonlabs-human:page-receipt:${batch.id}`
    const acknowledge = () => target?.postMessage({type: 'onepersonlabs:page-saved', channel: config.channel,
      id: batch.id}, event.origin)
    try {
      let previous
      try { previous = JSON.parse(localStorage.getItem(receiptKey)) } catch { /* Retry uses server idempotency. */ }
      if (previous) {
        if (previous.body === batch.body) acknowledge()
        else notice('This feedback identifier already belongs to different notes. Keep the draft and reconnect.')
        return
      }
      // Receipt storage is a recovery hint; /api/contribute owns durable idempotency.
      await contribute({title: 'Page feedback', body: batch.body, request_id: batch.id,
        session: config.session, capture: true, onSubmitted: () => {
          try { localStorage.setItem(receiptKey, JSON.stringify({body: batch.body})) }
          catch { notice('Feedback is saved; this device could not save its recovery receipt.') }
          acknowledge()
        }})
      notice('Page notes are a draft. Review them, then send your contribution.')
    } catch (error) { notice(`Page notes remain on the reviewed page. ${error.message}`) }
  })
  return {
    prepare(input) {
      const url = validUrl(input.url)
      if (!sessions().some((session) => session.id === input.session)) throw new Error('Choose an enrolled root session.')
      // Reattachment keeps the channel, so a page reload cannot orphan saved notes.
      const same = config?.url === url.href && config?.session === input.session
      config = {url: url.href, session: input.session, channel: same ? config.channel : (crypto.randomUUID?.() || Array.from(crypto.getRandomValues(new Uint8Array(16)), (byte) => byte.toString(16).padStart(2, '0')).join('')),
        sourceState: String(input.sourceState || 'not recorded'), variant: String(input.variant || '')}
      save()
      return options()
    },
    open,
    options: () => config ? options() : null,
  }
}
