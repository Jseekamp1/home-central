<template>
  <section aria-labelledby="steps-title" class="flex flex-col gap-3">
    <div class="flex items-center justify-between gap-3">
      <h2 id="steps-title" class="text-sm font-semibold tracking-wide text-muted-foreground uppercase">
        Steps · {{ project.done_step_count }} of {{ project.step_count }}
      </h2>
      <Button
        v-if="canEdit && project.steps.length > 1"
        variant="outline"
        size="sm"
        :aria-pressed="editing ? 'true' : 'false'"
        @click="editing = !editing"
      >
        {{ editing ? 'Done editing' : 'Edit steps' }}
      </Button>
    </div>

    <p v-if="!project.steps.length" class="rounded-xl border border-dashed border-input px-4 py-6 text-center text-sm text-muted-foreground">
      No steps yet. Break the work into steps with time estimates so it can be scheduled.
    </p>

    <ol v-else ref="listEl" class="flex flex-col divide-y divide-border rounded-xl border border-border bg-card">
      <StepRow
        v-for="(step, index) in project.steps"
        :key="step.id"
        :step="step"
        :index="index"
        :count="project.steps.length"
        :editing="editing"
        :can-edit="canEdit"
        @toggle="onToggle(step.id, $event)"
        @estimate="run(steps.update(project, step.id, { estimated_minutes: $event }))"
        @rename="run(steps.update(project, step.id, { title: $event }))"
        @move="onMove(step, $event)"
        @delete="onDelete(step, index)"
      />
    </ol>

    <p v-if="steps.error.value" role="alert" class="text-sm text-destructive">{{ steps.error.value }}</p>
    <p ref="announcer" role="status" class="sr-only" />

    <AddStepForm v-if="canEdit" :busy="adding" @add="onAdd" />
  </section>
</template>

<script setup lang="ts">
import { nextTick, ref } from 'vue'
import { Button } from '~/shared/components/ui/button'
import type { Schemas } from '~/shared/api/types'
import { useSteps } from '../composables/useSteps'
import AddStepForm from './AddStepForm.vue'
import StepRow from './StepRow.vue'

type ProjectDetail = Schemas['ProjectDetail']
type Step = Schemas['StepRead']

const props = defineProps<{ project: ProjectDetail, canEdit: boolean }>()
const emit = defineEmits<{
  change: [project: ProjectDetail]
  /** A short message for the page's status line, with an optional undo. */
  notice: [message: string, undo?: () => void]
}>()

const steps = useSteps()
const editing = ref(false)
const adding = ref(false)
const listEl = ref<HTMLOListElement | null>(null)
const announcer = ref<HTMLParagraphElement | null>(null)

async function run(request: Promise<ProjectDetail | null>) {
  const saved = await request
  if (saved) emit('change', saved)
  return saved
}

async function onAdd(body: { title: string, estimated_minutes: number | null }) {
  adding.value = true
  // Scheduling rules get their own controls in Milestone 6; new steps start with none.
  await run(steps.add(props.project, { ...body, wait_after_minutes: 0, keep_with_next: false }))
  adding.value = false
}

async function onToggle(stepId: string, done: boolean) {
  const result = await steps.setDone(props.project, stepId, done)
  if (!result) return
  emit('change', result.project)
  if (result.started) emit('notice', 'Moved to In progress.')
}

async function onMove(step: Step, delta: -1 | 1) {
  const saved = await run(steps.move(props.project, step.id, delta))
  if (!saved) return
  const position = saved.steps.findIndex(s => s.id === step.id) + 1
  // Moving the row in the DOM drops focus; put it back on the button that was
  // pressed, or the other one if this step reached the end of the list.
  await nextTick()
  const row = listEl.value?.querySelector<HTMLElement>(`[data-step-id="${step.id}"]`)
  const pressed = row?.querySelector<HTMLButtonElement>(`[data-move="${delta}"]`)
  const fallback = row?.querySelector<HTMLButtonElement>(`[data-move="${-delta}"]`)
  ;(pressed && !pressed.disabled ? pressed : fallback)?.focus()
  // One announcement for the whole move, not one per item that shifted.
  if (announcer.value) announcer.value.textContent = `Moved "${step.title}" to position ${position} of ${saved.steps.length}.`
}

async function onDelete(step: Step, index: number) {
  const saved = await run(steps.remove(props.project, step.id))
  if (!saved) return
  emit('notice', `Deleted "${step.title}".`, () => restore(step, index))
}

// Undo a delete: add the step back, then put it where it was.
async function restore(step: Step, index: number) {
  const added = await steps.add(props.project, {
    title: step.title,
    details: step.details,
    estimated_minutes: step.estimated_minutes,
    wait_after_minutes: step.wait_after_minutes,
    keep_with_next: step.keep_with_next,
  })
  if (!added) return
  const restoredId = added.steps[added.steps.length - 1]!.id
  const ids = added.steps.map(s => s.id).filter(id => id !== restoredId)
  ids.splice(index, 0, restoredId)
  const reordered = await steps.reorder(added, ids)
  emit('change', reordered ?? added)
  if (step.done_at && reordered) await run(steps.update(reordered, restoredId, { done: true }))
}
</script>
