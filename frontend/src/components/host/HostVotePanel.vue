<template>
  <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
    <h3 class="text-xl font-bold">Vote realtime</h3>

    <div v-if="!voteStarted" class="mt-4 text-sm text-slate-400">
      Vote chưa bắt đầu.
    </div>

    <div v-else class="mt-4 space-y-4">
      <div class="rounded-xl bg-slate-950 p-4">
        <p class="text-sm text-slate-400">Ngày {{ voteStarted.day_number }}</p>
        <p class="text-lg font-bold">Đã vote: {{ voteSummary?.total_votes || 0 }} / {{ voteSummary?.total_alive || voteStarted.targets.length }}</p>
      </div>

      <div class="space-y-2">
        <div
          v-for="item in voteSummary?.ranking || []"
          :key="item.player_id"
          class="flex items-center justify-between rounded-xl bg-slate-800 p-3"
        >
          <span>{{ item.player_name }}</span>
          <b class="text-yellow-300">{{ item.votes }} phiếu</b>
        </div>
      </div>

      <div v-if="voteEnded" class="rounded-xl border border-yellow-800 bg-yellow-950/50 p-4">
        <p class="font-bold text-yellow-100">{{ voteEnded.message }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { VoteEndedPayload, VoteStartedPayload, VoteSummary } from '@/types/game'

defineProps<{
  voteStarted: VoteStartedPayload | null
  voteSummary: VoteSummary | null
  voteEnded: VoteEndedPayload | null
}>()
</script>
