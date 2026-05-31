import { defineStore } from 'pinia'
import type {
  DayStartedPayload,
  GameState,
  NightActionPayload,
  NightActionResponse,
  VoteEndedPayload,
  VoteStartedPayload,
  VoteSummary,
} from '@/types/game'

interface GameStoreState {
  state: GameState | null
  allowedNightAction: NightActionPayload | null
  lastNightActionResult: NightActionResponse | null
  dayResult: DayStartedPayload | null
  voteStarted: VoteStartedPayload | null
  voteSummary: VoteSummary | null
  voteEnded: VoteEndedPayload | null
}

export const useGameStore = defineStore('game', {
  state: (): GameStoreState => ({
    state: null,
    allowedNightAction: null,
    lastNightActionResult: null,
    dayResult: null,
    voteStarted: null,
    voteSummary: null,
    voteEnded: null,
  }),

  getters: {
    currentPhase: (state) => state.state?.current_phase || 'setup',
    phaseEndsAt: (state) => state.state?.phase_ends_at || null,
    currentAudioText: (state) => state.state?.current_audio_text || '',
    currentRoleTurn: (state) => state.state?.current_role_turn || null,
    isGameOver: (state) => Boolean(state.state?.is_game_over),
  },

  actions: {
    setState(gameState: GameState) {
      this.state = gameState
    },

    clearTurnSensitiveState() {
      this.allowedNightAction = null
      this.lastNightActionResult = null
    },

    setAllowedNightAction(payload: NightActionPayload) {
      this.allowedNightAction = payload
      this.lastNightActionResult = null
    },

    setNightActionResult(payload: NightActionResponse) {
      this.lastNightActionResult = payload
    },

    setDayResult(payload: DayStartedPayload) {
      this.dayResult = payload
    },

    setVoteStarted(payload: VoteStartedPayload) {
      this.voteStarted = payload
      this.voteSummary = null
      this.voteEnded = null
    },

    setVoteSummary(payload: VoteSummary) {
      this.voteSummary = payload
    },

    setVoteEnded(payload: VoteEndedPayload) {
      this.voteEnded = payload
    },
  },
})
