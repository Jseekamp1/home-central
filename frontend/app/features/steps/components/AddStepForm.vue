<template>
  <form class="flex flex-col gap-3 border-t border-border p-4" @submit.prevent="onSubmit">
    <div class="flex flex-col gap-1.5">
      <label :for="titleId" class="text-sm font-semibold">Add a step</label>
      <input
        :id="titleId"
        ref="titleEl"
        v-model="title"
        type="text"
        required
        maxlength="200"
        autocomplete="off"
        placeholder="e.g. Turn off the water under the sink"
        class="h-11 w-full rounded-md border border-input bg-inset px-3 text-base placeholder:text-muted-foreground focus-visible:outline-2 focus-visible:outline-ring"
      >
    </div>
    <EstimatePicker v-model="minutes" />
    <Button type="submit" variant="secondary" :disabled="busy" class="self-start">{{ busy ? 'Adding…' : 'Add step' }}</Button>
  </form>
</template>

<script setup lang="ts">
import { ref, useId } from 'vue'
import { Button } from '~/shared/components/ui/button'
import EstimatePicker from './EstimatePicker.vue'

defineProps<{ busy?: boolean }>()
const emit = defineEmits<{ add: [step: { title: string, estimated_minutes: number | null }] }>()

const titleId = `${useId()}-title`
const titleEl = ref<HTMLInputElement | null>(null)
const title = ref('')
const minutes = ref<number | null>(30)

function onSubmit() {
  const trimmed = title.value.trim()
  if (!trimmed) return
  emit('add', { title: trimmed, estimated_minutes: minutes.value })
  title.value = ''
  // Keep focus in the title field so several steps can be added in a row.
  titleEl.value?.focus()
}
</script>
