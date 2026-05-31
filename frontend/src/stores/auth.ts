import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../api/client'

interface User {
  id: number
  username: string
  email: string
  rol: string
  partida_id: number | null
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('merp_token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  async function login(username: string, password: string) {
    const res = await api.post<{ access_token: string; user_id: number; username: string; rol: string }>('/auth/login', { username, password })
    token.value = res.access_token
    localStorage.setItem('merp_token', res.access_token)
    user.value = { id: res.user_id, username: res.username, rol: res.rol, email: '', partida_id: null }
    await fetchMe()
  }

  async function register(username: string, email: string, password: string) {
    const res = await api.post<{ access_token: string; user_id: number; username: string; rol: string }>('/auth/register', { username, email, password })
    token.value = res.access_token
    localStorage.setItem('merp_token', res.access_token)
    user.value = { id: res.user_id, username: res.username, rol: res.rol, email, partida_id: null }
    await fetchMe()
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      user.value = await api.get<User>('/auth/me')
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('merp_token')
  }

  return { token, user, isAuthenticated, login, register, fetchMe, logout }
})
