<template>
  <div class="space-y-6">
    <HostPhasePanel
      :phase="phase"
      :night-number="nightNumber"
      :day-number="dayNumber"
      :current-role-turn="currentRoleTurn"
      :phase-ends-at="phaseEndsAt"
      :audio-text="audioText"
    />

    <HostVotePanel :vote-started="voteStarted" :vote-summary="voteSummary" :vote-ended="voteEnded" />

    <HostEmergencyControls @pause="$emit('pause')" @resume="$emit('resume')" @stop="$emit('stop')" />

    <HostGameLog v-if="isGameOver" :logs="logs" @load="$emit('load-logs')" />
  </div>
</template>

<script setup lang="ts">
import HostEmergencyControls from '@/components/host/HostEmergencyControls.vue'
import HostGameLog from '@/components/host/HostGameLog.vue'
import HostPhasePanel from '@/components/host/HostPhasePanel.vue'
import HostVotePanel from '@/components/host/HostVotePanel.vue'
import type { GameLogItem, VoteEndedPayload, VoteStartedPayload, VoteSummary } from '@/types/game'

defineProps<{
  phase: string
  nightNumber: number
  dayNumber: number
  currentRoleTurn: string
  phaseEndsAt: string
  audioText: string
  isGameOver: boolean
  voteStarted: VoteStartedPayload | null
  voteSummary: VoteSummary | null
  voteEnded: VoteEndedPayload | null
  logs: GameLogItem[]
}>()

defineEmits<{
  pause: []
  resume: []
  stop: []
  'load-logs': []
}>()
</script>
