<template>
  <div class="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
    <div class="space-y-6">
      <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h2 class="text-2xl font-bold">Host Room</h2>
        <p class="mt-1 text-sm text-slate-400">Tạo phòng, chọn role, kiểm tra người chơi rồi bấm bắt đầu.</p>

        <button
          v-if="!roomCode"
          :disabled="loading"
          class="mt-6 rounded-xl bg-red-700 px-5 py-3 font-semibold hover:bg-red-600 disabled:opacity-60"
          @click="$emit('create-room')"
        >
          Tạo phòng mới
        </button>

        <div v-else class="mt-6 space-y-3">
          <p class="text-sm text-slate-400">Mã phòng</p>
          <div class="rounded-xl border border-red-800 bg-red-950/40 p-5 text-center">
            <p class="text-4xl font-black tracking-[0.3em] text-red-300">{{ roomCode }}</p>
          </div>
          <p class="text-sm text-slate-400">Player vào trang Người chơi rồi nhập mã phòng này.</p>
        </div>
      </div>

      <HostPlayerList
        v-if="roomCode"
        :players="players"
        :can-kick="status === 'waiting'"
        @refresh="$emit('refresh-room')"
        @kick="$emit('kick-player', $event)"
      />
    </div>

    <HostRoleCart
      v-if="roomCode"
      :roles="roles"
      :role-cart="roleCart"
      :disabled="loading || status !== 'waiting'"
      @change-quantity="forwardChangeQuantity"
      @start="$emit('start-game')"
    />
  </div>
</template>

<script setup lang="ts">
import HostPlayerList from '@/components/host/HostPlayerList.vue'
import HostRoleCart from '@/components/host/HostRoleCart.vue'
import type { PlayerInRoom } from '@/types/player'
import type { RoleCartResponse, RoleResponse } from '@/types/room'

defineProps<{
  roomCode: string
  status: string
  loading: boolean
  players: PlayerInRoom[]
  roles: RoleResponse[]
  roleCart: RoleCartResponse | null
}>()

const emit = defineEmits<{
  'create-room': []
  'refresh-room': []
  'kick-player': [playerId: string]
  'change-quantity': [roleCode: string, quantity: number]
  'start-game': []
}>()

function forwardChangeQuantity(roleCode: string, quantity: number) {
  emit('change-quantity', roleCode, quantity)
}
</script>
