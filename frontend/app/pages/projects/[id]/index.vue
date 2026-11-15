<template>
  <section class="mx-auto flex max-w-2xl flex-col gap-5">
    <NuxtLink to="/" class="-ml-2 flex min-h-11 items-center gap-1 self-start rounded-md px-2 text-muted-foreground hover:text-foreground">
      <ChevronLeft class="size-5" aria-hidden="true" />
      Projects
    </NuxtLink>

    <p v-if="loadError" role="alert" class="text-destructive">{{ loadError }}</p>

    <template v-else-if="project">
      <header class="flex flex-col gap-3">
        <h1 class="text-3xl leading-tight font-bold tracking-tight">{{ project.title }}</h1>
        <div class="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-muted-foreground">
          <StatusBadge :status="project.status" />
          <PriorityLabel :priority="project.priority" />
          <span v-if="due" :class="{ 'font-semibold text-attention': due.overdue }">{{ due.text }}</span>
          <span v-if="property && hasMultiple" class="flex items-center gap-1.5 text-foreground">
            <PropertyDot :color="property.my_color" size="sm" />
            {{ property.name }}
          </span>
        </div>
      </header>

      <p v-if="project.description" class="whitespace-pre-line rounded-xl border border-border bg-card p-4 text-muted-foreground">{{ project.description }}</p>

      <div v-if="notice" role="status" class="flex items-center justify-between gap-3 rounded-lg border border-primary/50 bg-primary/10 px-3 py-2.5 text-sm">
        <span>{{ notice }}</span>
        <Button v-if="undoAction" variant="outline" size="sm" @click="runUndo">Undo</Button>
      </div>

      <p v-if="actionError" role="alert" class="rounded-lg border border-destructive-border bg-card px-3 py-2.5 text-sm text-destructive">{{ actionError }}</p>

      <div v-if="allStepsDone && canEdit" class="flex flex-col gap-3 rounded-xl border border-primary bg-card p-4">
        <p class="font-semibold">All steps done. Mark the project done?</p>
        <Button class="self-start" @click="setStatus('done', 'Project done.', true)">Mark done</Button>
      </div>

      <section aria-label="Time" class="flex flex-wrap items-baseline gap-x-3 gap-y-1 rounded-xl border border-border bg-card p-4">
        <span class="font-display text-2xl font-bold">{{ project.estimated_minutes ? `≈ ${formatMinutes(project.estimated_minutes)}` : 'No estimates yet' }}</span>
        <span v-if="project.unestimated_step_count" class="text-sm font-medium text-attention">
          + {{ project.unestimated_step_count }} {{ project.unestimated_step_count === 1 ? 'step needs' : 'steps need' }} an estimate
        </span>
      </section>

      <p v-if="!canEdit" class="rounded-lg border border-border bg-card px-4 py-3 text-sm text-muted-foreground">
        You can follow this project, but only the property's owner or editors can change it.
      </p>

      <section v-else-if="project.status === 'cancelled'" aria-label="Status" class="flex flex-col items-start gap-3 rounded-xl border border-border bg-card p-4">
        <p class="text-muted-foreground">This project is cancelled.</p>
        <Button variant="outline" @click="setStatus('draft', 'Reopened as a draft.')">Reopen</Button>
      </section>

      <section v-else aria-label="Status" class="flex flex-col gap-2 rounded-xl border border-border bg-card p-4">
        <label :for="statusId" class="text-sm font-semibold">Status</label>
        <select
          :id="statusId"
          :value="project.status"
          :aria-describedby="`${statusId}-help`"
          class="h-11 w-full rounded-md border border-input bg-inset px-3 text-base focus-visible:outline-2 focus-visible:outline-ring sm:max-w-xs"
          @change="onStatusChange"
        >
          <option value="draft">Draft</option>
          <option value="ready" :disabled="!!blocker">{{ blocker ? 'Ready (not yet)' : 'Ready' }}</option>
          <option value="in_progress">In progress</option>
          <option value="done">Done</option>
        </select>
        <p :id="`${statusId}-help`" class="text-sm" :class="blocker && project.status !== 'ready' ? 'text-attention' : 'text-muted-foreground'">
          <template v-if="blocker && project.status !== 'ready'">Not ready to schedule: {{ blocker }}</template>
          <template v-else>Ready means it can be scheduled.</template>
        </p>
      </section>

      <StepList :project="project" :can-edit="canEdit" @change="onStepsChange" @notice="showNotice" />

      <div v-if="canEdit" class="flex flex-wrap gap-3 border-t border-border pt-5">
        <Button as-child variant="outline">
          <NuxtLink :to="`/projects/${project.id}/edit`">Edit details</NuxtLink>
        </Button>
        <Button v-if="project.status !== 'cancelled'" variant="outline" @click="setStatus('cancelled', 'Project cancelled.', true)">Cancel project</Button>
        <Button
          variant="outline"
          class="border-destructive-border text-destructive hover:bg-destructive/10 hover:text-destructive"
          @click="confirmEl?.showModal()"
        >
          Delete
        </Button>
      </div>

      <dialog
        ref="confirmEl"
        aria-labelledby="delete-project-title"
        aria-describedby="delete-project-body"
        class="m-auto w-[min(26rem,calc(100%-2rem))] rounded-2xl border border-border bg-card p-0 text-foreground"
        @close="onConfirmClose"
      >
        <form method="dialog" class="flex flex-col gap-3 p-5">
          <h2 id="delete-project-title" class="text-xl font-bold">Delete "{{ project.title }}"?</h2>
          <p id="delete-project-body" class="text-muted-foreground">
            This deletes it and its {{ project.step_count }} {{ project.step_count === 1 ? 'step' : 'steps' }} for everyone who shares this property. If you might want it back, cancel it instead.
          </p>
          <div class="mt-2 flex gap-3">
            <Button value="keep" variant="outline" size="lg" class="flex-1" autofocus>Keep it</Button>
            <Button value="delete" size="lg" class="flex-1 bg-destructive text-primary-foreground hover:bg-destructive/90">Delete</Button>
          </div>
        </form>
      </dialog>
    </template>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, useId } from 'vue'
