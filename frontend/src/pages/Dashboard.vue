<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { api } from '../api/client'

const auth = useAuthStore()
const router = useRouter()
const personajes = ref<any[]>([])
const partidas = ref<any[]>([])
const loading = ref(true)

interface PersonajeResumen {
  id: number
  nombre: string
  raza: string
  profesion: string
  nivel: number
  estado: string
  pv_actuales: number
  pv_maximos: number
}

onMounted(async () => {
  try {
    personajes.value = await api.get<PersonajeResumen[]>('/personajes/mis')
    partidas.value = await api.get<any[]>('/partidas')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="max-w-5xl mx-auto px-6 py-8 space-y-8">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold text-white">Mis Personajes</h1>
      <router-link to="/personajes/crear" class="bg-amber-600 hover:bg-amber-500 text-white px-5 py-2 rounded-lg font-medium transition-colors">
        + Nuevo Personaje
      </router-link>
    </div>

    <div v-if="loading" class="text-gray-500 text-center py-12">Cargando...</div>

    <div v-else-if="personajes.length === 0" class="bg-gray-900 border border-gray-800 rounded-xl p-12 text-center">
      <p class="text-gray-500 text-lg mb-2">No tienes personajes creados</p>
      <p class="text-gray-600 text-sm">Crea tu primer personaje para empezar a jugar</p>
    </div>

    <div v-else class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <router-link
        v-for="p in personajes"
        :key="p.id"
        :to="`/personajes/${p.id}`"
        class="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-amber-700 transition-colors block"
      >
        <div class="flex items-start justify-between mb-3">
          <h2 class="text-lg font-semibold text-white">{{ p.nombre }}</h2>
          <span class="text-xs px-2 py-0.5 rounded" :class="p.estado === 'vivo' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'">{{ p.estado }}</span>
        </div>
        <div class="space-y-1 text-sm text-gray-400">
          <p><span class="text-gray-500">Raza:</span> {{ p.raza }}</p>
          <p><span class="text-gray-500">Profesión:</span> {{ p.profesion }}</p>
          <p><span class="text-gray-500">Nivel:</span> {{ p.nivel }}</p>
          <p><span class="text-gray-500">PV:</span> {{ p.pv_actuales }} / {{ p.pv_maximos }}</p>
        </div>
      </router-link>
    </div>

    <div v-if="partidas.length > 0" class="border-t border-gray-800 pt-8">
      <h2 class="text-xl font-bold text-white mb-4">Partidas Disponibles</h2>
      <div class="space-y-2">
        <div v-for="p in partidas" :key="p.id" class="bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 text-sm text-gray-300">
          {{ p.nombre }} <span class="text-gray-600">(ID: {{ p.id }})</span>
        </div>
      </div>
    </div>
  </div>
</template>
