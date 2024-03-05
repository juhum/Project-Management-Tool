import { createRouter, createWebHistory } from 'vue-router'
import store from '../store/index.js'
import HomeView from '../views/HomeView.vue'
import SignUpView from '../views/SignUpView'
import LoginView from '../views/LoginView'
import NotFoundView from '../views/NotFoundView'
import ProjectsView from '../views/ProjectsView'
import ProjectDetailView from '../views/ProjectDetailView'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'notfound',
    component: NotFoundView
  },
  {
  path: '/projects',
  name: 'projects',
  component: ProjectsView,
  meta: {
    requiresAuth: true
  }
  },
  {
    path: '/projects/:projectId',
    name: 'ProjectDetailView',
    component: ProjectDetailView,
    props: true,
    meta: {
      requiresAuth: true
    }
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("token");

  if (to.name === 'login' || to.name === 'signup') {
    if (isAuthenticated) {
      next('/');
    } else {
      next();
    }
  } else {
    if (to.meta.requiresAuth && !isAuthenticated) {
      next('/login');
    } else {
      next();
    }
  }
});

export default router
