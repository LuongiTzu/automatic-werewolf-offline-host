import { createRouter, createWebHistory } from 'vue-router'
import HostRoom from '../pages/HostRoom.vue'
import PlayerJoin from '../pages/PlayerJoin.vue'
import PlayerGame from '../pages/PlayerGame.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/host',
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