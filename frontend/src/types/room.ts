import type { PlayerInRoom } from './player'

export interface CreateRoomResponse {
  room_id: string
  room_code: string
  host_token: string
  status: string
  created_at: string
}

export interface JoinRoomResponse {
  player_id: string
  session_token: string
  room_code: string
  room_id: string
  player_name: string
  player_count: number
  status: string
}

export interface RoomInfoResponse {
  id: string
  room_code: string
  status: string
  current_phase: string
  night_number: number
  day_number: number
  current_role_turn?: string | null
  phase_ends_at?: string | null
  current_audio_text?: string | null
  is_paused?: boolean
  is_game_over?: boolean
  winner?: string | null
  players: PlayerInRoom[]
  player_count: number
  created_at: string
}

export interface RoleResponse {
  code: string
  name: string
  side: string
  description: string
  night_order: number | null
  is_active: boolean
}

export interface RoleCartItem {
  role_code: string
  name: string
  quantity: number
}

export interface RoleCartResponse {
  room_code: string
  room_id: string
  cart: RoleCartItem[]
  total_roles: number
  total_players: number
  can_start: boolean
}
