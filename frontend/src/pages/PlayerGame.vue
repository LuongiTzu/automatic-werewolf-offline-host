<template>
  <section class="mx-auto max-w-2xl space-y-6">
    <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 class="text-2xl font-bold">Player Game</h2>

      <div v-if="!store.roomCode || !store.playerId" class="mt-4 rounded-xl bg-yellow-950 p-4 text-yellow-100">
        Bạn chưa join phòng. Hãy quay lại trang Player để vào phòng.
      </div>

      <div v-else class="mt-6 space-y-4">
        <div class="rounded-xl bg-slate-800 p-4">
          <p class="text-sm text-slate-400">Tên</p>
          <p class="text-xl font-bold">{{ store.playerName }}</p>
        </div>

        <div class="rounded-xl bg-slate-800 p-4">
          <p class="text-sm text-slate-400">Mã phòng</p>
          <p class="text-3xl font-black tracking-[0.3em] text-red-300">{{ store.roomCode }}</p>
        </div>

        <div class="grid gap-3 sm:grid-cols-3">
          <div class="rounded-xl bg-slate-800 p-4">
            <p class="text-sm text-slate-400">Status</p>
            <p class="font-bold">{{ store.status || 'waiting' }}</p>
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

        <button
          v-if="store.status === 'playing'"
          class="w-full rounded-xl bg-red-700 px-5 py-3 font-bold hover:bg-red-600"
          @click="store.loadMyRole"
        >
          Xem role của tôi
        </button>

        <div v-if="store.myRole" class="rounded-2xl border border-red-800 bg-red-950/40 p-6 text-center">
          <p class="text-sm text-red-200">Role của bạn</p>
          <h3 class="mt-2 text-3xl font-black">{{ store.myRole.role_name }}</h3>
          <p class="mt-2 text-sm text-red-100">{{ store.myRole.role_code }} · {{ store.myRole.side }}</p>
          <p class="mt-4 text-sm text-slate-200">{{ store.myRole.description }}</p>
        </div>
      </div>
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
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoomStore } from '../stores/roomStore'

const store = useRoomStore()

onMounted(async () => {
  if (store.roomCode && store.playerId) {
    await store.loadRoom()
    store.connectWebSocket('player')
  }
})
</script>