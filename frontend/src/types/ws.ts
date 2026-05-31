export interface RealtimeEvent<T = unknown> {
  type: string
  room_code: string
  payload: T
  timestamp: string
}
