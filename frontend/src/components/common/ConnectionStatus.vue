<template>
  <div class="inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-bold" :class="statusClass">
    <span class="h-2 w-2 rounded-full bg-current" />
    {{ label }}
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ConnectionStatus } from '@/services/websocket'

const props = defineProps<{
  status: ConnectionStatus
}>()

const label = computed(() => {
  const map: Record<ConnectionStatus, string> = {
    idle: 'Chưa kết nối',
    connecting: 'Đang kết nối',
    connected: 'Online',
    closed: 'Mất kết nối',
    error: 'Lỗi kết nối',
  }
  return map[props.status]
})

const statusClass = computed(() => {
  if (props.status === 'connected') return 'bg-green-900 text-green-200'
  if (props.status === 'connecting') return 'bg-yellow-900 text-yellow-200'
  if (props.status === 'error') return 'bg-red-900 text-red-200'
  return 'bg-slate-800 text-slate-300'
})
</script>
