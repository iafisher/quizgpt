import { createRouter, createWebHistory } from 'vue-router';

import CreatePage from '../views/CreatePage.vue';
import HomePage from '../views/HomePage.vue';
import SubjectPage from '../views/SubjectPage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/subject/:subjectId',
      name: 'subject',
      component: SubjectPage,
      props: true,
    },
    {
      path: '/create',
      name: 'create',
      component: CreatePage,
    }
  ]
});

export default router;
