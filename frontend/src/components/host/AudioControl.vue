<template>
  <section class="rounded-3xl border border-slate-800 bg-slate-950/70 p-5 shadow-2xl">
    <div class="mb-5 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
      <div>
        <h2 class="text-2xl font-bold text-white">🔊 Âm thanh Host</h2>
        <p class="text-sm text-slate-300">
          Bố cục gọn kiểu 3 khối: kích hoạt, âm nói và âm nền.
        </p>
      </div>

      <div
        class="inline-flex w-fit items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold"
        :class="statusClass"
      >
        <span class="h-2.5 w-2.5 rounded-full bg-current"></span>
        <span>{{ statusLabel }}</span>
      </div>
    </div>

    <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
      <!-- Box 1: Activate / Test -->
      <div class="rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
        <div class="mb-4 flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-white">Kích hoạt</h3>
            <p class="text-sm text-slate-400">Mở âm thanh và test nhanh</p>
          </div>
          <div class="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">
            Host
          </div>
        </div>

        <button
          type="button"
          class="mb-3 flex w-full items-center justify-center gap-2 rounded-2xl bg-emerald-600 px-4 py-3 text-base font-bold text-white transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="isBusy"
          @click="handleActivate"
        >
          <span>🎤</span>
          <span>{{ state.isReady ? 'Test âm thanh' : 'Kích hoạt + test âm thanh' }}</span>
        </button>

        <div class="grid grid-cols-2 gap-2">
          <button
            type="button"
            class="rounded-xl bg-blue-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="!state.isReady"
            @click="handleReplay"
          >
            Đọc lại
          </button>

          <button
            type="button"
            class="rounded-xl bg-rose-700 px-3 py-2 text-sm font-semibold text-white transition hover:bg-rose-600 disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="!state.isSpeaking"
            @click="handleStop"
          >
            Dừng
          </button>
        </div>
      </div>

      <!-- Box 2: Voice -->
      <div class="rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
        <div class="mb-4 flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-white">Âm nói</h3>
            <p class="text-sm text-slate-400">Giọng quản trò chính</p>
          </div>

          <label class="relative inline-flex cursor-pointer items-center">
            <input
              :checked="state.isSpeechEnabled"
              type="checkbox"
              class="peer sr-only"
              @change="handleSpeechToggle"
            />
            <div
              class="peer h-7 w-12 rounded-full bg-slate-700 transition after:absolute after:left-[4px] after:top-[4px] after:h-5 after:w-5 after:rounded-full after:bg-white after:transition-all after:content-[''] peer-checked:bg-emerald-600 peer-checked:after:translate-x-5"
            ></div>
          </label>
        </div>

        <div class="mb-3 flex items-center justify-between">
          <span class="text-sm text-slate-300">Âm lượng giọng đọc</span>
          <span class="text-sm font-bold text-white">{{ voicePercent }}%</span>
        </div>

        <div class="flex items-center gap-3">
          <span class="text-lg text-slate-300">🔈</span>
          <input
            :value="state.voiceVolume"
            type="range"
            min="0"
            max="1"
            step="0.01"
            class="youtube-slider"
            @input="handleVoiceInput"
          />
          <span class="text-xl text-slate-100">🔊</span>
        </div>
      </div>

      <!-- Box 3: Ambient -->
      <div class="rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
        <div class="mb-4 flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-white">Âm nền</h3>
            <p class="text-sm text-slate-400">Ambient noise ban đêm</p>
          </div>

          <label class="relative inline-flex cursor-pointer items-center">
            <input
              :checked="state.isAmbientEnabled"
              type="checkbox"
              class="peer sr-only"
              @change="handleAmbientToggle"
            />
            <div
              class="peer h-7 w-12 rounded-full bg-slate-700 transition after:absolute after:left-[4px] after:top-[4px] after:h-5 after:w-5 after:rounded-full after:bg-white after:transition-all after:content-[''] peer-checked:bg-red-600 peer-checked:after:translate-x-5"
            ></div>
          </label>
        </div>

        <div class="mb-3 flex items-center justify-between">
          <span class="text-sm text-slate-300">Âm lượng nền</span>
          <span class="text-sm font-bold text-white">{{ ambientPercent }}%</span>
        </div>

        <div class="flex items-center gap-3">
          <span class="text-lg text-slate-300">🔈</span>
          <input
            :value="state.ambientVolume"
            type="range"
            min="0"
            max="1"
            step="0.01"
            class="youtube-slider ambient"
            @input="handleAmbientInput"
          />
          <span class="text-xl text-slate-100">🌙</span>
        </div>
      </div>
    </div>

    <div class="mt-4 rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
      <div class="mb-2 flex items-center justify-between gap-3">
        <h3 class="text-sm font-semibold text-white">Câu đang đọc / fallback cho Host</h3>
        <span class="text-xs text-slate-400">{{ currentModeText }}</span>
      </div>

      <div class="min-h-[88px] rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-base text-slate-100">
        {{ state.lastText || 'Chưa có nội dung nào.' }}
      </div>

      <div
        v-if="state.error"
        class="mt-3 rounded-xl border border-amber-700/50 bg-amber-950/40 px-4 py-3 text-sm text-amber-200"
      >
        {{ state.error }}
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import audioService, { type AudioState } from '@/services/audioService'

