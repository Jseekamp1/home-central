<template>
  <span
    aria-hidden="true"
    class="property-color inline-block shrink-0 rounded-full"
    :class="size === 'sm' ? 'size-2.5' : 'size-3'"
    :style="{ backgroundColor: colorVar(color) }"
  />
</template>

<script setup lang="ts">
import type { Schemas } from '~/shared/api/types'
import { colorVar } from '../colors'

// Decorative: the property's name is always shown or announced next to it.
withDefaults(defineProps<{ color: Schemas['PropertyColor'], size?: 'sm' | 'md' }>(), { size: 'md' })
</script>
