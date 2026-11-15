<template>
  <fieldset class="flex flex-col gap-2">
    <legend class="mb-1.5 text-sm font-semibold">{{ legend }}</legend>
    <div class="flex flex-wrap gap-1.5">
      <button
        v-for="pick in estimatePicks"
        :key="pick.label"
        type="button"
        :aria-pressed="!custom && modelValue === pick.minutes ? 'true' : 'false'"
        :class="chipClass(!custom && modelValue === pick.minutes)"
        @click="choose(pick.minutes)"
      >
        {{ pick.label }}
      </button>
      <button type="button" :aria-pressed="custom ? 'true' : 'false'" :class="chipClass(custom)" @click="custom = true">
        Custom
      </button>
    </div>
    <div v-if="custom" class="flex items-center gap-2">
      <label :for="customId" class="text-sm text-muted-foreground">Minutes</label>
      <input
        :id="customId"
        type="number"
        inputmode="numeric"
        min="1"
        max="10080"
        step="5"
        :value="modelValue ?? ''"
        class="h-10 w-28 rounded-md border border-input bg-inset px-3 text-base focus-visible:outline-2 focus-visible:outline-ring"
        @input="onCustom"
      >
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { ref, useId } from 'vue'
import { estimatePicks } from '../estimates'

const props = withDefaults(defineProps<{ modelValue: number | null, legend?: string }>(), { legend: 'Time estimate' })
const emit = defineEmits<{ 'update:modelValue': [value: number | null] }>()

const customId = `${useId()}-custom`
const isPreset = estimatePicks.some(p => p.minutes === props.modelValue)
const custom = ref(props.modelValue !== null && !isPreset)

function choose(minutes: number | null) {
  custom.value = false
  emit('update:modelValue', minutes)
}

function onCustom(event: Event) {
  const value = (event.target as HTMLInputElement).valueAsNumber
  emit('update:modelValue', Number.isFinite(value) && value > 0 ? Math.round(value) : null)
}

function chipClass(on: boolean) {
  return [
    'min-h-9 rounded-md border px-3 text-sm font-medium focus-visible:outline-2 focus-visible:outline-ring',
    on ? 'border-primary bg-primary text-primary-foreground' : 'border-input bg-inset text-foreground hover:bg-secondary',
  ]
}
</script>
