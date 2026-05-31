const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://127.0.0.1:8000'

export interface RealtimeEvent {
  type: string
  room_code: string
  payload: any
  timestamp: string
}

export class RoomWebSocket {
  private socket: WebSocket | null = null
  private onEvent: (event: RealtimeEvent) => void

  constructor(onEvent: (event: RealtimeEvent) => void) {
    this.onEvent = onEvent
  }

  connect(roomCode: string, clientType: 'host' | 'player', clientId?: string) {
    this.disconnect()

    const params = new URLSearchParams({
      client_type: clientType,
    })

    if (clientId) {
      params.set('client_id', clientId)
    }

    const url = `${WS_BASE_URL}/ws/rooms/${roomCode}?${params.toString()}`
    this.socket = new WebSocket(url)

    this.socket.onopen = () => {
      console.log('WebSocket connected')
      this.send({
        type: 'CLIENT_READY',
      })
    }

    this.socket.onmessage = (message) => {
      try {
        const event = JSON.parse(message.data)
        this.onEvent(event)
      } catch (error) {
        console.error('Invalid WebSocket message', error)
      }
    }

    this.socket.onerror = (error) => {
      console.error('WebSocket error', error)
    }

    this.socket.onclose = () => {
      console.log('WebSocket closed')
    }
  }

  send(data: Record<string, unknown>) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      return
    }

    this.socket.send(JSON.stringify(data))
  }

  disconnect() {
    if (this.socket) {
      this.socket.close()
      this.socket = null
    }
  }
}