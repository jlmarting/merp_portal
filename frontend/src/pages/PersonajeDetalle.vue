<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api/client'

const route = useRoute()
const personaje = ref<any>(null)
const sortilegios = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const data = await api.get<any>(`/personajes/${route.params.id}`)
    personaje.value = data
    sortilegios.value = data.sortilegios || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

const caracKeys: Record<string, string> = {
  fuerza: 'FO', agilidad: 'AG', constitucion: 'CO',
  inteligencia: 'IG', intuicion: 'IT', presencia: 'PR', apariencia: 'APA'
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-6 py-8">
    <div v-if="loading" class="text-gray-500 text-center py-12">Cargando...</div>
    <div v-else-if="!personaje" class="text-center py-12 text-red-400">Personaje no encontrado</div>

    <template v-else>
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-3xl font-bold text-white">{{ personaje.nombre }}</h1>
        <router-link to="/" class="text-sm text-gray-400 hover:text-white">← Volver</router-link>
      </div>

      <div class="grid gap-6 md:grid-cols-2">
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-3">
          <h2 class="text-lg font-semibold text-amber-400 mb-3">Información General</h2>
          <p class="text-sm"><span class="text-gray-500">Raza:</span> {{ personaje.raza }}</p>
          <p class="text-sm"><span class="text-gray-500">Profesión:</span> {{ personaje.profesion }}</p>
          <p class="text-sm"><span class="text-gray-500">Nivel:</span> {{ personaje.nivel }}</p>
          <p class="text-sm"><span class="text-gray-500">Experiencia:</span> {{ personaje.experiencia }}</p>
          <p class="text-sm">
            <span class="text-gray-500">PV:</span>
            <span :class="personaje.pv_actuales > 0 ? 'text-green-400' : 'text-red-400'">{{ personaje.pv_actuales }}</span>
            / {{ personaje.pv_maximos }}
          </p>
          <p class="text-sm"><span class="text-gray-500">PP:</span> {{ personaje.pp_actuales }} / {{ personaje.pp_maximos }}</p>
          <p class="text-sm">
            <span class="text-gray-500">Estado:</span>
            <span :class="personaje.estado === 'vivo' ? 'text-green-400' : 'text-red-400'">{{ personaje.estado }}</span>
          </p>
        </div>

        <div class="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 class="text-lg font-semibold text-amber-400 mb-3">Características</h2>
          <div class="space-y-2">
            <div v-for="(val, key) in personaje.datos_json?.caracteristicas" :key="key" class="flex items-center justify-between text-sm">
              <span class="text-gray-400">{{ caracKeys[String(key)] || key }}:</span>
              <span class="text-white font-mono">{{ val.total }} (bono: {{ val.bono >= 0 ? '+' : '' }}{{ val.bono }})</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 md:col-span-2">
          <h2 class="text-lg font-semibold text-amber-400 mb-3">Habilidades</h2>
          <div class="grid gap-2 sm:grid-cols-2">
            <div v-for="(val, key) in personaje.datos_json?.habilidades" :key="key" class="flex items-center justify-between text-sm py-1 border-b border-gray-800 last:border-0">
              <span class="text-gray-400 truncate">{{ String(key).replace(/_/g, ' ') }}</span>
              <span class="text-white font-mono">{{ val.total >= 0 ? '+' : '' }}{{ val.total }}</span>
            </div>
          </div>
        </div>

        <div v-if="sortilegios.length > 0" class="bg-gray-900 border border-gray-800 rounded-xl p-5 md:col-span-2">
          <h2 class="text-lg font-semibold text-amber-400 mb-3">Sortilegios Conocidos</h2>
          <div class="space-y-1 text-sm">
            <div v-for="s in sortilegios" :key="s.id" class="flex items-center justify-between py-1">
              <span class="text-gray-300">{{ s.sortilegio_nombre }}</span>
              <span class="text-gray-500 text-xs">Círculo {{ s.circulo }} | Grado {{ s.grado_conocido }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
