<template>
  <div class="min-h-[70vh] rounded-3xl border border-slate-900 bg-black p-6 text-center">
    <div class="flex min-h-[60vh] flex-col items-center justify-center">
      <div class="h-20 w-20 animate-pulse rounded-full bg-indigo-900/30" />
      <h2 class="mt-8 text-3xl font-black text-slate-200">Đang ngủ</h2>
      <p class="mt-2 max-w-md text-sm text-slate-500">
        Không nhìn màn hình người khác. Khi tới lượt role của bạn, màn hình sẽ tự mở.
      </p>
      <div class="mt-8 w-full max-w-sm">
        <CountdownTimer :ends-at="phaseEndsAt" label="Phase hiện tại còn" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import CountdownTimer from '@/components/common/CountdownTimer.vue'

defineProps<{
  phaseEndsAt: string
}>()
</script>
