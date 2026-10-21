// Inject with supported browser automation into the reviewed page, then call
// onepersonlabsAnnotate(options). No service token or network client enters it.
window.onepersonlabsAnnotate = function (options) {
  window.onepersonlabsAnnotation?.close()
  if (!window.opener || new URL(options.inboxOrigin).origin !== options.inboxOrigin) {
    throw new Error('Open this page from the human inbox before attaching feedback controls.')
  }
  const key = `onepersonlabs-page-notes:${options.channel}`
  let state = {notes: [], pending: null}, selecting = false, selected = null
  try { state = JSON.parse(localStorage.getItem(key)) || state } catch { /* New review. */ }
  const host = document.createElement('aside')
  host.id = 'onepersonlabs-page-feedback'
  host.style.cssText = 'position:fixed;right:12px;bottom:12px;z-index:2147483647;max-width:calc(100vw - 24px)'
  const root = host.attachShadow({mode: 'open'})
  root.innerHTML = `<style>
    :host{color-scheme:light;font:14px system-ui;color:#17252a}section{box-sizing:border-box;width:320px;max-width:calc(100vw - 24px);padding:14px;background:#fff;border:2px solid #16756b;border-radius:12px;box-shadow:0 8px 32px #0005}
    h2{font-size:17px;margin:0 0 8px}button,textarea{font:inherit}button{padding:7px;margin:3px;border:1px solid #16756b;border-radius:5px;background:#edf8f6;color:#17252a;cursor:pointer}textarea{box-sizing:border-box;width:100%;height:80px;margin:8px 0}p{margin:8px 0}ol{max-height:120px;overflow:auto;padding-left:24px}small{display:block}
    </style><section aria-label="Page feedback"><h2>Page feedback</h2><button id="pick">Pin an element</button><button id="close">Hide</button><p id="selected">Choose something on the page, then describe it.</p><textarea aria-label="Feedback note" placeholder="What should change, or what works?"></textarea><button id="add">Save note</button><ol></ol><button id="send">Review in inbox</button><p id="status" role="status"></p><small>Notes stay on this device until you send them from the inbox.</small></section>`
  document.documentElement.append(host)
  const $ = (selector) => root.querySelector(selector)
  selected = state.selection || null
  $('textarea').value = state.draft || ''
  if (selected) $('#selected').textContent = `Pinned: ${selected.selector}`
  const status = (message) => { $('#status').textContent = message }
  const save = () => {
    try { localStorage.setItem(key, JSON.stringify(state)); return true }
    catch { status('Device storage is unavailable. Keep this page open until submitted.'); return false }
  }
  const render = () => {
    $('ol').replaceChildren(...state.notes.map((note, index) => {
      const item = document.createElement('li'); item.textContent = note.note; return item
    }))
    $('#add').disabled = Boolean(state.pending)
    $('#send').disabled = !state.notes.length
    if (state.pending) status('Notes are retained. Review in the inbox, or retry after reconnecting.')
  }
  const selector = (element) => {
    if (element.id) return `#${CSS.escape(element.id)}`
    const parts = []
    for (let node = element; node && node !== document.documentElement && parts.length < 5; node = node.parentElement) {
      const siblings = [...node.parentElement.children].filter((other) => other.tagName === node.tagName)
      parts.unshift(`${node.localName}:nth-of-type(${siblings.indexOf(node) + 1})`)
    }
    return parts.join(' > ')
  }
  const pick = (event) => {
    if (!selecting || event.composedPath().includes(host)) return
    event.preventDefault(); event.stopImmediatePropagation(); selecting = false
    const element = event.target, rect = element.getBoundingClientRect()
    const url = new URL(location.href)
    selected = {page: url.origin + url.pathname, at: new Date().toISOString(),
      viewport: {width: innerWidth, height: innerHeight, scrollX, scrollY},
      selector: selector(element), excerpt: (element.textContent || '').trim().slice(0, 240),
      rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height},
      point: {x: event.clientX, y: event.clientY}, sourceState: options.sourceState, variant: options.variant}
    state.selection = selected; save()
    $('#selected').textContent = `Pinned: ${selected.selector}`
    $('textarea').focus()
  }
  document.addEventListener('click', pick, true)
  $('textarea').addEventListener('input', () => { state.draft = $('textarea').value; save() })
  $('#pick').onclick = () => { selecting = true; status('Click the element you want to discuss.') }
  $('#add').onclick = () => {
    const note = $('textarea').value.trim()
    if (!selected || !note) { status('Pin an element and add a note first.'); return }
    state.notes.push({...selected, note}); selected = null; state.selection = null; state.draft = ''; $('textarea').value = ''
    $('#selected').textContent = 'Choose another element to add a note.'
    const retained = save(); render()
    if (retained) status('Note saved. Add another, or review in the inbox.')
  }
  $('#send').onclick = () => {
    if (!state.pending) {
      state.pending = {id: (crypto.randomUUID?.() || Array.from(crypto.getRandomValues(new Uint8Array(16)), (byte) => byte.toString(16).padStart(2, '0')).join('')), body: '## Page feedback\n\n' + state.notes.map((note, index) =>
        `### Note ${index + 1}\n\n${note.note}\n\nCaptured context (verify against the current page):\n\n\`\`\`json\n${JSON.stringify({...note, note: undefined}, null, 2)}\n\`\`\``).join('\n\n')}
      save(); render()
    }
    window.opener.postMessage({type: 'onepersonlabs:page-notes', channel: options.channel, batch: state.pending}, options.inboxOrigin)
    window.opener.focus()
    status('Review the draft in the inbox and send it there. Retry here if the inbox was reloaded.')
  }
  const receive = (event) => {
    if (event.source !== window.opener || event.origin !== options.inboxOrigin ||
        event.data?.type !== 'onepersonlabs:page-saved' || event.data.channel !== options.channel ||
        event.data.id !== state.pending?.id) return
    state = {notes: [], pending: null}; save(); render(); status('Submitted. The agent will record an outcome in the inbox.')
  }
  window.addEventListener('message', receive)
  const close = () => { document.removeEventListener('click', pick, true); window.removeEventListener('message', receive); host.remove() }
  $('#close').onclick = close
  window.onepersonlabsAnnotation = {close}
  render()
}
