<template>
  <section class="mx-auto max-w-xl">
    <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 class="text-2xl font-bold">Player Join</h2>
      <p class="mt-1 text-sm text-slate-400">
        Nhập mã phòng và tên để tham gia game.
      </p>

      <form class="mt-6 space-y-4" @submit.prevent="join">
        <div>
          <label class="mb-2 block text-sm font-semibold">Mã phòng</label>
          <input
            v-model="roomCode"
            class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 uppercase outline-none focus:border-red-500"
            placeholder="ABC123"
            maxlength="6"
          />
        </div>

        <div>
          <label class="mb-2 block text-sm font-semibold">Tên người chơi</label>
          <input
            v-model="name"
            class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-red-500"
            placeholder="Nhập tên của bạn"
            maxlength="50"
          />
        </div>

        <button
          class="w-full rounded-xl bg-red-700 px-5 py-3 font-bold hover:bg-red-600 disabled:opacity-50"
          :disabled="store.loading"
        >
          Vào phòng
        </button>
      </form>

      <p v-if="store.error" class="mt-4 rounded-lg bg-red-950 p-3 text-sm text-red-200">
        {{ store.error }}
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoomStore } from '../stores/roomStore'

const router = useRouter()
const store = useRoomStore()

const roomCode = ref('')
const name = ref('')

async function join() {
  if (!roomCode.value.trim() || !name.value.trim()) {
    store.error = 'Vui lòng nhập mã phòng và tên.'
    return
  }

  await store.joinRoom(roomCode.value, name.value)

  if (!store.error) {
    router.push('/player')
  }
}
</script>