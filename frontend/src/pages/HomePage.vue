<template>
  <section class="mx-auto max-w-4xl">
    <div class="rounded-3xl border border-slate-800 bg-slate-900 p-8 text-center">
      <p class="text-sm font-bold uppercase tracking-[0.3em] text-red-300">Automatic Werewolf Host</p>
      <h1 class="mt-4 text-4xl font-black sm:text-5xl">Ma Sói tự động realtime</h1>
      <p class="mx-auto mt-4 max-w-2xl text-slate-300">
        Chọn vai trò để bắt đầu. Host là màn hình trung tâm và loa quản trò, Player dùng điện thoại để nhận role và thao tác bí mật.
      </p>

      <div class="mt-8 grid gap-4 sm:grid-cols-2">
        <RouterLink
          to="/host"
          class="rounded-2xl border border-red-800 bg-red-950/50 p-6 text-left transition hover:bg-red-900/60"
        >
          <p class="text-3xl">🎙️</p>
          <h2 class="mt-3 text-2xl font-black">Tôi là Host</h2>
          <p class="mt-2 text-sm text-slate-300">Tạo phòng, chọn role, bật âm thanh và để hệ thống tự quản trò.</p>
        </RouterLink>

        <RouterLink
          to="/join"
          class="rounded-2xl border border-slate-700 bg-slate-800 p-6 text-left transition hover:bg-slate-700"
        >
          <p class="text-3xl">📱</p>
          <h2 class="mt-3 text-2xl font-black">Tôi là Người chơi</h2>
          <p class="mt-2 text-sm text-slate-300">Nhập tên và mã phòng để vào lobby, nhận role và chơi.</p>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
