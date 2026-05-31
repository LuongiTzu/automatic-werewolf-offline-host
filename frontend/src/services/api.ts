const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })

  if (!response.ok) {
    let message = `HTTP ${response.status}`

    try {
      const data = await response.json()
      message = data.detail || message
    } catch {
      // Ignore JSON parse error
    }

    throw new Error(message)
  }

  return response.json()
}

export interface PlayerInRoom {
  id: string
  name: string
  is_alive: boolean
  is_connected: boolean
}

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

export interface StartGameResponse {
  room_code: string
  room_id: string
  status: string
  current_phase: string
  night_number: number
  day_number: number
  total_players: number
  message: string
  players: PlayerInRoom[]
}

export interface PlayerRoleResponse {
  player_id: string
  player_name: string
  room_id: string
  role_code: string
  role_name: string
  side: string
  description?: string
  night_order?: number
}

export const api = {
  createRoom() {
    return request<CreateRoomResponse>('/api/rooms/', {
      method: 'POST',
    })
  },

  getRoom(roomCode: string) {
    return request<RoomInfoResponse>(`/api/rooms/${roomCode}`)
  },

  joinRoom(roomCode: string, name: string) {
    return request<JoinRoomResponse>(`/api/rooms/${roomCode}/join`, {
      method: 'POST',
      body: JSON.stringify({ name }),
    })
  },

  getRoles() {
    return request<RoleResponse[]>('/api/roles/')
  },

  getRoleCart(roomCode: string) {
    return request<RoleCartResponse>(`/api/rooms/${roomCode}/role-cart`)
  },

  updateRoleCart(roomCode: string, roles: { role_code: string; quantity: number }[]) {
    return request<RoleCartResponse>(`/api/rooms/${roomCode}/role-cart`, {
      method: 'PUT',
      body: JSON.stringify({ roles }),
    })
  },

  startGame(roomCode: string) {
    return request<StartGameResponse>(`/api/rooms/${roomCode}/start`, {
      method: 'POST',
    })
  },

  getMyRole(playerId: string, sessionToken: string) {
    const token = encodeURIComponent(sessionToken)
    return request<PlayerRoleResponse>(`/api/players/${playerId}/role?session_token=${token}`)
  },
}