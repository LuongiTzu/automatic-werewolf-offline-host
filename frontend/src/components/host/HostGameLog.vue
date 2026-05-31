<template>
  <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
    <div class="flex items-center justify-between gap-3">
      <div>
        <h3 class="text-xl font-bold">Log cuối game</h3>
        <p class="text-sm text-slate-400">Chỉ nên xem khi game đã kết thúc để không lộ bài.</p>
      </div>

      <button class="rounded-lg bg-slate-700 px-3 py-2 text-sm hover:bg-slate-600" @click="$emit('load')">
        Tải log
      </button>
    </div>

    <div class="mt-4 max-h-96 space-y-2 overflow-auto">
      <div v-for="log in logs" :key="log.id" class="rounded-xl bg-slate-800 p-4 text-sm">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <b class="text-yellow-300">{{ log.event_type }}</b>
          <span class="text-xs text-slate-400">Đêm {{ log.night_number ?? '-' }} · Ngày {{ log.day_number ?? '-' }}</span>
        </div>
        <p class="mt-1">{{ log.message }}</p>
        <pre class="mt-2 overflow-auto rounded-lg bg-slate-950 p-2 text-xs text-slate-300">{{ log.data }}</pre>
      </div>

      <p v-if="logs.length === 0" class="text-sm text-slate-400">
        Chưa có log hoặc chưa tải log.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { GameLogItem } from '@/types/game'

defineProps<{
  logs: GameLogItem[]
}>()

defineEmits<{
  load: []
}>()
</script>
