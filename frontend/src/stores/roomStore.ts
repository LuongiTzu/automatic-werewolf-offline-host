import { defineStore } from 'pinia'
import { api, type PlayerInRoom, type RoleResponse, type RoleCartResponse, type PlayerRoleResponse } from '../services/api'
import { RoomWebSocket, type RealtimeEvent } from '../services/websocket'

interface RoomState {
  roomId: string
  roomCode: string
  hostToken: string
  playerId: string
  playerName: string
  sessionToken: string
  status: string
  currentPhase: string
  players: PlayerInRoom[]
  roles: RoleResponse[]
  roleCart: RoleCartResponse | null
  myRole: PlayerRoleResponse | null
  events: RealtimeEvent[]
  error: string
  loading: boolean
  socketConnected: boolean
}

let roomSocket: RoomWebSocket | null = null

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
    players: [],
    roles: [],
    roleCart: null,
    myRole: null,
    events: [],
    error: '',
    loading: false,
    socketConnected: false,
  }),

  actions: {
    saveSession() {
      localStorage.setItem('room_id', this.roomId)
      localStorage.setItem('room_code', this.roomCode)
      localStorage.setItem('host_token', this.hostToken)
      localStorage.setItem('player_id', this.playerId)
      localStorage.setItem('player_name', this.playerName)
      localStorage.setItem('session_token', this.sessionToken)
    },

    clearError() {
      this.error = ''
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
      } catch (error: any) {
        this.error = error.message || 'Create room failed'
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
      this.players = room.players
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
      } catch (error: any) {
        this.error = error.message || 'Join room failed'
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
        for (const item of this.roleCart.cart) {
          currentRoles.set(item.role_code, item.quantity)
        }
      }

      currentRoles.set(roleCode, Math.max(0, quantity))

      const roles = Array.from(currentRoles.entries()).map(([role_code, qty]) => ({
        role_code,
        quantity: qty,
      }))

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
        this.players = result.players
      } catch (error: any) {
        this.error = error.message || 'Start game failed'
      } finally {
        this.loading = false
      }
    },

    async loadMyRole() {
      if (!this.playerId || !this.sessionToken) return

      this.myRole = await api.getMyRole(this.playerId, this.sessionToken)
    },

    connectWebSocket(clientType: 'host' | 'player') {
      if (!this.roomCode) return

      roomSocket = new RoomWebSocket((event) => {
        this.handleRealtimeEvent(event)
      })

      roomSocket.connect(
        this.roomCode,
        clientType,
        clientType === 'player' ? this.playerId : undefined,
      )

      this.socketConnected = true
    },

    handleRealtimeEvent(event: RealtimeEvent) {
      this.events.unshift(event)

      if (this.events.length > 20) {
        this.events.pop()
      }

      if (event.type === 'CONNECTION_ESTABLISHED') {
        this.socketConnected = true
      }

      if (event.type === 'PLAYER_JOINED') {
        this.loadRoom()
        this.loadRoleCart()
      }

      if (event.type === 'ROLE_CART_UPDATED') {
        this.roleCart = event.payload
      }

      if (event.type === 'GAME_STARTED') {
        this.status = event.payload.status
        this.currentPhase = event.payload.current_phase
        this.players = event.payload.players || this.players
      }
    },
  },
})