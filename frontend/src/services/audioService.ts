/**
 * Host audio service for the Werewolf realtime game.
 *
 * Supports:
 * - Browser Text-To-Speech.
 * - Optional MP3 narration files from /audio.
 * - Optional looping night ambient sound.
 * - Replay current sentence.
 * - Safe fallback: even if audio fails, the current text remains visible on Host UI.
 */

export type AudioKey =
  | 'GAME_START'
  | 'NIGHT_SLEEP'
  | 'DAY_WAKE'
  | 'WEREWOLF_WAKE'
  | 'GUARD_WAKE'
  | 'WITCH_WAKE'
  | 'HUNTER_WAKE'
  | 'SEER_WAKE'
  | 'CUPID_WAKE'
  | 'OILMAN_WAKE'
  | 'GUARD_CHOOSE'
  | 'SEER_CHOOSE'
  | 'WITCH_CHOOSE'
  | 'ROLE_DONE_SLEEP'
  | 'DISCUSSION_ALMOST_END'
  | 'DISCUSSION_END'
  | 'VOTE_REQUEST'
  | 'PLAYER_DEAD_ANNOUNCE'
  | 'GAME_END'
  | 'WIN_VILLAGER'
  | 'WIN_WEREWOLF'
  | 'WIN_FOOL'
  | 'WIN_OILMAN'
  | 'WIN_CUPID'

const AUDIO_FILES: Partial<Record<AudioKey, string>> = {
  GAME_START: '/audio/thongbaotrochoistart.mp3',
  NIGHT_SLEEP: '/audio/thongbaodingu.mp3',
  DAY_WAKE: '/audio/thongbaotroisang.mp3',
  WEREWOLF_WAKE: '/audio/thongbaosoiday.mp3',
  GUARD_WAKE: '/audio/thongbaobaoveday.mp3',
  WITCH_WAKE: '/audio/thongbaophuthuyday.mp3',
  HUNTER_WAKE: '/audio/thongbaothosanday.mp3',
  SEER_WAKE: '/audio/thongbaotientriday.mp3',
  CUPID_WAKE: '/audio/thongbaocupidday.mp3',
  OILMAN_WAKE: '/audio/thongbaotamdauiday.mp3',
  GUARD_CHOOSE: '/audio/yeucau_baovechon.mp3',
  SEER_CHOOSE: '/audio/yeucau_tientrichon.mp3',
  WITCH_CHOOSE: '/audio/yeucau_phuthuychon.mp3',
  ROLE_DONE_SLEEP: '/audio/thongbao_dalamxongrole_yeucaudingu_dungchungchotatca.mp3',
  DISCUSSION_ALMOST_END: '/audio/thongbaosaphettthoigian.mp3',
  DISCUSSION_END: '/audio/thongbaohetgiothaoluan.mp3',
  VOTE_REQUEST: '/audio/yeucauvote.mp3',
  PLAYER_DEAD_ANNOUNCE: '/audio/thongbaonguoibichet.mp3',
  GAME_END: '/audio/thongbaoendgame.mp3',
  WIN_VILLAGER: '/audio/baochienthangdanlang.mp3',
  WIN_WEREWOLF: '/audio/baochienthangsoi.mp3',
  WIN_FOOL: '/audio/baochienthangthangkho.mp3',
  WIN_OILMAN: '/audio/baochienthangtamdau.mp3',
  WIN_CUPID: '/audio/baochienthangcupid.mp3',
}

