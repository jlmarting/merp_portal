<script setup lang="ts">
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

if (auth.user?.rol !== 'dj') {
  router.push('/')
}
</script>

<template>
  <div class="flex min-h-[80vh]">
    <aside class="w-56 bg-gray-900 border-r border-gray-800 p-4 space-y-2">
      <h2 class="text-sm font-semibold text-amber-400 uppercase tracking-wider mb-4">Panel DJ</h2>
      <router-link to="/dj" class="block px-3 py-2 rounded-lg text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors">📊 Dashboard</router-link>
      <router-link to="/dj/npcs" class="block px-3 py-2 rounded-lg text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors">👹 Gestión de NPCs</router-link>
      <router-link to="/dj/combate" class="block px-3 py-2 rounded-lg text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors">⚔️ Registro de Combate</router-link>
      <hr class="border-gray-800 my-3" />
      <router-link to="/" class="block px-3 py-2 rounded-lg text-sm text-gray-500 hover:bg-gray-800 hover:text-white transition-colors">← Volver al portal</router-link>
    </aside>
    <div class="flex-1 p-6">
      <router-view />
    </div>
  </div>
</template>
