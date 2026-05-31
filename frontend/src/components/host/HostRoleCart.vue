<template>
  <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
    <h3 class="text-xl font-bold">Role Cart</h3>
    <p class="mt-1 text-sm text-slate-400">Chọn số lượng role trước khi bắt đầu.</p>

    <div class="mt-4 space-y-3">
      <div v-for="role in roles" :key="role.code" class="rounded-xl bg-slate-800 p-4">
        <div class="flex items-center justify-between gap-3">
          <div>
            <p class="font-semibold">{{ role.name }}</p>
            <p class="text-xs text-slate-400">{{ role.code }} · {{ role.side }}</p>
          </div>

          <div class="flex items-center gap-2">
            <button
              class="h-9 w-9 rounded-lg bg-slate-700 text-xl hover:bg-slate-600 disabled:opacity-40"
              :disabled="disabled"
              @click="$emit('change-quantity', role.code, getQuantity(role.code) - 1)"
            >
              -
            </button>

            <span class="w-8 text-center font-bold">{{ getQuantity(role.code) }}</span>

            <button
              class="h-9 w-9 rounded-lg bg-red-700 text-xl hover:bg-red-600 disabled:opacity-40"
              :disabled="disabled"
              @click="$emit('change-quantity', role.code, getQuantity(role.code) + 1)"
            >
              +
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="roleCart" class="mt-5 rounded-xl bg-slate-950 p-4 text-sm">
      <p>Total roles: <b>{{ roleCart.total_roles }}</b></p>
      <p>Total players: <b>{{ roleCart.total_players }}</b></p>
      <p>
        Can start:
        <b :class="roleCart.can_start ? 'text-green-400' : 'text-red-400'">{{ roleCart.can_start }}</b>
      </p>
    </div>

    <button
      class="mt-5 w-full rounded-xl bg-red-700 px-5 py-3 font-bold hover:bg-red-600 disabled:opacity-50"
      :disabled="disabled || !roleCart?.can_start"
      @click="$emit('start')"
    >
      Bắt đầu game tự động
    </button>
  </div>
</template>

<script setup lang="ts">
import type { RoleCartResponse, RoleResponse } from '@/types/room'

const props = defineProps<{
  roles: RoleResponse[]
  roleCart: RoleCartResponse | null
  disabled: boolean
}>()

defineEmits<{
  'change-quantity': [roleCode: string, quantity: number]
  start: []
}>()

function getQuantity(roleCode: string): number {
  return props.roleCart?.cart.find((item) => item.role_code === roleCode)?.quantity || 0
}
</script>
