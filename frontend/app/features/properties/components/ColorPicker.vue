<template>
  <fieldset class="flex flex-col gap-3">
    <legend class="mb-1 text-sm font-semibold">{{ legend }}</legend>
    <div class="grid grid-cols-4 gap-2 sm:grid-cols-8">
      <label
        v-for="option in colorOptions"
        :key="option.value"
        class="flex cursor-pointer flex-col items-center gap-1.5 rounded-lg p-1.5 text-xs text-muted-foreground has-[:checked]:text-foreground has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-ring"
      >
        <input
          type="radio"
          :name="name"
          :value="option.value"
          :checked="modelValue === option.value"
          :disabled="disabled"
          class="peer sr-only"
          @change="emit('update:modelValue', option.value)"
        >
        <span
          aria-hidden="true"
          class="property-color size-9 rounded-full outline-2 outline-offset-2 outline-transparent peer-checked:outline-foreground"
          :style="{ backgroundColor: colorVar(option.value) }"
        />
        {{ option.label }}
      </label>
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { useId } from 'vue'
import type { Schemas } from '~/shared/api/types'
import { colorOptions, colorVar } from '../colors'

withDefaults(defineProps<{
  modelValue: Schemas['PropertyColor']
  legend?: string
  disabled?: boolean
}>(), { legend: 'Your color', disabled: false })

const emit = defineEmits<{ 'update:modelValue': [value: Schemas['PropertyColor']] }>()

const name = `${useId()}-color`
</script>
