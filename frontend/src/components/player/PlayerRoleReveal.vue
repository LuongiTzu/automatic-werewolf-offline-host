<template>
  <div class="rounded-2xl border border-red-800 bg-red-950/40 p-6 text-center">
    <p class="text-sm text-red-200">Role của bạn</p>

    <div v-if="role" class="mt-3">
      <h2 class="text-4xl font-black">{{ role.role_name }}</h2>
      <p class="mt-2 text-sm text-red-100">{{ role.role_code }} · {{ sideName(role.side) }}</p>
      <p class="mt-4 text-base text-slate-100">{{ role.description || 'Không có mô tả.' }}</p>
    </div>

    <button
      v-else
      class="mt-5 rounded-xl bg-red-700 px-5 py-3 font-bold hover:bg-red-600"
      @click="$emit('load-role')"
    >
      Xem role của tôi
    </button>

    <p class="mt-5 text-sm text-slate-300">
      Ghi nhớ role của bạn. Khi tới lượt, màn hình sẽ tự mở chức năng.
    </p>
  </div>
</template>

<script setup lang="ts">
import type { PlayerRole } from '@/types/player'
import { sideName } from '@/types/player'

defineProps<{
  role: PlayerRole | null
}>()

defineEmits<{
  'load-role': []
}>()
</script>
