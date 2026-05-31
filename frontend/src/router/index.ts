import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import HostRoom from '@/pages/HostRoom.vue'
import PlayerGame from '@/pages/PlayerGame.vue'
import PlayerJoin from '@/pages/PlayerJoin.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/host',
      name: 'HostRoom',
      component: HostRoom,
    },
    {
      path: '/join',
      name: 'PlayerJoin',
      component: PlayerJoin,
    },
    {
      path: '/player',
      name: 'PlayerGame',
      component: PlayerGame,
    },
  ],
})

export default router
