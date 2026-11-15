<template>
  <section aria-labelledby="new-title" class="mx-auto flex max-w-lg flex-col gap-6">
    <h1 id="new-title" class="text-3xl font-bold tracking-tight">New project</h1>
    <p v-if="!choices.length" class="text-muted-foreground">You can view these properties, but not add projects to them.</p>
    <div v-else class="rounded-xl border border-border bg-card p-5">
      <ProjectForm
        :initial="{ property_id: current?.id }"
        :property-choices="choices"
        submit-label="Create project"
        :busy="busy"
        :error="formError"
        cancel-to="/"
        @submit="onSubmit"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import ProjectForm, { type ProjectFormValues } from '~/features/projects/components/ProjectForm.vue'
import { useProjects } from '~/features/projects/composables/useProjects'
import { useProperties } from '~/features/properties/composables/useProperties'

const { properties, current, isAll } = useProperties()
const { create, error } = useProjects()

// In All properties you choose where the project belongs; otherwise it's the current property.
const choices = computed(() => {
  const editable = properties.value.filter(p => p.my_role !== 'viewer')
  if (isAll.value) return editable
  return editable.filter(p => p.id === current.value?.id)
})

const busy = ref(false)
const formError = ref<string | null>(null)

async function onSubmit({ property_id, ...body }: ProjectFormValues) {
  busy.value = true
  formError.value = null
  const created = await create(property_id, body)
  busy.value = false
  if (!created) {
    formError.value = error.value
    return
  }
  await navigateTo(`/projects/${created.id}`)
}
</script>
