<template>
  <section v-if="current" aria-labelledby="settings-title" class="mx-auto flex max-w-lg flex-col gap-6">
    <div class="flex flex-col gap-1">
      <h1 id="settings-title" class="text-3xl font-bold tracking-tight">Property settings</h1>
      <p class="text-muted-foreground">{{ current.name }} · {{ roleLabel(current.my_role) }}</p>
    </div>

    <p v-if="isViewer" class="rounded-lg border border-border bg-card px-4 py-3 text-sm text-muted-foreground">
      You can view this property, but only its owner or editors can change it.
    </p>

    <div class="rounded-xl border border-border bg-card p-5">
      <PropertyForm
        :key="current.id"
        :initial="current"
        submit-label="Save changes"
        :readonly="isViewer"
        :busy="saving"
        :error="saveError"
        @submit="onSave"
      />
      <p v-if="savedNotice" role="status" class="mt-4 text-sm text-project-time-label">{{ savedNotice }}</p>
    </div>

    <section v-if="isOwner" aria-labelledby="delete-title" class="flex flex-col gap-3 rounded-xl border border-border bg-card p-5">
      <h2 id="delete-title" class="text-lg font-semibold">Delete property</h2>
      <p class="text-sm text-muted-foreground">Removes {{ current.name }} and everything in it for everyone who has access.</p>
      <Button
        variant="outline"
        size="lg"
        class="self-start border-destructive-border text-destructive hover:bg-destructive/10 hover:text-destructive"
        @click="confirmEl?.showModal()"
      >
        Delete {{ current.name }}
      </Button>
      <p v-if="deleteError" role="alert" class="text-sm text-destructive">{{ deleteError }}</p>
    </section>

    <dialog
      ref="confirmEl"
      aria-labelledby="confirm-title"
      aria-describedby="confirm-body"
      class="m-auto w-[min(26rem,calc(100%-2rem))] rounded-2xl border border-border bg-card p-0 text-foreground"
      @close="onConfirmClose"
    >
      <form method="dialog" class="flex flex-col gap-3 p-5">
        <h2 id="confirm-title" class="text-xl font-bold">Delete {{ current.name }}?</h2>
        <p id="confirm-body" class="text-muted-foreground">
          This deletes it for everyone who has access, along with all of its projects. It can't be undone.
        </p>
        <div class="mt-2 flex gap-3">
          <Button value="keep" variant="outline" size="lg" class="flex-1" autofocus>Keep it</Button>
          <Button value="delete" size="lg" class="flex-1 bg-destructive text-primary-foreground hover:bg-destructive/90">Delete</Button>
        </div>
      </form>
    </dialog>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Button } from '~/shared/components/ui/button'
import PropertyForm from '~/features/properties/components/PropertyForm.vue'
import { useProperties } from '~/features/properties/composables/useProperties'
import { roleLabel } from '~/features/properties/kinds'
import type { Schemas } from '~/shared/api/types'

const { current, error, update, remove } = useProperties()

const isViewer = computed(() => current.value?.my_role === 'viewer')
const isOwner = computed(() => current.value?.my_role === 'owner')

const saving = ref(false)
const saveError = ref<string | null>(null)
const savedNotice = ref('')

async function onSave(values: Schemas['PropertyCreate']) {
  if (!current.value) return
  saving.value = true
  saveError.value = null
  savedNotice.value = ''
  const saved = await update(current.value.id, values)
  saving.value = false
  if (saved) savedNotice.value = 'Saved.'
  else saveError.value = error.value
}

const confirmEl = ref<HTMLDialogElement | null>(null)
const deleteError = ref<string | null>(null)

async function onConfirmClose() {
  const dialog = confirmEl.value
  if (!dialog) return
  const choice = dialog.returnValue
  // Esc and other close requests leave no value; reset so a stale one can't leak.
  dialog.returnValue = ''
  if (choice !== 'delete' || !current.value) return

  deleteError.value = null
  const removed = await remove(current.value.id)
  if (!removed) {
    deleteError.value = error.value
    return
  }
  await navigateTo('/')
}
</script>