const state = ref<AudioState>(audioService.getState())
const isBusy = ref(false)

let unsubscribe: (() => void) | null = null

onMounted(() => {
  unsubscribe = audioService.subscribe((nextState) => {
    state.value = nextState
  })
})

onBeforeUnmount(() => {
  if (unsubscribe) unsubscribe()
})

const voicePercent = computed(() => Math.round((state.value.voiceVolume || 0) * 100))
const ambientPercent = computed(() => Math.round((state.value.ambientVolume || 0) * 100))

const statusLabel = computed(() => {
  if (state.value.status === 'error') return 'Lỗi âm thanh'
  if (state.value.isSpeaking) return 'Đang phát'
  if (state.value.isReady) return 'Sẵn sàng'
  return 'Chưa kích hoạt'
})

const statusClass = computed(() => {
  if (state.value.status === 'error') {
    return 'bg-rose-900/50 text-rose-300 border border-rose-700/50'
  }
  if (state.value.isSpeaking) {
    return 'bg-blue-900/50 text-blue-300 border border-blue-700/50'
  }
  if (state.value.isReady) {
    return 'bg-emerald-900/50 text-emerald-300 border border-emerald-700/50'
  }
  return 'bg-slate-800 text-slate-300 border border-slate-700'
})

const currentModeText = computed(() => {
  if (state.value.currentFile) return 'Đang ưu tiên MP3'
  if (state.value.isSpeaking) return 'Đang dùng Text-To-Speech'
  return 'Sẵn sàng fallback'
})

async function handleActivate() {
  isBusy.value = true
  try {
    if (!state.value.isReady) {
      await audioService.initAudio()
    } else {
      await audioService.testAudio()
    }
  } finally {
    isBusy.value = false
  }
}

async function handleReplay() {
  await audioService.replayLast()
}

function handleStop() {
  audioService.stopSpeaking()
}

function handleSpeechToggle(event: Event) {
  const checked = (event.target as HTMLInputElement).checked
  audioService.setSpeechEnabled(checked)
}

function handleVoiceInput(event: Event) {
  const value = Number((event.target as HTMLInputElement).value)
  audioService.setVoiceVolume(value)
}

async function handleAmbientToggle(event: Event) {
  const checked = (event.target as HTMLInputElement).checked
  await audioService.setAmbientEnabled(checked)
}

function handleAmbientInput(event: Event) {
  const value = Number((event.target as HTMLInputElement).value)
  audioService.setAmbientVolume(value)
}
</script>

<style scoped>
.youtube-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 9999px;
  background: linear-gradient(90deg, #22c55e 0%, #14b8a6 100%);
  outline: none;
}

.youtube-slider.ambient {
  background: linear-gradient(90deg, #ef4444 0%, #f97316 100%);
}

.youtube-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 9999px;
  background: #ffffff;
  border: 2px solid #0f172a;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.08);
  cursor: pointer;
}

.youtube-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 9999px;
  background: #ffffff;
  border: 2px solid #0f172a;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.08);
  cursor: pointer;
}
</style>