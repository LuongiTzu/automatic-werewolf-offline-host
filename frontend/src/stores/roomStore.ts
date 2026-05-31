import { defineStore } from 'pinia'
import { api, type PlayerRole } from '@/services/api'
import type {
  DayStartedPayload,
  GameLogItem,
  GameState,
  NightActionPayload,
  NightActionResponse,
  SubmitNightActionRequest,
  VoteEndedPayload,
  VoteStartedPayload,
  VoteSummary,
} from '@/types/game'
import type { PlayerInRoom } from '@/types/player'
import type { RoleCartResponse, RoleResponse } from '@/types/room'
import { RoomWebSocket, type ConnectionStatus, type RealtimeEvent } from '@/services/websocket'

interface RoomState {
  roomId: string
  roomCode: string
  hostToken: string
  playerId: string
  playerName: string
  sessionToken: string
  status: string
  currentPhase: string
  nightNumber: number
  dayNumber: number
  currentRoleTurn: string
  phaseEndsAt: string
  currentAudioText: string
  isPaused: boolean
  isGameOver: boolean
  winner: string
  players: PlayerInRoom[]
  roles: RoleResponse[]
  roleCart: RoleCartResponse | null
  myRole: PlayerRole | null
  allowedNightAction: NightActionPayload | null
  lastNightActionResult: NightActionResponse | null
  dayResult: DayStartedPayload | null
  voteStarted: VoteStartedPayload | null
  voteSummary: VoteSummary | null
  voteEnded: VoteEndedPayload | null
  gameLogs: GameLogItem[]
  events: RealtimeEvent[]
  error: string
  loading: boolean
  socketStatus: ConnectionStatus
}

let roomSocket: RoomWebSocket | null = null

function stringifyPayload(payload: unknown): string {
  if (typeof payload === 'string') return payload
  try {
    return JSON.stringify(payload, null, 2)
  } catch {
    return String(payload)
  }
}

function normalizeGameState(payload: Partial<GameState>): Partial<RoomState> {
  return {
    roomId: payload.room_id || '',
    roomCode: payload.room_code || '',
    status: payload.status || '',
    currentPhase: String(payload.current_phase || ''),
    nightNumber: payload.night_number || 0,
    dayNumber: payload.day_number || 0,
    currentRoleTurn: payload.current_role_turn || '',
    phaseEndsAt: payload.phase_ends_at || '',
    currentAudioText: payload.current_audio_text || '',
    isPaused: Boolean(payload.is_paused),
    isGameOver: Boolean(payload.is_game_over),
    winner: payload.winner || '',
  }
}

