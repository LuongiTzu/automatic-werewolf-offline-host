import type {
  DayStartedPayload,
  GameLogItem,
  GameState,
  NightActionResponse,
  StartGameResponse,
  SubmitNightActionRequest,
  VoteEndedPayload,
  VoteStartedPayload,
  VoteSummary,
} from '@/types/game'
import type { PlayerRole } from '@/types/player'
import type {
  CreateRoomResponse,
  JoinRoomResponse,
  RoleCartResponse,
  RoleResponse,
  RoomInfoResponse,
} from '@/types/room'

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
      if (typeof data.detail === 'string') message = data.detail
      else if (Array.isArray(data.detail)) message = data.detail.map((item: { msg?: string }) => item.msg || 'Validation error').join(', ')
    } catch {
      // Keep default message.
    }

    throw new Error(message)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export const api = {
  createRoom() {
    return request<CreateRoomResponse>('/api/rooms/', { method: 'POST' })
  },

  getRoom(roomCode: string) {
    return request<RoomInfoResponse>(`/api/rooms/${encodeURIComponent(roomCode)}`)
  },

  joinRoom(roomCode: string, name: string) {
    return request<JoinRoomResponse>(`/api/rooms/${encodeURIComponent(roomCode)}/join`, {
      method: 'POST',
      body: JSON.stringify({ name }),
    })
  },

  kickPlayer(roomId: string, playerId: string, hostToken: string) {
    return request<{ message: string; player_id: string }>(
      `/api/rooms/${encodeURIComponent(roomId)}/players/${encodeURIComponent(playerId)}`,
      {
        method: 'DELETE',
        headers: { 'X-Host-Token': hostToken },
      },
    )
  },

  getRoles() {
    return request<RoleResponse[]>('/api/roles/')
  },

  getRoleCart(roomCode: string) {
    return request<RoleCartResponse>(`/api/rooms/${encodeURIComponent(roomCode)}/role-cart`)
  },

  updateRoleCart(roomCode: string, roles: { role_code: string; quantity: number }[]) {
    return request<RoleCartResponse>(`/api/rooms/${encodeURIComponent(roomCode)}/role-cart`, {
      method: 'PUT',
      body: JSON.stringify({ roles }),
    })
  },

  startGame(roomCode: string) {
    return request<StartGameResponse>(`/api/rooms/${encodeURIComponent(roomCode)}/start`, {
      method: 'POST',
    })
  },

  startAutoGame(roomId: string, hostToken: string) {
    return request<{ message: string; room_code: string }>(`/api/rooms/${encodeURIComponent(roomId)}/auto/start`, {
      method: 'POST',
      body: JSON.stringify({ host_token: hostToken }),
    })
  },

  pauseAutoGame(roomId: string, hostToken: string) {
    return request<{ message: string }>(`/api/rooms/${encodeURIComponent(roomId)}/auto/pause`, {
      method: 'POST',
      body: JSON.stringify({ host_token: hostToken }),
    })
  },

  resumeAutoGame(roomId: string, hostToken: string) {
    return request<{ message: string }>(`/api/rooms/${encodeURIComponent(roomId)}/auto/resume`, {
      method: 'POST',
      body: JSON.stringify({ host_token: hostToken }),
    })
  },

  stopAutoGame(roomId: string, hostToken: string) {
    return request<{ message: string }>(`/api/rooms/${encodeURIComponent(roomId)}/auto/stop`, {
      method: 'POST',
      body: JSON.stringify({ host_token: hostToken }),
    })
  },

  getGameState(roomId: string) {
    return request<GameState>(`/api/rooms/${encodeURIComponent(roomId)}/state`)
  },

  submitNightAction(roomId: string, payload: SubmitNightActionRequest) {
    return request<NightActionResponse>(`/api/rooms/${encodeURIComponent(roomId)}/night/action`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  submitVote(roomId: string, payload: { voter_player_id: string; session_token: string; target_player_id: string }) {
    return request<VoteSummary>(`/api/rooms/${encodeURIComponent(roomId)}/vote`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  getMyRole(playerId: string, sessionToken: string) {
    const token = encodeURIComponent(sessionToken)
    return request<PlayerRole>(`/api/players/${encodeURIComponent(playerId)}/role?session_token=${token}`)
  },

  getLogs(roomId: string, hostToken: string) {
    return request<{ logs: GameLogItem[] }>(`/api/rooms/${encodeURIComponent(roomId)}/logs`, {
      headers: { 'X-Host-Token': hostToken },
    })
  },
}

export type {
  CreateRoomResponse,
  DayStartedPayload,
  GameLogItem,
  GameState,
  JoinRoomResponse,
  NightActionResponse,
  PlayerRole,
  RoleCartResponse,
  RoleResponse,
  RoomInfoResponse,
  StartGameResponse,
  SubmitNightActionRequest,
  VoteEndedPayload,
  VoteStartedPayload,
  VoteSummary,
}
