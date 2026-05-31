// Game types
export interface Player {
  id: string
  name: string
  roomId: string
  role: string | null
  isAlive: boolean
  isConnected: boolean
}

export interface Room {
  id: string
  code: string
  hostToken: string
  status: 'waiting' | 'playing' | 'ended'
  currentPhase: 'setup' | 'night' | 'day' | 'vote' | 'ended'
  players: Player[]
}

export type GamePhase = 'setup' | 'night' | 'day' | 'vote' | 'ended'
export type PlayerRole = 'werewolf' | 'villager' | 'protector' | 'seer' | 'witch'
