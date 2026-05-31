<template>
  <div class="rounded-xl border border-slate-700 bg-slate-950 p-4 text-center">
    <p class="text-sm text-slate-400">{{ label }}</p>
    <p class="mt-1 text-3xl font-black" :class="remaining <= 10 ? 'text-red-300' : 'text-white'">
      {{ remainingText }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'

const props = withDefaults(
  defineProps<{
    endsAt?: string | null
    label?: string
  }>(),
  {
    endsAt: null,
    label: 'Thời gian còn lại',
  },
)

const remaining = ref(0)
let timerId: number | null = null

function tick() {
  if (!props.endsAt) {
    remaining.value = 0
    return
  }

  const endTime = Date.parse(props.endsAt)
  if (Number.isNaN(endTime)) {
    remaining.value = 0
    return
  }

  remaining.value = Math.max(0, Math.ceil((endTime - Date.now()) / 1000))
}

function startTimer() {
  if (timerId) window.clearInterval(timerId)
  tick()
  timerId = window.setInterval(tick, 1000)
}

const remainingText = computed(() => {
  const minutes = Math.floor(remaining.value / 60)
  const seconds = remaining.value % 60
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
})

watch(() => props.endsAt, startTimer)

onMounted(startTimer)

onUnmounted(() => {
  if (timerId) window.clearInterval(timerId)
})
</script>
