<template>
  <div class="min-h-screen bg-slate-950 text-white">
    <header class="border-b border-slate-800 bg-slate-900/80">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <div>
          <h1 class="text-2xl font-bold">🐺 Werewolf Game</h1>
          <p class="text-sm text-slate-400">Realtime Offline Host System</p>
        </div>

        <nav class="flex gap-3">
          <RouterLink
            to="/host"
            class="rounded-lg bg-red-700 px-4 py-2 text-sm font-semibold hover:bg-red-600"
          >
            Host
          </RouterLink>

          <RouterLink
            to="/join"
            class="rounded-lg bg-slate-700 px-4 py-2 text-sm font-semibold hover:bg-slate-600"
          >
            Player
          </RouterLink>
        </nav>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>