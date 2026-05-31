import { defineStore } from 'pinia'
import type { PlayerRole } from '@/types/player'

interface PlayerStoreState {
  playerId: string
  playerName: string
  sessionToken: string
  myRole: PlayerRole | null
  isAlive: boolean
}

export const usePlayerStore = defineStore('player', {
  state: (): PlayerStoreState => ({
    playerId: localStorage.getItem('player_id') || '',
    playerName: localStorage.getItem('player_name') || '',
    sessionToken: localStorage.getItem('session_token') || '',
    myRole: null,
    isAlive: true,
  }),

  actions: {
    setSession(playerId: string, playerName: string, sessionToken: string) {
      this.playerId = playerId
      this.playerName = playerName
      this.sessionToken = sessionToken
      localStorage.setItem('player_id', playerId)
      localStorage.setItem('player_name', playerName)
      localStorage.setItem('session_token', sessionToken)
    },

    setRole(role: PlayerRole) {
      this.myRole = role
    },

    clear() {
      this.playerId = ''
      this.playerName = ''
      this.sessionToken = ''
      this.myRole = null
      localStorage.removeItem('player_id')
      localStorage.removeItem('player_name')
      localStorage.removeItem('session_token')
    },
  },
})
