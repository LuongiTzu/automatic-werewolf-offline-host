<template>
  <div class="rounded-3xl border border-purple-800 bg-purple-950/60 p-8 text-center">
    <p class="text-sm text-purple-100">Game over</p>
    <h2 class="mt-2 text-4xl font-black">Trò chơi kết thúc</h2>
    <p class="mt-4 text-2xl font-bold text-yellow-200">{{ winnerLabel(winner) }} chiến thắng</p>
  </div>
</template>

<script setup lang="ts">
import { winnerLabel } from '@/types/game'

defineProps<{
  winner: string
}>()
</script>
