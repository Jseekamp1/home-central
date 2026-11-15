<template>
  <form ref="formEl" class="flex flex-col gap-5" @submit.prevent="onSubmit">
    <div v-if="propertyChoices.length > 1" class="flex flex-col gap-1.5">
      <label :for="ids.property" class="text-sm font-semibold">Property</label>
      <select :id="ids.property" v-model="values.property_id" required :class="fieldClass">
        <option v-for="p in propertyChoices" :key="p.id" :value="p.id">{{ p.name }}</option>
      </select>
    </div>

    <div class="flex flex-col gap-1.5">
      <label :for="ids.title" class="text-sm font-semibold">Title</label>
      <input
        :id="ids.title"
        v-model="values.title"
        type="text"
        required
        maxlength="200"
        autocomplete="off"
        :data-error="`${ids.title}-error`"
        placeholder="e.g. Replace kitchen faucet"
        :class="fieldClass"
      >
      <span :id="`${ids.title}-error`" class="field-error text-sm text-destructive">Give the project a title.</span>
    </div>

    <div class="flex flex-col gap-1.5">
      <label :for="ids.description" class="text-sm font-semibold">Description <span class="font-normal text-muted-foreground">(optional)</span></label>
      <textarea
        :id="ids.description"
        v-model="values.description"
        rows="3"
        maxlength="5000"
        :class="[fieldClass, 'min-h-24 resize-y py-2.5']"
      />
    </div>

    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
      <div class="flex flex-col gap-1.5">
        <label :for="ids.priority" class="text-sm font-semibold">Priority</label>
        <select :id="ids.priority" v-model="values.priority" :class="fieldClass">
          <option v-for="option in priorityOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1.5">
        <label :for="ids.due" class="text-sm font-semibold">Due date <span class="font-normal text-muted-foreground">(optional)</span></label>
        <input :id="ids.due" v-model="values.due_date" type="date" :class="fieldClass">
      </div>
    </div>

    <p v-if="error" role="alert" class="rounded-md border border-destructive-border bg-inset px-3 py-2.5 text-sm text-destructive">{{ error }}</p>

    <div class="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
      <Button as-child variant="outline" size="lg">
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
import { priorityOptions } from '../labels'

type ProjectCreate = Schemas['ProjectCreate']

export interface ProjectFormValues extends ProjectCreate {
  property_id: string
}

const props = withDefaults(defineProps<{
  initial?: Partial<ProjectFormValues>
  /** Properties the project could belong to; a picker appears when there's more than one. */
  propertyChoices?: Schemas['PropertyRead'][]
  submitLabel?: string
  busy?: boolean
  error?: string | null
  cancelTo: string
}>(), {
  initial: undefined,
  propertyChoices: () => [],
  submitLabel: 'Save',
  busy: false,
  error: null,
})

const emit = defineEmits<{ submit: [values: ProjectFormValues] }>()

const uid = useId()
const ids = {
  property: `${uid}-property`,
  title: `${uid}-title`,
  description: `${uid}-description`,
  priority: `${uid}-priority`,
  due: `${uid}-due`,
}

const fieldClass = 'h-11 w-full rounded-md border border-input bg-inset px-3 text-base text-foreground placeholder:text-muted-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring'

const values = reactive({
  property_id: props.initial?.property_id ?? props.propertyChoices[0]?.id ?? '',
  title: props.initial?.title ?? '',
  description: props.initial?.description ?? '',
  priority: props.initial?.priority ?? 'medium',
  due_date: props.initial?.due_date ?? '',
})

const formEl = ref<HTMLFormElement | null>(null)
let detach: (() => void) | null = null
onMounted(() => {
  if (formEl.value) detach = attachAccessibleValidation(formEl.value)
})
onBeforeUnmount(() => detach?.())

function onSubmit() {
  emit('submit', {
    property_id: values.property_id,
    title: values.title.trim(),
    description: values.description.trim() || null,
    priority: values.priority,
    due_date: values.due_date || null,
  })
}
</script>
