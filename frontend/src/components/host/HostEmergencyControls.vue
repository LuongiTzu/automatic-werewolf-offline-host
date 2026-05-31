<template>
  <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
    <h3 class="text-xl font-bold">Can thiệp khẩn cấp</h3>
    <p class="mt-1 text-sm text-slate-400">Dùng khi cần tạm dừng hoặc kết thúc ván.</p>

    <div class="mt-4 grid gap-3 sm:grid-cols-3">
      <button class="rounded-xl bg-yellow-700 px-4 py-3 font-bold hover:bg-yellow-600" @click="$emit('pause')">
        Tạm dừng
      </button>
      <button class="rounded-xl bg-green-700 px-4 py-3 font-bold hover:bg-green-600" @click="$emit('resume')">
        Tiếp tục
      </button>
      <button class="rounded-xl bg-red-800 px-4 py-3 font-bold hover:bg-red-700" @click="$emit('stop')">
        Dừng game
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineEmits<{
  pause: []
  resume: []
  stop: []
}>()
</script>
