<template>
  <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
    <h2 class="text-2xl font-bold">Phòng chờ</h2>
    <p class="mt-1 text-sm text-slate-400">Chờ Host chọn role và bắt đầu game.</p>

    <div class="mt-5 grid gap-3 sm:grid-cols-2">
      <div class="rounded-xl bg-slate-800 p-4">
        <p class="text-sm text-slate-400">Tên</p>
        <p class="text-xl font-bold">{{ playerName }}</p>
      </div>
      <div class="rounded-xl bg-slate-800 p-4">
        <p class="text-sm text-slate-400">Mã phòng</p>
        <p class="text-3xl font-black tracking-[0.3em] text-red-300">{{ roomCode }}</p>
      </div>
    </div>

    <div class="mt-5 space-y-2">
      <p class="font-semibold">Người chơi trong phòng</p>
      <PlayerCard v-for="player in players" :key="player.id" :player="player" />
    </div>
  </div>
</template>

<script setup lang="ts">
import PlayerCard from '@/components/common/PlayerCard.vue'
import type { PlayerInRoom } from '@/types/player'

defineProps<{
  playerName: string
  roomCode: string
  players: PlayerInRoom[]
}>()
</script>
