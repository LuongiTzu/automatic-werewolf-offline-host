<template>
  <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h3 class="text-xl font-bold">Bảng điều khiển tự động</h3>
        <p class="mt-1 text-sm text-slate-400">Host chỉ giám sát, backend tự chạy phase theo thời gian.</p>
      </div>
      <PhaseBadge :phase="phase" />
    </div>

    <div class="mt-5 grid gap-3 sm:grid-cols-3">
      <div class="rounded-xl bg-slate-800 p-4">
        <p class="text-sm text-slate-400">Đêm</p>
        <p class="text-2xl font-black">{{ nightNumber }}</p>
      </div>
      <div class="rounded-xl bg-slate-800 p-4">
        <p class="text-sm text-slate-400">Ngày</p>
        <p class="text-2xl font-black">{{ dayNumber }}</p>
      </div>
      <div class="rounded-xl bg-slate-800 p-4">
        <p class="text-sm text-slate-400">Role đang gọi</p>
        <p class="text-2xl font-black">{{ roleName(currentRoleTurn) }}</p>
      </div>
    </div>

    <div class="mt-5">
      <CountdownTimer :ends-at="phaseEndsAt" />
    </div>

    <div class="mt-5 rounded-xl bg-slate-950 p-4">
      <p class="text-sm font-semibold text-slate-400">Câu quản trò hiện tại</p>
      <p class="mt-2 text-lg font-bold text-yellow-100">{{ audioText || 'Chưa có câu đọc.' }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import CountdownTimer from '@/components/common/CountdownTimer.vue'
import PhaseBadge from '@/components/common/PhaseBadge.vue'
import { roleName } from '@/types/player'

defineProps<{
  phase: string
  nightNumber: number
  dayNumber: number
  currentRoleTurn: string
  phaseEndsAt: string
  audioText: string
}>()
</script>
