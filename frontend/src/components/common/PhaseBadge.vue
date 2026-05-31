<template>
  <span class="inline-flex rounded-full px-3 py-1 text-xs font-bold" :class="badgeClass">
    {{ phaseLabel(phase) }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { phaseLabel } from '@/types/game'

const props = defineProps<{
  phase?: string | null
}>()

const badgeClass = computed(() => {
  if (props.phase?.includes('night')) return 'bg-indigo-950 text-indigo-200'
  if (props.phase?.includes('day')) return 'bg-amber-900 text-amber-100'
  if (props.phase === 'voting') return 'bg-red-900 text-red-100'
  if (props.phase === 'ended') return 'bg-purple-900 text-purple-100'
  return 'bg-slate-800 text-slate-200'
})
</script>
