<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

async function handleRegister() {
  error.value = ''
  try {
    await auth.register(username.value, email.value, password.value)
    router.push('/')
  } catch (e: any) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-[80vh]">
    <form @submit.prevent="handleRegister" class="bg-gray-900 border border-gray-800 rounded-xl p-8 w-full max-w-sm space-y-5">
      <h1 class="text-2xl font-bold text-amber-400 text-center">Crear Cuenta</h1>
      <p v-if="error" class="text-red-400 text-sm text-center">{{ error }}</p>
      <div>
        <label class="block text-sm text-gray-400 mb-1">Usuario</label>
        <input v-model="username" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-500" />
      </div>
      <div>
        <label class="block text-sm text-gray-400 mb-1">Email</label>
        <input v-model="email" type="email" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-500" />
      </div>
      <div>
        <label class="block text-sm text-gray-400 mb-1">Contraseña</label>
        <input v-model="password" type="password" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-500" />
      </div>
      <button type="submit" class="w-full bg-amber-600 hover:bg-amber-500 text-white font-semibold py-2 rounded-lg transition-colors">Registrarse</button>
      <p class="text-center text-sm text-gray-500">¿Ya tienes cuenta? <router-link to="/login" class="text-amber-400 hover:underline">Inicia sesión</router-link></p>
    </form>
  </div>
</template>
