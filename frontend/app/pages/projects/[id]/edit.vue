<template>
  <section aria-labelledby="edit-title" class="mx-auto flex max-w-lg flex-col gap-6">
    <h1 id="edit-title" class="text-3xl font-bold tracking-tight">Edit project</h1>
    <p v-if="loadError" role="alert" class="text-destructive">{{ loadError }}</p>
    <div v-else-if="project" class="rounded-xl border border-border bg-card p-5">
      <ProjectForm
        :initial="project"
        submit-label="Save changes"
        :busy="busy"
        :error="formError"
        :cancel-to="`/projects/${project.id}`"
        @submit="onSubmit"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import ProjectForm, { type ProjectFormValues } from '~/features/projects/components/ProjectForm.vue'
import { useProjects } from '~/features/projects/composables/useProjects'
import type { Schemas } from '~/shared/api/types'

const route = useRoute()
const { get, update, error } = useProjects()

const project = ref<Schemas['ProjectRead'] | null>(null)
const loadError = ref<string | null>(null)
const busy = ref(false)
const formError = ref<string | null>(null)

onMounted(async () => {
  project.value = await get(String(route.params.id))
  if (!project.value) loadError.value = error.value
})

async function onSubmit({ property_id: _ignored, ...body }: ProjectFormValues) {
  if (!project.value) return
  busy.value = true
  formError.value = null
  const saved = await update(project.value.id, body)
  busy.value = false
  if (!saved) {
    formError.value = error.value
    return
  }
  await navigateTo(`/projects/${saved.id}`)
}
</script>
