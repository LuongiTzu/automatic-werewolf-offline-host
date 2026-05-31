<template>
  <div class="rounded-3xl border border-amber-800 bg-amber-950/40 p-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <p class="text-sm text-amber-100">Ban ngày</p>
        <h2 class="text-3xl font-black">Trời sáng rồi</h2>
      </div>
      <CountdownTimer :ends-at="phaseEndsAt" label="Còn" />
    </div>

    <div class="mt-5 rounded-xl bg-slate-950 p-4">
      <p class="font-bold">Kết quả ban đêm</p>
      <p v-if="deadPlayers.length === 0" class="mt-2 text-green-200">Đêm qua không có ai chết.</p>
      <ul v-else class="mt-2 list-inside list-disc text-red-200">
        <li v-for="player in deadPlayers" :key="player.id">{{ player.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import CountdownTimer from '@/components/common/CountdownTimer.vue'
import type { NightTarget } from '@/types/player'

defineProps<{
  phaseEndsAt: string
  deadPlayers: NightTarget[]
}>()
</script>
