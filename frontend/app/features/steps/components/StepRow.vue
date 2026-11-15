<template>
  <li :data-step-id="step.id" class="flex flex-col gap-3 px-3 py-2.5">
    <div class="flex items-center gap-2">
      <label class="flex min-h-11 min-w-0 flex-1 cursor-pointer items-center gap-3" :class="{ 'cursor-default': !canEdit }">
        <input
          type="checkbox"
          class="step-check"
          :checked="!!step.done_at"
          :disabled="!canEdit"
          @change="emit('toggle', ($event.target as HTMLInputElement).checked)"
        >
        <span v-if="!renaming" class="leading-snug" :class="{ 'text-muted-foreground line-through': step.done_at }">{{ step.title }}</span>
      </label>

      <form v-if="renaming" class="flex min-w-0 flex-1 items-center gap-2" @submit.prevent="saveRename">
        <label :for="renameId" class="sr-only">Step title</label>
        <input
          :id="renameId"
          ref="renameEl"
          v-model="draftTitle"
          required
          maxlength="200"
          class="h-10 min-w-0 flex-1 rounded-md border border-input bg-inset px-3 focus-visible:outline-2 focus-visible:outline-ring"
          @keydown.esc.prevent="renaming = false"
        >
        <Button type="submit" size="sm">Save</Button>
      </form>

      <template v-if="!editing && !renaming">
        <button
          v-if="step.estimated_minutes !== null"
          type="button"
          :disabled="!canEdit"
          :aria-expanded="canEdit ? picking : undefined"
          :aria-label="`Estimate ${formatMinutes(step.estimated_minutes)}. Change estimate`"
          class="shrink-0 rounded-md bg-secondary px-2 py-1 font-mono text-xs text-foreground enabled:hover:bg-accent focus-visible:outline-2 focus-visible:outline-ring"
          @click="picking = !picking"
        >
          {{ formatMinutes(step.estimated_minutes) }}
        </button>
        <button
          v-else-if="canEdit"
          type="button"
          :aria-expanded="picking"
          class="shrink-0 rounded-md border border-dashed border-attention px-2 py-1 text-xs font-semibold text-attention hover:bg-attention/10 focus-visible:outline-2 focus-visible:outline-ring"
          @click="picking = !picking"
        >
          Add estimate
        </button>
        <span v-else class="shrink-0 text-xs font-semibold text-attention">Needs estimate</span>
      </template>

      <div v-if="editing && !renaming" class="flex shrink-0 gap-1">
        <button type="button" :data-move="-1" :disabled="index === 0" aria-label="Move step up" :class="iconButton" @click="emit('move', -1)">
          <ChevronUp class="size-4" aria-hidden="true" />
        </button>
        <button type="button" :data-move="1" :disabled="index === count - 1" aria-label="Move step down" :class="iconButton" @click="emit('move', 1)">
          <ChevronDown class="size-4" aria-hidden="true" />
        </button>
        <button type="button" aria-label="Rename step" :class="iconButton" @click="startRename">
          <Pencil class="size-4" aria-hidden="true" />
        </button>
        <button type="button" aria-label="Delete step" :class="[iconButton, 'text-destructive']" @click="emit('delete')">
          <Trash2 class="size-4" aria-hidden="true" />
        </button>
      </div>
    </div>

    <div v-if="picking" class="flex flex-col gap-3 rounded-lg bg-inset p-3">
      <EstimatePicker v-model="pending" :legend="`Estimate for ${step.title}`" />
      <div class="flex gap-2">
        <Button size="sm" @click="saveEstimate">Save estimate</Button>
        <Button size="sm" variant="ghost" @click="picking = false">Cancel</Button>
      </div>
    </div>
  </li>
</template>

<script setup lang="ts">
import { nextTick, ref, useId, watch } from 'vue'
import { ChevronDown, ChevronUp, Pencil, Trash2 } from 'lucide-vue-next'
import { Button } from '~/shared/components/ui/button'
import type { Schemas } from '~/shared/api/types'
import { formatMinutes } from '../estimates'
import EstimatePicker from './EstimatePicker.vue'

const props = defineProps<{
  step: Schemas['StepRead']
  index: number
  count: number
  editing: boolean
  canEdit: boolean
}>()

const emit = defineEmits<{
  toggle: [done: boolean]
  estimate: [minutes: number | null]
  rename: [title: string]
  move: [delta: -1 | 1]
  delete: []
}>()

const iconButton = 'flex size-10 items-center justify-center rounded-md border border-border bg-inset hover:bg-secondary disabled:opacity-40 focus-visible:outline-2 focus-visible:outline-ring'

const picking = ref(false)
const pending = ref<number | null>(props.step.estimated_minutes)

// Start each edit from the step's saved estimate.
watch(picking, (open) => {
  if (open) pending.value = props.step.estimated_minutes
})

function saveEstimate() {
  emit('estimate', pending.value)
  picking.value = false
}

const renameId = `${useId()}-rename`
const renameEl = ref<HTMLInputElement | null>(null)
const renaming = ref(false)
const draftTitle = ref('')

async function startRename() {
  draftTitle.value = props.step.title
  renaming.value = true
  await nextTick()
  renameEl.value?.select()
}

function saveRename() {
  const title = draftTitle.value.trim()
  if (title && title !== props.step.title) emit('rename', title)
  renaming.value = false
}
</script>
