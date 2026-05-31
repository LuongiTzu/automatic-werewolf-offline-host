<template>
  <div class="min-h-screen bg-dark-900 text-white">
    <header class="bg-dark-800 border-b border-dark-700">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-bold">🐺 Werewolf Game</h1>
        <p class="text-dark-400 mt-2">Realtime Multiplayer Werewolf</p>
      </div>
    </header>

    <main class="container mx-auto px-4 py-12">
      <div class="max-w-2xl mx-auto">
        <div class="bg-dark-800 rounded-lg p-8 border border-dark-700">
          <h2 class="text-2xl font-bold mb-4">Welcome to Werewolf Game</h2>
          <p class="text-dark-300 mb-6">
            This is the frontend for the Werewolf Game system. The app is now set up with Vue 3, Vite, TailwindCSS, and Pinia.
          </p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-dark-700 p-4 rounded-lg">
              <h3 class="font-bold text-lg mb-2">✅ Setup Complete</h3>
              <ul class="text-dark-300 text-sm space-y-1">
                <li>• Vue 3 + Vite</li>
                <li>• TailwindCSS Dark Mode</li>
                <li>• Pinia Store</li>
                <li>• TypeScript</li>
              </ul>
            </div>

            <div class="bg-dark-700 p-4 rounded-lg">
              <h3 class="font-bold text-lg mb-2">📋 Backend Status</h3>
              <p class="text-dark-300 text-sm mb-2">Backend is running on:</p>
              <p class="text-yellow-400 text-sm font-mono">http://localhost:8000</p>
            </div>
          </div>

          <div class="text-center">
            <p class="text-dark-400 text-sm">
              Ready to build the Werewolf Game 🎮
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
// App component ready for implementation
</script>

<style scoped>
/* Component styles here */
</style>
