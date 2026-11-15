<template>
  <form ref="formEl" class="flex flex-col gap-5" @submit.prevent="onSubmit">
    <div class="flex flex-col gap-1.5">
      <label :for="ids.name" class="text-sm font-semibold">Name</label>
      <input
        :id="ids.name"
        v-model="values.name"
        type="text"
        required
        maxlength="100"
        autocomplete="off"
        :data-error="`${ids.name}-error`"
        :readonly="readonly"
        placeholder="e.g. Our House"
        :class="fieldClass"
      >
      <span :id="`${ids.name}-error`" class="field-error text-sm text-destructive">Give the property a name.</span>
    </div>

    <div class="flex flex-col gap-1.5">
      <label :for="ids.kind" class="text-sm font-semibold">Kind</label>
      <select :id="ids.kind" v-model="values.kind" :disabled="readonly" :class="fieldClass">
        <option v-for="option in kindOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
      </select>
    </div>

    <div class="flex flex-col gap-1.5">
      <label :for="ids.postal" class="text-sm font-semibold">Postal code</label>
      <input
        :id="ids.postal"
        v-model="values.postal_code"
        type="text"
        required
        maxlength="20"
        autocomplete="postal-code"
        :data-error="`${ids.postal}-error`"
        :aria-describedby="`${ids.postal}-help`"
        :readonly="readonly"
        :class="fieldClass"
      >
      <span :id="`${ids.postal}-help`" class="text-sm text-muted-foreground">Used for seasonal timing, like when to seed the lawn.</span>
      <span :id="`${ids.postal}-error`" class="field-error text-sm text-destructive">Enter a postal code.</span>
    </div>

    <div class="flex flex-col gap-1.5">
      <label :for="ids.address" class="text-sm font-semibold">Address <span class="font-normal text-muted-foreground">(optional)</span></label>
      <input
        :id="ids.address"
        v-model="values.address_line"
        type="text"
        maxlength="200"
        autocomplete="street-address"
        :readonly="readonly"
        :class="fieldClass"
      >
    </div>

    <div class="flex flex-col gap-1.5">
      <label :for="ids.notes" class="text-sm font-semibold">Notes <span class="font-normal text-muted-foreground">(optional)</span></label>
      <textarea
        :id="ids.notes"
        v-model="values.notes"
        rows="3"
        maxlength="2000"
        :readonly="readonly"
        :class="[fieldClass, 'min-h-24 py-2.5 resize-y']"
      />
    </div>

    <p v-if="error" role="alert" class="rounded-md border border-destructive-border bg-inset px-3 py-2.5 text-sm text-destructive">{{ error }}</p>

    <div v-if="!readonly" class="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
      <Button v-if="cancelTo" as-child variant="outline" size="lg">
        <NuxtLink :to="cancelTo">Cancel</NuxtLink>
      </Button>
      <Button type="submit" size="lg" :disabled="busy">{{ busy ? 'Saving…' : submitLabel }}</Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, ref, useId } from 'vue'
import { Button } from '~/shared/components/ui/button'
import { attachAccessibleValidation } from '~/shared/composables/accessibleValidation'
import type { Schemas } from '~/shared/api/types'
import { kindOptions } from '../kinds'

type PropertyCreate = Schemas['PropertyCreate']

const props = withDefaults(defineProps<{
  initial?: Partial<PropertyCreate>
  submitLabel?: string
  busy?: boolean
  error?: string | null
  readonly?: boolean
  cancelTo?: string
}>(), {
  submitLabel: 'Save',
  busy: false,
  error: null,
  readonly: false,
  cancelTo: undefined,
})

const emit = defineEmits<{ submit: [values: PropertyCreate] }>()

const uid = useId()
const ids = {
  name: `${uid}-name`,
  kind: `${uid}-kind`,
  postal: `${uid}-postal`,
  address: `${uid}-address`,
  notes: `${uid}-notes`,
}

const fieldClass = 'h-11 w-full rounded-md border border-input bg-inset px-3 text-base text-foreground placeholder:text-muted-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring read-only:opacity-80'

const values = reactive({
  name: props.initial?.name ?? '',
  kind: props.initial?.kind ?? 'home',
  postal_code: props.initial?.postal_code ?? '',
  address_line: props.initial?.address_line ?? '',
  notes: props.initial?.notes ?? '',
})

const formEl = ref<HTMLFormElement | null>(null)
let detach: (() => void) | null = null
onMounted(() => {
  if (formEl.value) detach = attachAccessibleValidation(formEl.value)
})
onBeforeUnmount(() => detach?.())

function onSubmit() {
  emit('submit', {
    name: values.name.trim(),
    kind: values.kind,
    postal_code: values.postal_code.trim(),
    address_line: values.address_line.trim() || null,
    notes: values.notes.trim() || null,
  })
}
</script>
