<template>
  <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
    <div class="flex items-center justify-between gap-3">
      <div>
        <h3 class="text-xl font-bold">Người chơi</h3>
        <p class="text-sm text-slate-400">{{ players.length }} người trong phòng</p>
      </div>

      <button class="rounded-lg bg-slate-700 px-3 py-2 text-sm hover:bg-slate-600" @click="$emit('refresh')">
        Refresh
      </button>
    </div>

    <div class="mt-4 space-y-2">
      <PlayerCard v-for="player in players" :key="player.id" :player="player">
        <button
          v-if="canKick"
          class="rounded-lg bg-red-800 px-3 py-1 text-xs font-bold hover:bg-red-700"
          @click="$emit('kick', player.id)"
        >
          Kick
        </button>
      </PlayerCard>

      <p v-if="players.length === 0" class="text-slate-400">Chưa có player nào vào phòng.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import PlayerCard from '@/components/common/PlayerCard.vue'
import type { PlayerInRoom } from '@/types/player'

defineProps<{
  players: PlayerInRoom[]
  canKick: boolean
}>()

defineEmits<{
  refresh: []
  kick: [playerId: string]
}>()
</script>