const FALLBACK_TEXT: Record<AudioKey, string> = {
  GAME_START: 'Trò chơi bắt đầu. Hệ thống sẽ tự động quản trò.',
  NIGHT_SLEEP: 'Trời tối rồi. Tất cả người chơi hãy nhắm mắt lại.',
  DAY_WAKE: 'Trời sáng rồi. Tất cả người chơi hãy mở mắt.',
  WEREWOLF_WAKE: 'Ma Sói thức dậy. Ma Sói hãy nhìn nhau và chọn một người để cắn.',
  GUARD_WAKE: 'Bảo vệ thức dậy. Bảo vệ hãy chọn một người để bảo vệ trong đêm nay.',
  WITCH_WAKE: 'Phù thủy thức dậy. Hãy xem thông tin trong đêm và chọn dùng bình nếu muốn.',
  HUNTER_WAKE: 'Thợ săn thức dậy. Thợ săn hãy chọn một người để kéo theo nếu bản thân bị chết.',
  SEER_WAKE: 'Tiên tri thức dậy. Tiên tri hãy chọn một người để soi.',
  CUPID_WAKE: 'Cupid thức dậy. Cupid hãy chọn hai người để ghép đôi.',
  OILMAN_WAKE: 'Kẻ tẩm dầu thức dậy. Kẻ tẩm dầu hãy chọn tối đa hai người để tẩm dầu.',
  GUARD_CHOOSE: 'Bảo vệ hãy chọn một người để bảo vệ trong đêm nay.',
  SEER_CHOOSE: 'Tiên tri hãy chọn một người để soi.',
  WITCH_CHOOSE: 'Phù thủy hãy chọn hành động của mình.',
  ROLE_DONE_SLEEP: 'Role đã chọn xong. Hãy đi ngủ.',
  DISCUSSION_ALMOST_END: 'Sắp hết thời gian thảo luận.',
  DISCUSSION_END: 'Thời gian thảo luận đã kết thúc. Tất cả người chơi chuẩn bị bỏ phiếu.',
  VOTE_REQUEST: 'Bắt đầu bỏ phiếu treo cổ.',
  PLAYER_DEAD_ANNOUNCE: 'Hệ thống đang công bố người chết trong đêm.',
  GAME_END: 'Trò chơi kết thúc.',
  WIN_VILLAGER: 'Trò chơi kết thúc. Phe Dân Làng chiến thắng.',
  WIN_WEREWOLF: 'Trò chơi kết thúc. Phe Ma Sói chiến thắng.',
  WIN_FOOL: 'Trò chơi kết thúc. Thằng Khờ chiến thắng.',
  WIN_OILMAN: 'Trò chơi kết thúc. Kẻ Tẩm Dầu chiến thắng.',
  WIN_CUPID: 'Trò chơi kết thúc. Phe Người Yêu chiến thắng.',
}

export type AudioStatus = 'idle' | 'ready' | 'playing' | 'speaking' | 'error'

export interface AudioState {
  status: AudioStatus
  lastAudioKey: AudioKey | null
  lastText: string
  currentFile: string
  voiceVolume: number
  ambientVolume: number
  isReady: boolean
  isSpeechEnabled: boolean
  isAmbientEnabled: boolean
  isSpeaking: boolean
  isFileAudioEnabled: boolean
  error: string | null
}

class AudioService {
  private state: AudioState = {
    status: 'idle',
    lastAudioKey: null,
    lastText: '',
    currentFile: '',
    voiceVolume: 1,
    ambientVolume: 0.35,
    isReady: false,
    isSpeechEnabled: false,
    isAmbientEnabled: false,
    isSpeaking: false,
    isFileAudioEnabled: true,
    error: null,
  }

  private narrationAudio: HTMLAudioElement | null = null
  private ambientAudio: HTMLAudioElement | null = null
  private ambientContext: AudioContext | null = null
  private ambientGain: GainNode | null = null
  private ambientSource: AudioBufferSourceNode | null = null
  private synth: SpeechSynthesis | null = null
  private listeners = new Set<(state: AudioState) => void>()

  getState(): AudioState {
    return { ...this.state }
  }

  subscribe(listener: (state: AudioState) => void): () => void {
    this.listeners.add(listener)
    listener(this.getState())

    return () => {
      this.listeners.delete(listener)
    }
  }

  private notify(): void {
    const snapshot = this.getState()
    this.listeners.forEach((listener) => listener(snapshot))
  }

