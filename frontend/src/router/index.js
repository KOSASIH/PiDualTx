import { createRouter, createWebHistory } from 'vue-router';
import PiDualTxOmega from '@/components/PiDualTxOmega.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: PiDualTxOmega,
  },
  {
    path: '/omega',
    name: 'Omega',
    component: PiDualTxOmega,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
