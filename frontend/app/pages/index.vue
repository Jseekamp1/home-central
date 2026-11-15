<template>
  <section aria-labelledby="projects-title" class="flex flex-col gap-5">
    <div class="flex items-center justify-between gap-3">
      <h1 id="projects-title" class="text-3xl font-bold tracking-tight">Projects</h1>
      <Button v-if="canCreate" as-child>
        <NuxtLink to="/projects/new">
          <Plus aria-hidden="true" />
          New project
        </NuxtLink>
      </Button>
    </div>

    <nav aria-label="Project views" class="grid grid-cols-3 gap-1 rounded-lg border border-border bg-card p-1">
      <NuxtLink
        v-for="tab in tabs"
        :key="tab.value"
        :to="{ query: tab.value === 'active' ? {} : { view: tab.value } }"
        :aria-current="view === tab.value ? 'page' : undefined"
        class="flex h-10 items-center justify-center rounded-md text-sm font-medium focus-visible:outline-2 focus-visible:outline-ring"
        :class="view === tab.value ? 'bg-secondary text-foreground font-semibold' : 'text-muted-foreground hover:text-foreground'"
      >
        {{ tab.label }}
      </NuxtLink>
    </nav>

    <div v-if="error" role="alert" class="flex items-center justify-between gap-3 rounded-lg border border-destructive-border bg-card px-4 py-3">
      <span class="text-sm text-destructive">{{ error }}</span>
      <Button variant="outline" size="sm" @click="reload">Try again</Button>
    </div>

    <ul v-else-if="loading && !projects.length" aria-hidden="true" class="flex flex-col gap-3">
      <li v-for="n in 3" :key="n" class="flex flex-col gap-3 rounded-xl border border-border bg-card p-4">
        <span class="h-4 w-3/5 rounded bg-secondary" />
        <span class="h-3 w-2/5 rounded bg-secondary/70" />
      </li>
    </ul>

    <div v-else-if="!projects.length" class="flex flex-col items-center gap-2 rounded-xl border border-dashed border-input px-4 py-10 text-center">
      <p class="font-semibold">{{ empty.title }}</p>
      <p class="text-sm text-muted-foreground">{{ empty.body }}</p>
      <Button v-if="view === 'active' && canCreate" as-child class="mt-2">
        <NuxtLink to="/projects/new">New project</NuxtLink>
      </Button>
    </div>

    <ul v-else class="grid gap-3 lg:grid-cols-2">
      <li v-for="project in projects" :key="project.id">
        <ProjectCard :project="project" :property="isAll ? propertyById.get(project.property_id) : null" />
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { Plus } from 'lucide-vue-next'
import { Button } from '~/shared/components/ui/button'
import ProjectCard from '~/features/projects/components/ProjectCard.vue'
import { useProjects, type ProjectScope, type ProjectView } from '~/features/projects/composables/useProjects'
import { useProperties } from '~/features/properties/composables/useProperties'

const route = useRoute()
const { properties, current, isAll } = useProperties()
const { projects, loading, error, load } = useProjects()

const tabs: { value: ProjectView, label: string }[] = [
  { value: 'active', label: 'Active' },
  { value: 'done', label: 'Done' },
  { value: 'cancelled', label: 'Cancelled' },
]

const view = computed<ProjectView>(() => {
  const requested = route.query.view
  return requested === 'done' || requested === 'cancelled' ? requested : 'active'
})

const scope = computed<ProjectScope | null>(() => {
  if (isAll.value) return { all: true }
  if (current.value) return { propertyId: current.value.id }
  return null
})

const propertyById = computed(() => new Map(properties.value.map(p => [p.id, p])))

const canCreate = computed(() => {
  if (isAll.value) return properties.value.some(p => p.my_role !== 'viewer')
  return !!current.value && current.value.my_role !== 'viewer'
})

const empty = computed(() => ({
  active: { title: 'No projects yet', body: 'Start with something small, like a filter change.' },
  done: { title: 'Nothing finished yet', body: 'Projects you mark done show up here.' },
  cancelled: { title: 'No cancelled projects', body: 'Cancelled projects show up here, in case you change your mind.' },
}[view.value]))

function reload() {
  if (scope.value) load(scope.value, view.value)
}

watch([scope, view], reload, { immediate: true, deep: true })
</script>
