<template>
  <div class="rounded-3xl border border-red-800 bg-red-950/50 p-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <p class="text-sm text-red-100">Vote</p>
        <h2 class="text-3xl font-black">Bỏ phiếu treo cổ</h2>
      </div>
      <CountdownTimer :ends-at="phaseEndsAt" label="Còn" />
    </div>

    <div class="mt-6 grid gap-3 sm:grid-cols-2">
      <button
        v-for="target in targets"
        :key="target.id"
        class="rounded-xl bg-slate-950/80 px-4 py-4 text-left font-bold hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
        :disabled="target.id === playerId"
        @click="$emit('vote', target.id)"
      >
        {{ target.name }}
      </button>
    </div>

    <div v-if="summary" class="mt-5 rounded-xl bg-slate-950 p-4">
      <p class="font-bold">Đã vote: {{ summary.total_votes }} / {{ summary.total_alive }}</p>
      <div class="mt-3 space-y-2">
        <div v-for="item in summary.ranking" :key="item.player_id" class="flex justify-between text-sm">
          <span>{{ item.player_name }}</span>
          <b>{{ item.votes }} phiếu</b>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import CountdownTimer from '@/components/common/CountdownTimer.vue'
import type { VoteSummary } from '@/types/game'
import type { NightTarget } from '@/types/player'

defineProps<{
  targets: NightTarget[]
  playerId: string
  phaseEndsAt: string
  summary: VoteSummary | null
}>()

defineEmits<{
  vote: [targetId: string]
}>()
</script>
