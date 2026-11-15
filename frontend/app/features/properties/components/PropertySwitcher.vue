<template>
  <div>
    <button
      type="button"
      aria-haspopup="dialog"
      :aria-label="`Current: ${triggerLabel}. Switch property`"
      class="-ml-2 flex min-h-11 items-center gap-2 rounded-md px-2 font-display text-[17px] font-semibold hover:bg-secondary focus-visible:outline-2 focus-visible:outline-ring"
      @click="open"
    >
      <PropertyDot v-if="current && hasMultiple" :color="current.my_color" />
      <Layers v-else-if="isAll" class="size-4 text-muted-foreground" aria-hidden="true" />
      {{ triggerLabel }}
      <ChevronDown class="size-4 text-muted-foreground" aria-hidden="true" />
    </button>

    <dialog
      ref="dialogEl"
      closedby="any"
      :aria-labelledby="titleId"
      class="mx-0 mt-auto mb-0 w-full max-w-full rounded-t-2xl border border-border bg-card p-0 text-foreground sm:m-auto sm:max-w-md sm:rounded-2xl"
    >
      <div class="flex flex-col gap-2 px-4 pt-3 pb-6">
        <div aria-hidden="true" class="mx-auto h-1.5 w-10 rounded-full bg-input sm:hidden" />
        <div class="flex items-center justify-between py-1">
          <h2 :id="titleId" class="text-xl font-bold">Your properties</h2>
          <form method="dialog">
            <button
              aria-label="Close"
              class="-mr-2 flex size-11 items-center justify-center rounded-md text-muted-foreground hover:bg-secondary focus-visible:outline-2 focus-visible:outline-ring"
            >
              <X class="size-5" aria-hidden="true" />
            </button>
          </form>
        </div>

        <ul class="flex flex-col gap-2">
          <li v-if="hasMultiple">
            <button
              type="button"
              :aria-current="isAll ? 'true' : undefined"
              :class="rowClass(isAll)"
              @click="choose(ALL)"
            >
              <span class="flex size-10 shrink-0 items-center justify-center rounded-md bg-card text-muted-foreground">
                <Layers class="size-5" aria-hidden="true" />
              </span>
              <span class="flex min-w-0 flex-1 flex-col">
                <span class="font-semibold">All properties</span>
                <span class="flex items-center gap-1 pt-0.5" aria-hidden="true">
                  <PropertyDot v-for="p in properties" :key="p.id" :color="p.my_color" size="sm" />
                </span>
                <span class="visually-hidden">{{ properties.length }} properties together</span>
              </span>
              <Check v-if="isAll" class="size-5 text-primary" aria-hidden="true" />
            </button>
          </li>
          <li v-for="p in properties" :key="p.id">
            <button
              type="button"
              :aria-current="p.id === current?.id ? 'true' : undefined"
              :class="rowClass(p.id === current?.id)"
              @click="choose(p.id)"
            >
              <span
                class="property-color flex size-10 shrink-0 items-center justify-center rounded-md bg-card"
                :class="{ 'text-muted-foreground': !hasMultiple }"
                :style="hasMultiple ? { color: colorVar(p.my_color) } : undefined"
              >
                <component :is="kindIcon(p.kind)" class="size-5" aria-hidden="true" />
              </span>
              <span class="flex min-w-0 flex-1 flex-col">
                <span class="truncate font-semibold">{{ p.name }}</span>
                <span class="text-sm text-muted-foreground">{{ kindLabel(p.kind) }} · {{ roleLabel(p.my_role) }}</span>
              </span>
              <Check v-if="p.id === current?.id" class="size-5 text-primary" aria-hidden="true" />
            </button>
          </li>
        </ul>

        <div class="mt-2 flex flex-col border-t border-border">
          <NuxtLink
            to="/setup"
            class="flex min-h-13 items-center gap-3 px-1 font-semibold text-primary"
            @click="close"
          >
            <Plus class="size-5" aria-hidden="true" />
            Add a property
          </NuxtLink>
          <NuxtLink
            v-if="current"
            to="/property"
            class="flex min-h-13 items-center gap-3 border-t border-border px-1 font-medium"
            @click="close"
          >
            <Settings class="size-5 text-muted-foreground" aria-hidden="true" />
            {{ current.name }} settings
          </NuxtLink>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, useId } from 'vue'
import { Building2, Check, ChevronDown, House, KeyRound, Layers, MapPin, Plus, Settings, Users, X } from 'lucide-vue-next'
import { addLightDismissFallback } from '~/shared/composables/lightDismiss'
import type { Schemas } from '~/shared/api/types'
import { ALL, useProperties } from '../composables/useProperties'
import { colorVar } from '../colors'
import { kindLabel, roleLabel } from '../kinds'
import PropertyDot from './PropertyDot.vue'

const { properties, current, isAll, hasMultiple, select } = useProperties()

const triggerLabel = computed(() => (isAll.value ? 'All properties' : current.value?.name ?? 'Choose a property'))

const titleId = `${useId()}-title`
const dialogEl = ref<HTMLDialogElement | null>(null)

let removeFallback: (() => void) | null = null
onMounted(() => {
  if (dialogEl.value) removeFallback = addLightDismissFallback(dialogEl.value)
})
onBeforeUnmount(() => removeFallback?.())

function open() {
  dialogEl.value?.showModal()
}

function close() {
  dialogEl.value?.close()
}

function choose(id: string) {
  select(id)
  close()
}

function rowClass(selected: boolean) {
  return [
    'flex w-full items-center gap-3 rounded-lg border p-3 text-left focus-visible:outline-2 focus-visible:outline-ring',
    selected ? 'border-primary bg-primary/10' : 'border-border bg-inset hover:bg-secondary',
  ]
}

function kindIcon(kind: Schemas['PropertyKind']) {
  return { home: House, rental: KeyRound, family: Users, organization: Building2, other: MapPin }[kind]
}
</script>
