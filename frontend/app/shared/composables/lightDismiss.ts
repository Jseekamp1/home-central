/**
 * Close a modal <dialog closedby="any"> when the user taps outside it, in browsers that
 * don't support `closedby` yet (Safari). Elsewhere the attribute does this natively.
 * Based on Modern Web Guidance "dialog" / "light-dismiss-a-dialog".
 */
export function addLightDismissFallback(dialog: HTMLDialogElement): () => void {
  if ('closedBy' in HTMLDialogElement.prototype) return () => {}

  // Test the pointer position, not the event target: the dialog is also the target for
  // its own padding, so a target check would close on those taps.
  const outside = (e: PointerEvent) => {
    const r = dialog.getBoundingClientRect()
    return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom
  }
  let pressedOutside = false
  const onDown = (e: PointerEvent) => { pressedOutside = outside(e) }
  // Require press and release outside, so a text-selection drag ending on the backdrop doesn't close it.
  const onUp = (e: PointerEvent) => { if (pressedOutside && outside(e)) dialog.close() }

  dialog.addEventListener('pointerdown', onDown)
  dialog.addEventListener('pointerup', onUp)
  return () => {
    dialog.removeEventListener('pointerdown', onDown)
    dialog.removeEventListener('pointerup', onUp)
  }
}
