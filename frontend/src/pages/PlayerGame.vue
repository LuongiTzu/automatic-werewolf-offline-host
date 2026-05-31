<template>
  <section class="mx-auto max-w-3xl space-y-6">
    <div v-if="!store.roomCode || !store.playerId" class="rounded-xl bg-yellow-950 p-4 text-yellow-100">
      Bạn chưa join phòng. Hãy quay lại trang Người chơi để vào phòng.
    </div>

    <template v-else>
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 class="text-2xl font-black">{{ store.playerName }}</h1>
          <p class="text-sm text-slate-400">Phòng {{ store.roomCode }}</p>
        </div>
        <div class="flex items-center gap-2">
          <PhaseBadge :phase="store.currentPhase || 'setup'" />
          <ConnectionStatus :status="store.socketStatus" />
        </div>
      </div>

      <p v-if="store.error" class="rounded-lg bg-red-950 p-3 text-sm text-red-200">
        {{ store.error }}
      </p>

      <PlayerGameOver v-if="store.isGameOver || store.currentPhase === 'ended'" :winner="store.winner" />

      <PlayerDeadView v-else-if="!store.isMeAlive" />

      <PlayerLobby
        v-else-if="store.status !== 'playing'"
        :player-name="store.playerName"
        :room-code="store.roomCode"
        :players="store.players"
      />

      <PlayerRoleReveal
        v-else-if="store.currentPhase === 'role_reveal' || !store.myRole"
        :role="store.myRole"
        @load-role="store.loadMyRole"
      />

      <PlayerNightAction
        v-else-if="store.allowedNightAction"
        :action="store.allowedNightAction"
        :result="store.lastNightActionResult"
        :player-id="store.playerId"
        @submit="store.submitNightAction"
      />

      <PlayerNightSleep
        v-else-if="store.currentPhase === 'night_start' || store.currentPhase === 'night_role_turn' || store.currentPhase === 'night_resolving'"
        :phase-ends-at="store.phaseEndsAt"
      />

      <PlayerDayView
        v-else-if="store.currentPhase === 'day_result' || store.currentPhase === 'day_discussion'"
        :phase-ends-at="store.phaseEndsAt"
        :dead-players="store.dayResult?.dead_players || []"
      />

      <PlayerVoteView
        v-else-if="store.currentPhase === 'voting'"
        :targets="store.voteStarted?.targets || store.alivePlayers"
        :player-id="store.playerId"
        :phase-ends-at="store.phaseEndsAt"
        :summary="store.voteSummary"
        @vote="store.submitVote"
      />

      <div v-else class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h2 class="text-2xl font-bold">Đang chờ</h2>
        <p class="mt-2 text-slate-300">Hệ thống đang chuyển phase. Hãy chờ màn hình tự cập nhật.</p>
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import ConnectionStatus from '@/components/common/ConnectionStatus.vue'
import PhaseBadge from '@/components/common/PhaseBadge.vue'
import PlayerDayView from '@/components/player/PlayerDayView.vue'
import PlayerDeadView from '@/components/player/PlayerDeadView.vue'
import PlayerGameOver from '@/components/player/PlayerGameOver.vue'
import PlayerLobby from '@/components/player/PlayerLobby.vue'
import PlayerNightAction from '@/components/player/PlayerNightAction.vue'
import PlayerNightSleep from '@/components/player/PlayerNightSleep.vue'
import PlayerRoleReveal from '@/components/player/PlayerRoleReveal.vue'
import PlayerVoteView from '@/components/player/PlayerVoteView.vue'
import { useRoomStore } from '@/stores/roomStore'

const store = useRoomStore()

onMounted(async () => {
  if (store.roomCode && store.playerId) {
    await store.loadRoom()
    if (store.status === 'playing') await store.loadMyRole()
    store.connectWebSocket('player')
  }
})
</script>
