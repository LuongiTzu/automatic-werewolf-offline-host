<template>
  <section class="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
    <div class="space-y-6">
      <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h2 class="text-2xl font-bold">Host Room</h2>
        <p class="mt-1 text-sm text-slate-400">
          Tạo phòng, chọn role và bắt đầu game.
        </p>

        <div class="mt-6">
          <button
            v-if="!store.roomCode"
            :disabled="store.loading"
            class="rounded-xl bg-red-700 px-5 py-3 font-semibold hover:bg-red-600 disabled:opacity-60"
            @click="store.createRoom"
          >
            Tạo phòng mới
          </button>

          <div v-else class="space-y-3">
            <p class="text-sm text-slate-400">Mã phòng</p>
            <div class="rounded-xl border border-red-800 bg-red-950/40 p-5 text-center">
              <p class="text-4xl font-black tracking-[0.3em] text-red-300">
                {{ store.roomCode }}
              </p>
            </div>

            <div class="grid gap-3 sm:grid-cols-3">
              <div class="rounded-xl bg-slate-800 p-4">
                <p class="text-sm text-slate-400">Trạng thái</p>
                <p class="font-bold">{{ store.status || 'unknown' }}</p>
              </div>

              <div class="rounded-xl bg-slate-800 p-4">
                <p class="text-sm text-slate-400">Phase</p>
                <p class="font-bold">{{ store.currentPhase || 'setup' }}</p>
              </div>

              <div class="rounded-xl bg-slate-800 p-4">
                <p class="text-sm text-slate-400">WebSocket</p>
                <p class="font-bold" :class="store.socketConnected ? 'text-green-400' : 'text-yellow-400'">
                  {{ store.socketConnected ? 'Connected' : 'Not connected' }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <p v-if="store.error" class="mt-4 rounded-lg bg-red-950 p-3 text-sm text-red-200">
          {{ store.error }}
        </p>
      </div>

      <div v-if="store.roomCode" class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold">Người chơi</h3>
          <button
            class="rounded-lg bg-slate-700 px-3 py-2 text-sm hover:bg-slate-600"
            @click="store.loadRoom"
          >
            Refresh
          </button>
        </div>

        <div class="mt-4 space-y-2">
          <div
            v-for="player in store.players"
            :key="player.id"
            class="flex items-center justify-between rounded-xl bg-slate-800 p-4"
          >
            <div>
              <p class="font-semibold">{{ player.name }}</p>
              <p class="text-xs text-slate-400">{{ player.id }}</p>
            </div>

            <span
              class="rounded-full px-3 py-1 text-xs font-bold"
              :class="player.is_connected ? 'bg-green-900 text-green-200' : 'bg-slate-700 text-slate-300'"
            >
              {{ player.is_connected ? 'online' : 'offline' }}
            </span>
          </div>

          <p v-if="store.players.length === 0" class="text-slate-400">
            Chưa có player nào vào phòng.
          </p>
        </div>
      </div>
    </div>

    <div v-if="store.roomCode" class="space-y-6">
      <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h3 class="text-xl font-bold">Role Cart</h3>

        <div class="mt-4 space-y-3">
          <div
            v-for="role in store.roles"
            :key="role.code"
            class="rounded-xl bg-slate-800 p-4"
          >
            <div class="flex items-center justify-between gap-3">
              <div>
                <p class="font-semibold">{{ role.name }}</p>
                <p class="text-xs text-slate-400">{{ role.code }} · {{ role.side }}</p>
              </div>

              <div class="flex items-center gap-2">
                <button
                  class="h-9 w-9 rounded-lg bg-slate-700 text-xl hover:bg-slate-600"
                  @click="changeQuantity(role.code, -1)"
                >
                  -
                </button>

                <span class="w-8 text-center font-bold">
                  {{ getQuantity(role.code) }}
                </span>

                <button
                  class="h-9 w-9 rounded-lg bg-red-700 text-xl hover:bg-red-600"
                  @click="changeQuantity(role.code, 1)"
                >
                  +
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="store.roleCart" class="mt-5 rounded-xl bg-slate-950 p-4 text-sm">
          <p>Total roles: <b>{{ store.roleCart.total_roles }}</b></p>
          <p>Total players: <b>{{ store.roleCart.total_players }}</b></p>
          <p>
            Can start:
            <b :class="store.roleCart.can_start ? 'text-green-400' : 'text-red-400'">
              {{ store.roleCart.can_start }}
            </b>
          </p>
        </div>

        <button
          class="mt-5 w-full rounded-xl bg-red-700 px-5 py-3 font-bold hover:bg-red-600 disabled:opacity-50"
          :disabled="!store.roleCart?.can_start || store.loading"
          @click="store.startGame"
        >
          Bắt đầu game
        </button>
      </div>

      <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h3 class="text-xl font-bold">Realtime Events</h3>

        <div class="mt-4 max-h-72 space-y-2 overflow-auto">
          <div
            v-for="event in store.events"
            :key="event.timestamp + event.type"
            class="rounded-lg bg-slate-800 p-3 text-xs"
          >
            <p class="font-bold text-yellow-300">{{ event.type }}</p>
            <pre class="mt-1 whitespace-pre-wrap text-slate-300">{{ event.payload }}</pre>
          </div>

          <p v-if="store.events.length === 0" class="text-sm text-slate-400">
            Chưa có event realtime.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoomStore } from '../stores/roomStore'

const store = useRoomStore()

onMounted(async () => {
  if (store.roomCode) {
    await store.loadRoom()
    await store.loadRoles()
    await store.loadRoleCart()
    store.connectWebSocket('host')
  }
})

function getQuantity(roleCode: string) {
  return store.roleCart?.cart.find((item) => item.role_code === roleCode)?.quantity || 0
}

async function changeQuantity(roleCode: string, delta: number) {
  const current = getQuantity(roleCode)
  await store.setRoleQuantity(roleCode, current + delta)
}
</script>