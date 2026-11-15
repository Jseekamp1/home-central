<template>
  <div>
    <button
      type="button"
      aria-haspopup="dialog"
      :aria-label="`Current property: ${current?.name ?? 'none'}. Switch property`"
      class="-ml-2 flex min-h-11 items-center gap-1.5 rounded-md px-2 font-display text-[17px] font-semibold hover:bg-secondary focus-visible:outline-2 focus-visible:outline-ring"
      @click="open"
    >
      {{ current?.name ?? 'Choose a property' }}
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
          <li v-for="p in properties" :key="p.id">
            <button
              type="button"
              :aria-current="p.id === current?.id ? 'true' : undefined"
              class="flex w-full items-center gap-3 rounded-lg border p-3 text-left focus-visible:outline-2 focus-visible:outline-ring"
              :class="p.id === current?.id ? 'border-primary bg-primary/10' : 'border-border bg-inset hover:bg-secondary'"
              @click="choose(p.id)"
            >
              <span class="flex size-10 shrink-0 items-center justify-center rounded-md bg-card" :class="p.id === current?.id ? 'text-primary' : 'text-muted-foreground'">
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
import { onBeforeUnmount, onMounted, ref, useId } from 'vue'
import { Building2, Check, ChevronDown, House, KeyRound, MapPin, Plus, Settings, Users, X } from 'lucide-vue-next'
import { addLightDismissFallback } from '~/shared/composables/lightDismiss'
import type { Schemas } from '~/shared/api/types'
import { useProperties } from '../composables/useProperties'
import { kindLabel, roleLabel } from '../kinds'

const { properties, current, select } = useProperties()

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

function kindIcon(kind: Schemas['PropertyKind']) {
  return { home: House, rental: KeyRound, family: Users, organization: Building2, other: MapPin }[kind]
}
</script>