export const useRoomStore = defineStore('room', {
  state: (): RoomState => ({
    roomId: localStorage.getItem('room_id') || '',
    roomCode: localStorage.getItem('room_code') || '',
    hostToken: localStorage.getItem('host_token') || '',
    playerId: localStorage.getItem('player_id') || '',
    playerName: localStorage.getItem('player_name') || '',
    sessionToken: localStorage.getItem('session_token') || '',
    status: '',
    currentPhase: '',
    nightNumber: 0,
    dayNumber: 0,
    currentRoleTurn: '',
    phaseEndsAt: '',
    currentAudioText: '',
    isPaused: false,
    isGameOver: false,
    winner: '',
    players: [],
    roles: [],
    roleCart: null,
    myRole: null,
    allowedNightAction: null,
    lastNightActionResult: null,
    dayResult: null,
    voteStarted: null,
    voteSummary: null,
    voteEnded: null,
    gameLogs: [],
    events: [],
    error: '',
    loading: false,
    socketStatus: 'idle',
  }),

  getters: {
    socketConnected: (state) => state.socketStatus === 'connected',
    alivePlayers: (state) => state.players.filter((player) => player.is_alive),
    me: (state) => state.players.find((player) => player.id === state.playerId) || null,
    isMeAlive: (state) => {
      const me = state.players.find((player) => player.id === state.playerId)
      return me ? me.is_alive : true
    },
  },

  actions: {
    saveSession() {
      localStorage.setItem('room_id', this.roomId)
      localStorage.setItem('room_code', this.roomCode)
      localStorage.setItem('host_token', this.hostToken)
      localStorage.setItem('player_id', this.playerId)
      localStorage.setItem('player_name', this.playerName)
      localStorage.setItem('session_token', this.sessionToken)
    },

    clearSession() {
      this.roomId = ''
      this.roomCode = ''
      this.hostToken = ''
      this.playerId = ''
      this.playerName = ''
      this.sessionToken = ''
      this.myRole = null
      localStorage.removeItem('room_id')
      localStorage.removeItem('room_code')
      localStorage.removeItem('host_token')
      localStorage.removeItem('player_id')
      localStorage.removeItem('player_name')
      localStorage.removeItem('session_token')
    },

    setError(error: unknown, fallback: string) {
      this.error = error instanceof Error ? error.message : fallback
    },

    async createRoom() {
      this.loading = true
      this.error = ''
      try {
        const room = await api.createRoom()
        this.roomId = room.room_id
        this.roomCode = room.room_code
        this.hostToken = room.host_token
        this.status = room.status
        this.saveSession()
        await this.loadRoom()
        await this.loadRoles()
        await this.loadRoleCart()
        this.connectWebSocket('host')
      } catch (error) {
        this.setError(error, 'Create room failed')
      } finally {
        this.loading = false
      }
    },

    async loadRoom() {
      if (!this.roomCode) return
      const room = await api.getRoom(this.roomCode)
      this.roomId = room.id
      this.roomCode = room.room_code
      this.status = room.status
      this.currentPhase = room.current_phase
      this.nightNumber = room.night_number
      this.dayNumber = room.day_number
      this.currentRoleTurn = room.current_role_turn || ''
      this.phaseEndsAt = room.phase_ends_at || ''
      this.currentAudioText = room.current_audio_text || ''
      this.isPaused = Boolean(room.is_paused)
      this.isGameOver = Boolean(room.is_game_over)
      this.winner = room.winner || ''
      this.players = room.players
      this.saveSession()
    },

    async joinRoom(roomCode: string, name: string) {
      this.loading = true
      this.error = ''
      try {
        const result = await api.joinRoom(roomCode.trim().toUpperCase(), name.trim())
        this.roomId = result.room_id
        this.roomCode = result.room_code
        this.playerId = result.player_id
        this.playerName = result.player_name
        this.sessionToken = result.session_token
        this.status = result.status
        this.saveSession()
        await this.loadRoom()
        this.connectWebSocket('player')
      } catch (error) {
        this.setError(error, 'Join room failed')
      } finally {
        this.loading = false
      }
    },

    async loadRoles() {
      this.roles = await api.getRoles()
    },

    async loadRoleCart() {
      if (!this.roomCode) return
      this.roleCart = await api.getRoleCart(this.roomCode)
    },

    async setRoleQuantity(roleCode: string, quantity: number) {
      if (!this.roomCode) return
      const currentRoles = new Map<string, number>()
      if (this.roleCart) {
        for (const item of this.roleCart.cart) currentRoles.set(item.role_code, item.quantity)
      }
      currentRoles.set(roleCode, Math.max(0, quantity))
      const roles = Array.from(currentRoles.entries()).map(([role_code, qty]) => ({ role_code, quantity: qty }))
      this.roleCart = await api.updateRoleCart(this.roomCode, roles)
    },

    async startGame() {
      if (!this.roomCode) return
      this.loading = true
      this.error = ''
      try {
        const result = await api.startGame(this.roomCode)
        this.status = result.status
        this.currentPhase = result.current_phase
        this.nightNumber = result.night_number
        this.dayNumber = result.day_number
        this.players = result.players
        await this.startAutoGame()
      } catch (error) {
        this.setError(error, 'Start game failed')
      } finally {
        this.loading = false
      }
    },

    async startAutoGame() {
      if (!this.roomId || !this.hostToken) return
      await api.startAutoGame(this.roomId, this.hostToken)
      await this.loadGameState()
    },

    async pauseGame() {
      if (!this.roomId || !this.hostToken) return
      await api.pauseAutoGame(this.roomId, this.hostToken)
    },

    async resumeGame() {
      if (!this.roomId || !this.hostToken) return
      await api.resumeAutoGame(this.roomId, this.hostToken)
    },

    async stopGame() {
      if (!this.roomId || !this.hostToken) return
      await api.stopAutoGame(this.roomId, this.hostToken)
    },

    async kickPlayer(playerId: string) {
      if (!this.roomId || !this.hostToken) return
      await api.kickPlayer(this.roomId, playerId, this.hostToken)
      await this.loadRoom()
      await this.loadRoleCart()
    },

    async loadGameState() {
      if (!this.roomId) return
      const state = await api.getGameState(this.roomId)
      this.applyGameState(state)
    },

    async loadMyRole() {
      if (!this.playerId || !this.sessionToken) return
      this.myRole = await api.getMyRole(this.playerId, this.sessionToken)
    },

    async submitNightAction(actionType: string, targetPlayerId?: string | null, targetPlayerIds?: string[] | null) {
      if (!this.roomId || !this.playerId || !this.sessionToken) return
      this.error = ''
      const payload: SubmitNightActionRequest = {
        player_id: this.playerId,
        session_token: this.sessionToken,
        action_type: actionType,
        target_player_id: targetPlayerId || null,
        target_player_ids: targetPlayerIds || null,
      }
      try {
        this.lastNightActionResult = await api.submitNightAction(this.roomId, payload)
      } catch (error) {
        this.setError(error, 'Submit night action failed')
      }
    },

    async submitVote(targetPlayerId: string) {
      if (!this.roomId || !this.playerId || !this.sessionToken) return
      this.error = ''
      try {
        this.voteSummary = await api.submitVote(this.roomId, {
          voter_player_id: this.playerId,
          session_token: this.sessionToken,
          target_player_id: targetPlayerId,
        })
      } catch (error) {
        this.setError(error, 'Submit vote failed')
      }
    },

    async loadGameLogs() {
      if (!this.roomId || !this.hostToken || !this.isGameOver) return
      try {
        const result = await api.getLogs(this.roomId, this.hostToken)
        this.gameLogs = result.logs
      } catch (error) {
        this.setError(error, 'Load game logs failed')
      }
    },

    connectWebSocket(clientType: 'host' | 'player') {
      if (!this.roomCode) return
      roomSocket?.disconnect()
      roomSocket = new RoomWebSocket(
        (event) => this.handleRealtimeEvent(event),
        (status) => {
          this.socketStatus = status
        },
      )
      roomSocket.connect(this.roomCode, clientType, clientType === 'player' ? this.playerId : undefined)
    },

    disconnectWebSocket() {
      roomSocket?.disconnect()
      roomSocket = null
      this.socketStatus = 'idle'
    },

    applyGameState(payload: Partial<GameState>) {
      const normalized = normalizeGameState(payload)
      if (normalized.roomId) this.roomId = normalized.roomId
      if (normalized.roomCode) this.roomCode = normalized.roomCode
      if (normalized.status) this.status = normalized.status
      if (normalized.currentPhase) this.currentPhase = normalized.currentPhase
      this.nightNumber = normalized.nightNumber || this.nightNumber
      this.dayNumber = normalized.dayNumber || this.dayNumber
      this.currentRoleTurn = normalized.currentRoleTurn || ''
      this.phaseEndsAt = normalized.phaseEndsAt || ''
      this.currentAudioText = normalized.currentAudioText || ''
      this.isPaused = normalized.isPaused || false
      this.isGameOver = normalized.isGameOver || false
      this.winner = normalized.winner || ''
      this.saveSession()
    },

    handleRealtimeEvent(event: RealtimeEvent) {
      this.events.unshift({
        ...event,
        payload: stringifyPayload(event.payload),
      })

      if (this.events.length > 60) this.events.pop()

      if (event.type === 'CONNECTION_ESTABLISHED') {
        this.socketStatus = 'connected'
        return
      }

      if (event.type === 'PLAYER_JOINED' || event.type === 'PLAYER_KICKED' || event.type === 'CLIENT_DISCONNECTED') {
        void this.loadRoom()
        void this.loadRoleCart()
      }

      if (event.type === 'ROLE_CART_UPDATED') {
        this.roleCart = event.payload as RoleCartResponse
      }

      if (event.type === 'GAME_STARTED') {
        const payload = event.payload as { status?: string; current_phase?: string; night_number?: number; day_number?: number; players?: PlayerInRoom[] }
        this.status = payload.status || this.status
        this.currentPhase = payload.current_phase || this.currentPhase
        this.nightNumber = payload.night_number || this.nightNumber
        this.dayNumber = payload.day_number || this.dayNumber
        if (payload.players) this.players = payload.players
        if (this.playerId) void this.loadMyRole()
      }

      if (event.type === 'PHASE_CHANGED' || event.type === 'GAME_PAUSED' || event.type === 'GAME_RESUMED') {
        this.applyGameState(event.payload as Partial<GameState>)
        if (this.currentPhase !== 'night_role_turn') this.allowedNightAction = null
      }

      if (event.type === 'PLAYER_WAKE_ALLOWED') {
        this.allowedNightAction = event.payload as NightActionPayload
        this.lastNightActionResult = null
      }

      if (event.type === 'PLAYER_SLEEP') {
        this.allowedNightAction = null
      }

      if (event.type === 'ACTION_RECEIVED') {
        const result = event.payload as NightActionResponse
        if (result.action_type) this.lastNightActionResult = result
      }

      if (event.type === 'DAY_STARTED') {
        this.dayResult = event.payload as DayStartedPayload
        this.allowedNightAction = null
        void this.loadRoom()
      }

      if (event.type === 'VOTE_STARTED') {
        this.voteStarted = event.payload as VoteStartedPayload
        this.voteSummary = null
        this.voteEnded = null
      }

      if (event.type === 'VOTE_UPDATED') {
        this.voteSummary = event.payload as VoteSummary
      }

      if (event.type === 'VOTE_ENDED') {
        this.voteEnded = event.payload as VoteEndedPayload
        void this.loadRoom()
      }

      if (event.type === 'GAME_OVER') {
        this.currentPhase = 'ended'
        this.isGameOver = true
        const payload = event.payload as Partial<GameState> & { audio_text?: string }
        this.winner = payload.winner || this.winner
        this.currentAudioText = payload.current_audio_text || payload.audio_text || this.currentAudioText
        void this.loadRoom()
      }
    },
  },
})
