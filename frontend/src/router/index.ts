import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: () => import('../pages/Dashboard.vue') },
    { path: '/login', name: 'login', component: () => import('../pages/Login.vue') },
    { path: '/register', name: 'register', component: () => import('../pages/Register.vue') },
    { path: '/personajes/crear', name: 'crear-personaje', component: () => import('../components/wizard/WizardContainer.vue') },
    { path: '/personajes/:id', name: 'personaje-detalle', component: () => import('../pages/PersonajeDetalle.vue') },
    {
      path: '/dj',
      component: () => import('../pages/dj/LayoutDJ.vue'),
      children: [
        { path: '', name: 'panel-dj', component: () => import('../pages/dj/PanelDJ.vue') },
        { path: 'npcs', name: 'gestor-npcs', component: () => import('../pages/dj/GestorNPCs.vue') },
        { path: 'combate/:sesionId?', name: 'registro-combate', component: () => import('../pages/dj/RegistroCombate.vue') },
      ]
    },
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('merp_token')
  const publicPages = ['/login', '/register']
  if (!token && !publicPages.includes(to.path)) {
    return next('/login')
  }
  next()
})

export default router
