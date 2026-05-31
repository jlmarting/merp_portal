<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  error.value = ''
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (e: any) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-[80vh]">
    <form @submit.prevent="handleLogin" class="bg-gray-900 border border-gray-800 rounded-xl p-8 w-full max-w-sm space-y-5">
      <h1 class="text-2xl font-bold text-amber-400 text-center">Iniciar Sesión</h1>
      <p v-if="error" class="text-red-400 text-sm text-center">{{ error }}</p>
      <div>
        <label class="block text-sm text-gray-400 mb-1">Usuario</label>
        <input v-model="username" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-500" />
      </div>
      <div>
        <label class="block text-sm text-gray-400 mb-1">Contraseña</label>
        <input v-model="password" type="password" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-500" />
      </div>
      <button type="submit" class="w-full bg-amber-600 hover:bg-amber-500 text-white font-semibold py-2 rounded-lg transition-colors">Entrar</button>
      <p class="text-center text-sm text-gray-500">¿No tienes cuenta? <router-link to="/register" class="text-amber-400 hover:underline">Regístrate</router-link></p>
    </form>
  </div>
</template>