  async initAudio(): Promise<void> {
    this.state.error = null

    if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) {
      this.state.isReady = false
      this.state.status = 'error'
      this.state.error =
        'Trình duyệt không hỗ trợ Text-To-Speech. Host vẫn có thể đọc thủ công câu hiển thị.'
      this.notify()
      return
    }

    this.synth = window.speechSynthesis

    this.narrationAudio = new Audio()
    this.narrationAudio.volume = this.state.voiceVolume

    this.narrationAudio.onplay = () => {
      this.state.status = 'playing'
      this.state.isSpeaking = true
      this.notify()
    }

    this.narrationAudio.onended = () => {
      this.state.status = 'ready'
      this.state.isSpeaking = false
      this.notify()
    }

    this.narrationAudio.onerror = () => {
      const text = this.state.lastText

      this.state.currentFile = ''
      this.state.status = 'error'
      this.state.isSpeaking = false
      this.state.error = 'Không phát được file MP3, đã chuyển sang giọng đọc trình duyệt nếu có.'
      this.notify()

      if (text) {
        void this.speak(text)
      }
    }

    this.ambientAudio = new Audio('/audio/night-ambient.mp3')
    this.ambientAudio.loop = true
    this.ambientAudio.volume = this.state.ambientVolume

    this.state.isReady = true
    this.state.isSpeechEnabled = true
    this.state.status = 'ready'
    this.notify()

