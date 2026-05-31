<template>
  <div class="flex items-center justify-between gap-3 rounded-xl bg-slate-800 p-4">
    <div>
      <p class="font-semibold">{{ player.name }}</p>
      <p class="text-xs text-slate-400">
        {{ player.is_alive ? 'Còn sống' : 'Đã chết' }} · {{ player.is_connected ? 'online' : 'offline' }}
      </p>
    </div>

    <div class="flex items-center gap-2">
      <span
        class="rounded-full px-3 py-1 text-xs font-bold"
        :class="player.is_alive ? 'bg-green-900 text-green-200' : 'bg-red-950 text-red-200'"
      >
        {{ player.is_alive ? 'Sống' : 'Chết' }}
      </span>

      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PlayerInRoom } from '@/types/player'

defineProps<{
  player: PlayerInRoom
}>()
</script>
