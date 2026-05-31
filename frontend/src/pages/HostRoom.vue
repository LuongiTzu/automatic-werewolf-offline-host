<template>
  <section class="space-y-6">
    <div class="container mx-auto px-4">
      <AudioControl />
    </div>

    <div class="container mx-auto px-4">
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <PhaseBadge :phase="store.currentPhase || 'setup'" />
          <ConnectionStatus :status="store.socketStatus" />
        </div>

        <button
          v-if="store.roomCode"
          class="rounded-lg bg-slate-800 px-3 py-2 text-sm hover:bg-slate-700"
          @click="refreshAll"
        >
          Refresh
        </button>
      </div>

      <p v-if="store.error" class="mb-4 rounded-lg bg-red-950 p-3 text-sm text-red-200">
        {{ store.error }}
      </p>

      <HostLobby
        v-if="store.status !== 'playing' && !store.isGameOver"
        :room-code="store.roomCode"
        :status="store.status || 'waiting'"
        :loading="store.loading"
        :players="store.players"
        :roles="store.roles"
        :role-cart="store.roleCart"
        @create-room="store.createRoom"
        @refresh-room="refreshAll"
        @kick-player="store.kickPlayer"
        @change-quantity="store.setRoleQuantity"
        @start-game="store.startGame"
      />

      <div v-else class="grid gap-6 lg:grid-cols-[1fr_0.85fr]">
        <HostGameDashboard
          :phase="store.currentPhase"
          :night-number="store.nightNumber"
          :day-number="store.dayNumber"
          :current-role-turn="store.currentRoleTurn"
          :phase-ends-at="store.phaseEndsAt"
          :audio-text="store.currentAudioText"
          :is-game-over="store.isGameOver"
          :vote-started="store.voteStarted"
          :vote-summary="store.voteSummary"
          :vote-ended="store.voteEnded"
          :logs="store.gameLogs"
          @pause="store.pauseGame"
          @resume="store.resumeGame"
          @stop="store.stopGame"
          @load-logs="store.loadGameLogs"
        />

        <div class="space-y-6">
          <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <p class="text-sm text-slate-400">Mã phòng</p>
            <p class="mt-2 text-4xl font-black tracking-[0.3em] text-red-300">{{ store.roomCode }}</p>
          </div>

          <HostPlayerList
            :players="store.players"
            :can-kick="true"
            @refresh="refreshAll"
            @kick="store.kickPlayer"
          />

          <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h3 class="text-xl font-bold">Realtime events</h3>
            <div class="mt-4 max-h-72 space-y-2 overflow-auto">
              <div v-for="event in store.events" :key="event.timestamp + event.type" class="rounded-lg bg-slate-800 p-3 text-xs">
                <p class="font-bold text-yellow-300">{{ event.type }}</p>
                <pre class="mt-1 whitespace-pre-wrap text-slate-300">{{ event.payload }}</pre>
              </div>
              <p v-if="store.events.length === 0" class="text-sm text-slate-400">Chưa có event realtime.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <LoadingOverlay :show="store.loading" />
  </section>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import ConnectionStatus from '@/components/common/ConnectionStatus.vue'
import LoadingOverlay from '@/components/common/LoadingOverlay.vue'
import PhaseBadge from '@/components/common/PhaseBadge.vue'
import AudioControl from '@/components/host/AudioControl.vue'
import HostGameDashboard from '@/components/host/HostGameDashboard.vue'
import HostLobby from '@/components/host/HostLobby.vue'
import HostPlayerList from '@/components/host/HostPlayerList.vue'
import audioService from '@/services/audioService'
import { useRoomStore } from '@/stores/roomStore'

const store = useRoomStore()

onMounted(async () => {
  if (store.roomCode) {
    await refreshAll()
    store.connectWebSocket('host')
  }
})

watch(
  () => store.currentAudioText,
  async (text) => {
    if (text) await audioService.speak(text)
  },
)

watch(
  () => store.currentPhase,
  async (phase) => {
    if (phase === 'night_start' || phase === 'night_role_turn' || phase === 'night_resolving') {
      await audioService.setAmbientEnabled(true)
    } else if (phase === 'day_result' || phase === 'day_discussion' || phase === 'voting' || phase === 'ended') {
      await audioService.setAmbientEnabled(false)
    }
  },
)

async function refreshAll() {
  await store.loadRoom()
  if (store.roomCode) {
    await store.loadRoles()
    await store.loadRoleCart()
  }
}
</script>