    await this.speak('Âm thanh đã sẵn sàng.')
  }

  async testAudio(): Promise<void> {
    await this.speak('Âm thanh đã sẵn sàng.')
  }

  async playNarration(key: AudioKey, text?: string): Promise<void> {
    const finalText = text || FALLBACK_TEXT[key]

    this.state.lastAudioKey = key
    this.state.lastText = finalText
    this.state.error = null
    this.notify()

    if (!this.state.isReady || !this.state.isSpeechEnabled) {
      return
    }

    const file = AUDIO_FILES[key]

    if (this.state.isFileAudioEnabled && file && this.narrationAudio) {
      this.stopSpeaking()

      this.state.currentFile = file
      this.narrationAudio.src = file
      this.narrationAudio.volume = this.state.voiceVolume

      try {
        await this.narrationAudio.play()
        return
      } catch {
        this.state.error = 'Trình duyệt chặn hoặc không phát được MP3, chuyển sang Text-To-Speech.'
        this.notify()
      }
    }

    await this.speak(finalText)
  }

  async speak(text: string): Promise<void> {
    this.state.lastText = text

    if (!this.state.isSpeechEnabled) {
      this.notify()
      return
    }

    if (!this.synth) {
      this.state.error = 'Text-To-Speech chưa sẵn sàng. Hãy bấm Kích hoạt âm thanh.'
      this.state.status = 'error'
      this.notify()
      return
    }

    this.stopSpeaking(false)

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'vi-VN'
    utterance.rate = 0.95
    utterance.pitch = 1
    utterance.volume = this.state.voiceVolume

    utterance.onstart = () => {
      this.state.status = 'speaking'
      this.state.isSpeaking = true
      this.state.error = null
      this.notify()
    }

    utterance.onend = () => {
      this.state.status = 'ready'
      this.state.isSpeaking = false
      this.notify()
    }

    utterance.onerror = (event) => {
      this.state.status = 'error'
      this.state.isSpeaking = false
      this.state.error = `Lỗi Text-To-Speech: ${event.error}`
      this.notify()
    }

    this.synth.speak(utterance)

    this.state.status = 'speaking'
    this.state.isSpeaking = true
    this.notify()
  }

  stopSpeaking(shouldNotify = true): void {
    if (this.narrationAudio) {
      this.narrationAudio.pause()
      this.narrationAudio.currentTime = 0
    }

    if (this.synth) {
      this.synth.cancel()
    }

    this.state.status = this.state.isReady ? 'ready' : 'idle'
    this.state.isSpeaking = false

    if (shouldNotify) {
      this.notify()
    }
  }

  stop(): void {
    this.stopSpeaking(false)
    this.stopAmbient(false)
    this.state.status = this.state.isReady ? 'ready' : 'idle'
    this.notify()
  }

  async replayLast(): Promise<void> {
    if (this.state.lastAudioKey) {
      await this.playNarration(this.state.lastAudioKey, this.state.lastText)
      return
    }

    if (this.state.lastText) {
      await this.speak(this.state.lastText)
      return
    }

    this.state.error = 'Chưa có câu nào để đọc lại.'
    this.notify()
  }

  setSpeechEnabled(enabled: boolean): void {
    this.state.isSpeechEnabled = enabled

    if (!enabled) {
      this.stopSpeaking(false)
    }

    this.notify()
  }

  setFileAudioEnabled(enabled: boolean): void {
    this.state.isFileAudioEnabled = enabled
    this.notify()
  }

  setVoiceVolume(value: number): void {
    this.state.voiceVolume = this.clamp(value)

    if (this.narrationAudio) {
      this.narrationAudio.volume = this.state.voiceVolume
    }

    this.notify()
  }

  setAmbientVolume(value: number): void {
    this.state.ambientVolume = this.clamp(value)

    if (this.ambientAudio) {
      this.ambientAudio.volume = this.state.ambientVolume
    }

    if (this.ambientGain) {
      this.ambientGain.gain.value = this.state.ambientVolume * 0.35
    }

    this.notify()
  }

  async setAmbientEnabled(enabled: boolean): Promise<void> {
    this.state.isAmbientEnabled = enabled

    if (enabled) {
      await this.playAmbient()
    } else {
      this.stopAmbient(false)
    }

    this.notify()
  }

  async playAmbient(): Promise<void> {
    if (!this.ambientAudio) {
      this.ambientAudio = new Audio('/audio/night-ambient.mp3')
      this.ambientAudio.loop = true
    }

    this.ambientAudio.volume = this.state.ambientVolume

    try {
      await this.ambientAudio.play()
      this.stopGeneratedAmbient()
      this.state.isAmbientEnabled = true
      this.state.error = null
    } catch {
      await this.startGeneratedAmbient()
      this.state.isAmbientEnabled = true
      this.state.error = null
    }

    this.notify()
  }

  private async startGeneratedAmbient(): Promise<void> {
    const AudioContextCtor =
      window.AudioContext ||
      (window as typeof window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext

    if (!AudioContextCtor) {
      return
    }

    if (!this.ambientContext) {
      this.ambientContext = new AudioContextCtor()
    }

    if (this.ambientContext.state === 'suspended') {
      await this.ambientContext.resume()
    }

    this.stopGeneratedAmbient()

    const sampleRate = this.ambientContext.sampleRate
    const bufferSize = sampleRate * 2
    const buffer = this.ambientContext.createBuffer(1, bufferSize, sampleRate)
    const data = buffer.getChannelData(0)

    for (let i = 0; i < bufferSize; i += 1) {
      data[i] = (Math.random() * 2 - 1) * 0.12
    }

    const source = this.ambientContext.createBufferSource()
    const gain = this.ambientContext.createGain()

    source.buffer = buffer
    source.loop = true
    gain.gain.value = this.state.ambientVolume * 0.35

    source.connect(gain)
    gain.connect(this.ambientContext.destination)
    source.start()

    this.ambientSource = source
    this.ambientGain = gain
  }

  private stopGeneratedAmbient(): void {
    if (this.ambientSource) {
      try {
        this.ambientSource.stop()
      } catch {
        // Already stopped.
      }

      this.ambientSource.disconnect()
      this.ambientSource = null
    }

    if (this.ambientGain) {
      this.ambientGain.disconnect()
      this.ambientGain = null
    }
  }

  stopAmbient(shouldNotify = true): void {
    if (this.ambientAudio) {
      this.ambientAudio.pause()
      this.ambientAudio.currentTime = 0
    }

    this.stopGeneratedAmbient()
    this.state.isAmbientEnabled = false

    if (shouldNotify) {
      this.notify()
    }
  }

  private clamp(value: number): number {
    return Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0))
  }
}

export const audioService = new AudioService()

export default audioService