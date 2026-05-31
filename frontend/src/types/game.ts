import type { NightTarget, PlayerInRoom } from './player'

export type GamePhase =
  | 'setup'
  | 'role_reveal'
  | 'night_start'
  | 'night_role_turn'
  | 'night_resolving'
  | 'day_result'
  | 'day_discussion'
  | 'voting'
  | 'vote_result'
  | 'paused'
  | 'ended'
  | 'night'
  | 'day'
  | 'vote'

export interface GameState {
  room_id: string
  room_code: string
  status: string
  current_phase: GamePhase | string
  night_number: number
  day_number: number
  current_role_turn?: string | null
  phase_ends_at?: string | null
  current_audio_text?: string | null
  is_paused: boolean
  is_game_over: boolean
  winner?: string | null
}

export interface StartedPlayerResponse extends PlayerInRoom {}

export interface StartGameResponse {
  room_code: string
  room_id: string
  status: string
  current_phase: string
  night_number: number
  day_number: number
  total_players: number
  message: string
  players: StartedPlayerResponse[]
}

export interface NightActionPayload {
  role_code: string
  night_number: number
  phase_ends_at?: string | null
  targets: NightTarget[]
}

export interface SubmitNightActionRequest {
  player_id: string
  session_token: string
  action_type: string
  target_player_id?: string | null
  target_player_ids?: string[] | null
}

export interface NightActionResponse {
  action_id?: string
  action_type: string
  actor_player_id?: string
  private_result?: {
    target_player_id: string
    target_name: string
    result: string
  } | null
}

export interface DayStartedPayload {
  day_number: number
  dead_players: NightTarget[]
}

export interface VoteStartedPayload {
  day_number: number
  seconds: number
  targets: NightTarget[]
}

export interface VoteSummary {
  day_number: number
  total_alive: number
  total_votes: number
  ranking: Array<{
    player_id: string
    player_name: string
    votes: number
  }>
  voted_player_ids: string[]
}

export interface VoteEndedPayload {
  day_number?: number
  eliminated_player?: NightTarget | null
  eliminated_players?: NightTarget[]
  message: string
  is_tie?: boolean
  ranking?: VoteSummary['ranking']
}

export interface GameLogItem {
  id: string
  night_number?: number | null
  day_number?: number | null
  event_type: string
  message: string
  data: Record<string, unknown>
  created_at?: string | null
}

export function phaseLabel(phase?: string | null): string {
  const map: Record<string, string> = {
    setup: 'Setup',
    role_reveal: 'Xem role',
    night_start: 'Trời tối',
    night_role_turn: 'Lượt role',
    night_resolving: 'Xử lý ban đêm',
    day_result: 'Trời sáng',
    day_discussion: 'Thảo luận',
    voting: 'Bỏ phiếu',
    vote_result: 'Kết quả vote',
    paused: 'Tạm dừng',
    ended: 'Kết thúc',
    night: 'Ban đêm',
    day: 'Ban ngày',
    vote: 'Vote',
  }
  return phase ? map[phase] || phase : 'Chưa rõ'
}

export function winnerLabel(winner?: string | null): string {
  const map: Record<string, string> = {
    villagers: 'Phe Dân Làng',
    werewolves: 'Phe Ma Sói',
    fool: 'Thằng Khờ',
    oilman: 'Kẻ Tẩm Dầu',
    lovers: 'Phe Người Yêu',
  }
  return winner ? map[winner] || winner : 'Chưa có'
}
