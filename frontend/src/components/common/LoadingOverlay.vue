<template>
  <div v-if="show" class="fixed inset-0 z-50 grid place-items-center bg-black/70">
    <div class="rounded-2xl border border-slate-700 bg-slate-900 p-6 text-center shadow-xl">
      <div class="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-slate-600 border-t-red-400" />
      <p class="mt-4 font-semibold">{{ text }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    show: boolean
    text?: string
  }>(),
  {
    text: 'Đang xử lý...',
  },
)
</script>
