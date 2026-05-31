<script setup lang="ts">
import { useAuthStore } from './stores/auth'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

onMounted(async () => {
  if (auth.token) {
    try {
      await auth.fetchMe()
    } catch {
      auth.logout()
      router.push('/login')
    }
  }
})
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <nav v-if="auth.isAuthenticated" class="bg-gray-900 border-b border-gray-800 px-6 py-3 flex items-center justify-between">
      <div class="flex items-center gap-6">
        <router-link to="/" class="text-xl font-bold tracking-tight text-amber-400">MERP Portal</router-link>
        <router-link to="/" class="text-sm text-gray-300 hover:text-white">Dashboard</router-link>
        <router-link v-if="auth.user?.rol === 'dj'" to="/dj" class="text-sm text-gray-300 hover:text-white">Panel DJ</router-link>
      </div>
      <div class="flex items-center gap-4 text-sm text-gray-400">
        <span>{{ auth.user?.username }}</span>
        <span class="px-2 py-0.5 rounded text-xs" :class="auth.user?.rol === 'dj' ? 'bg-amber-900 text-amber-200' : 'bg-gray-800'">{{ auth.user?.rol }}</span>
        <button @click="auth.logout(); router.push('/login')" class="text-red-400 hover:text-red-300">Salir</button>
      </div>
    </nav>
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>
