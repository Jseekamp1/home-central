/**
 * Keeps screen-reader state in step with what the user sees: a field is announced as
 * invalid only once it visibly is (:user-invalid), never on page load.
 *
 * Usage: give each field `data-error="<id of its error text>"`, then call
 * `attachAccessibleValidation(formElement)` once the form is in the page and call the
 * returned function to detach. Based on Modern Web Guidance "accessible-error-announcement".
 */
export function attachAccessibleValidation(form: HTMLFormElement): () => void {
  const announcer = document.createElement('div')
  announcer.setAttribute('aria-live', 'polite')
  announcer.className = 'visually-hidden'
  document.body.append(announcer)

  let announceTimer: ReturnType<typeof setTimeout> | undefined
  let announcedField: Element | null = null
  const flagged = new WeakSet<Element>()
  const announced = new WeakSet<Element>()

  const isField = (el: EventTarget | null): el is HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement =>
    el instanceof HTMLElement && el.matches('input, select, textarea')

  // List the error text in aria-describedby only while it's shown: referenced text is
  // announced even when hidden.
  const linkError = (el: HTMLElement, shown: boolean) => {
    const errorId = el.dataset.error
    if (!errorId) return
    const ids = (el.getAttribute('aria-describedby') ?? '').split(/\s+/).filter(id => id && id !== errorId)
    if (shown) ids.push(errorId)
    if (ids.length) el.setAttribute('aria-describedby', ids.join(' '))
    else el.removeAttribute('aria-describedby')
  }

  const announceError = (el: HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement) => {
    const error = el.dataset.error ? document.getElementById(el.dataset.error) : null
    if (!error) return
    const label = el.labels?.[0]?.textContent?.replace(/\s+/g, ' ').trim()
    clearTimeout(announceTimer)
    announcer.textContent = ''
    announcedField = el
    // Wait until the screen reader has announced the field that receives focus next.
    announceTimer = setTimeout(() => {
      announcer.textContent = (label ? `${label}: ` : '') + (error.textContent ?? '').replace(/\s+/g, ' ').trim()
    }, 500)
  }

  const sync = (target: EventTarget | null, announce = false) => {
    if (!isField(target)) return
    const invalid = target.matches(':user-invalid')
    if (invalid) {
      if (announce && !announced.has(target)) {
        announceError(target)
        announced.add(target)
      }
      target.setAttribute('aria-invalid', 'true')
      linkError(target, true)
      flagged.add(target)
    }
    else if (flagged.has(target) || target.getAttribute('aria-invalid') !== 'true') {
      target.setAttribute('aria-invalid', 'false')
      linkError(target, false)
      flagged.delete(target)
      announced.delete(target)
      if (announcedField === target) {
        clearTimeout(announceTimer)
        announcer.textContent = ''
      }
    }
  }

  form.querySelectorAll('input, select, textarea').forEach(el => sync(el))

  const onBlur = (e: Event) => sync(e.target, true)
  const onInput = (e: Event) => {
    if (e.target instanceof HTMLElement && e.target.hasAttribute('aria-invalid')) sync(e.target)
  }
  const onChange = (e: Event) => sync(e.target, true)
  // A failed submit fires 'invalid' on each failing field; focus moving to the first one
  // announces it, so these are not announced again.
  const onInvalid = (e: Event) => {
    if (e.target instanceof Element) announced.add(e.target)
    sync(e.target)
  }

  form.addEventListener('blur', onBlur, true)
  form.addEventListener('input', onInput)
  form.addEventListener('change', onChange, true)
  form.addEventListener('invalid', onInvalid, true)

  return () => {
    clearTimeout(announceTimer)
    form.removeEventListener('blur', onBlur, true)
    form.removeEventListener('input', onInput)
    form.removeEventListener('change', onChange, true)
    form.removeEventListener('invalid', onInvalid, true)
    announcer.remove()
  }
}
