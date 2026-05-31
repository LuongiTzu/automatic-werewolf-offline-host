import type { RealtimeEvent } from '@/types/ws'

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://127.0.0.1:8000'

export type ClientType = 'host' | 'player'
export type ConnectionStatus = 'idle' | 'connecting' | 'connected' | 'closed' | 'error'

export class RoomWebSocket {
  private socket: WebSocket | null = null
  private reconnectTimer: number | null = null
  private readonly onEvent: (event: RealtimeEvent) => void
  private readonly onStatus?: (status: ConnectionStatus) => void

  constructor(onEvent: (event: RealtimeEvent) => void, onStatus?: (status: ConnectionStatus) => void) {
    this.onEvent = onEvent
    this.onStatus = onStatus
  }

  connect(roomCode: string, clientType: ClientType, clientId?: string): void {
    this.disconnect()
    this.setStatus('connecting')

    const params = new URLSearchParams({ client_type: clientType })
    if (clientId) params.set('client_id', clientId)

    const url = `${WS_BASE_URL}/ws/rooms/${encodeURIComponent(roomCode)}?${params.toString()}`
    this.socket = new WebSocket(url)

    this.socket.onopen = () => {
      this.setStatus('connected')
      this.send({ type: 'CLIENT_READY' })
    }

    this.socket.onmessage = (message) => {
      try {
        this.onEvent(JSON.parse(message.data) as RealtimeEvent)
      } catch (error) {
        console.error('Invalid WebSocket message', error)
      }
    }

    this.socket.onerror = () => {
      this.setStatus('error')
    }

    this.socket.onclose = () => {
      this.setStatus('closed')
    }
  }

  send(data: Record<string, unknown>): void {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return
    this.socket.send(JSON.stringify(data))
  }

  disconnect(): void {
    if (this.reconnectTimer) {
      window.clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }

    if (this.socket) {
      this.socket.close()
      this.socket = null
    }

    this.setStatus('idle')
  }

  private setStatus(status: ConnectionStatus): void {
    this.onStatus?.(status)
  }
}

export type { RealtimeEvent }
