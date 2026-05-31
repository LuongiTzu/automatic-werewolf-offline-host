<template>
  <div class="rounded-3xl border p-6" :class="panelClass">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <p class="text-sm opacity-80">Đến lượt bạn</p>
        <h2 class="text-3xl font-black">{{ roleName(action.role_code) }}</h2>
      </div>
      <CountdownTimer :ends-at="action.phase_ends_at" label="Còn" />
    </div>

    <div v-if="result" class="mt-5 rounded-xl border border-green-700 bg-green-950/70 p-4">
      <p class="font-bold text-green-100">Đã gửi hành động.</p>
      <p v-if="result.private_result" class="mt-2 text-sm">
        Kết quả: <b>{{ result.private_result.target_name }}</b> là <b>{{ result.private_result.result }}</b>
      </p>
    </div>

    <div v-else class="mt-6 space-y-4">
      <p class="text-sm opacity-90">{{ instruction }}</p>

      <div v-if="action.role_code === 'WITCH'" class="grid gap-3 sm:grid-cols-3">
        <button class="rounded-xl bg-green-700 px-4 py-3 font-bold hover:bg-green-600" @click="$emit('submit', 'WITCH_HEAL', null)">
          Dùng bình cứu
        </button>
        <button class="rounded-xl bg-slate-700 px-4 py-3 font-bold hover:bg-slate-600" @click="$emit('submit', 'SKIP', null)">
          Bỏ qua
        </button>
      </div>

      <div class="grid gap-3 sm:grid-cols-2">
        <button
          v-for="target in filteredTargets"
          :key="target.id"
          class="rounded-xl bg-slate-950/70 px-4 py-4 text-left font-bold hover:bg-slate-800"
          @click="submitTarget(target.id)"
        >
          {{ target.name }}
        </button>
      </div>

      <button
        v-if="action.role_code !== 'WITCH'"
        class="w-full rounded-xl bg-slate-700 px-4 py-3 font-bold hover:bg-slate-600"
        @click="$emit('submit', 'SKIP', null)"
      >
        Bỏ qua
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import CountdownTimer from '@/components/common/CountdownTimer.vue'
import type { NightActionPayload, NightActionResponse } from '@/types/game'
import { roleName } from '@/types/player'

const props = defineProps<{
  action: NightActionPayload
  result: NightActionResponse | null
  playerId: string
}>()

const emit = defineEmits<{
  submit: [actionType: string, targetId: string | null]
}>()

const panelClass = computed(() => {
  if (props.action.role_code === 'WEREWOLF') return 'border-red-800 bg-red-950/70'
  if (props.action.role_code === 'WITCH') return 'border-purple-800 bg-purple-950/70'
  return 'border-green-800 bg-green-950/70'
})

const instruction = computed(() => {
  const map: Record<string, string> = {
    WEREWOLF: 'Chọn một người để cắn.',
    GUARD: 'Chọn một người để bảo vệ.',
    SEER: 'Chọn một người để soi.',
    WITCH: 'Có thể cứu, độc một người, hoặc bỏ qua.',
  }
  return map[props.action.role_code] || 'Chọn mục tiêu.'
})

const filteredTargets = computed(() => {
  if (props.action.role_code === 'GUARD') return props.action.targets
  return props.action.targets.filter((target) => target.id !== props.playerId)
})

function submitTarget(targetId: string) {
  const map: Record<string, string> = {
    WEREWOLF: 'WEREWOLF_BITE',
    GUARD: 'GUARD_PROTECT',
    SEER: 'SEER_CHECK',
    WITCH: 'WITCH_POISON',
  }
  emit('submit', map[props.action.role_code] || 'SKIP', targetId)
}
</script>