import { ChevronLeft } from 'lucide-vue-next'
import { Button } from '~/shared/components/ui/button'
import type { Schemas } from '~/shared/api/types'
import PropertyDot from '~/features/properties/components/PropertyDot.vue'
import { useProperties } from '~/features/properties/composables/useProperties'
import PriorityLabel from '~/features/projects/components/PriorityLabel.vue'
import StatusBadge from '~/features/projects/components/StatusBadge.vue'
import { useProjects, viewOf } from '~/features/projects/composables/useProjects'
import { dueLabel, localToday } from '~/features/projects/dueDates'
import { statusLabels } from '~/features/projects/labels'
import StepList from '~/features/steps/components/StepList.vue'
import { formatMinutes, readyBlocker } from '~/features/steps/estimates'

type ProjectStatus = Schemas['ProjectStatus']
type ProjectDetail = Schemas['ProjectDetail']

const route = useRoute()
const { properties, hasMultiple } = useProperties()
const { get, update, remove, error } = useProjects()

const project = ref<ProjectDetail | null>(null)
const loadError = ref<string | null>(null)
const actionError = ref<string | null>(null)
const statusId = `${useId()}-status`

const property = computed(() => properties.value.find(p => p.id === project.value?.property_id) ?? null)
const canEdit = computed(() => !!project.value && project.value.my_role !== 'viewer')
const blocker = computed(() => (project.value ? readyBlocker(project.value) : null))
const due = computed(() => project.value
  ? dueLabel(project.value.due_date, localToday(), viewOf(project.value.status) === 'active')
  : null)
const allStepsDone = computed(() => {
  const p = project.value
  return !!p && p.step_count > 0 && p.done_step_count === p.step_count && p.status !== 'done' && p.status !== 'cancelled'
})

onMounted(async () => {
  project.value = await get(String(route.params.id))
  if (!project.value) loadError.value = error.value
})

// One status line for the page: the latest thing that happened, with Undo when it can be undone.
const notice = ref('')
const undoAction = ref<(() => void) | null>(null)

function showNotice(message: string, undo?: () => void) {
  notice.value = message
  undoAction.value = undo ?? null
}

function runUndo() {
  const action = undoAction.value
  undoAction.value = null
  notice.value = ''
  action?.()
}

function onStepsChange(saved: ProjectDetail) {
  project.value = saved
  actionError.value = null
}

async function setStatus(status: ProjectStatus, message: string, undoable = false) {
  if (!project.value) return false
  const previous = project.value.status
  actionError.value = null
  const saved = await update(project.value.id, { status })
  if (!saved) {
    actionError.value = error.value
    return false
  }
  project.value = saved
  showNotice(message, undoable ? () => setStatus(previous, `Restored to ${statusLabels[previous]}.`) : undefined)
  return true
}

async function onStatusChange(event: Event) {
  const select = event.target as HTMLSelectElement
  const next = select.value as ProjectStatus
  const ok = await setStatus(next, `Status changed to ${statusLabels[next]}.`)
  // Put the control back if the change was refused.
  if (!ok && project.value) select.value = project.value.status
}

const confirmEl = ref<HTMLDialogElement | null>(null)

async function onConfirmClose() {
  const dialog = confirmEl.value
  if (!dialog || !project.value) return
  const choice = dialog.returnValue
  // Esc and other close requests leave no value; reset so a stale one can't leak.
  dialog.returnValue = ''
  if (choice !== 'delete') return
  if (await remove(project.value.id)) await navigateTo('/')
  else actionError.value = error.value
}
</script>
