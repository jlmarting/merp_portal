<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '../../api/client'

const partidas = ref<any[]>([])
const personajesPartida = ref<any[]>([])
const npcsPartida = ref<any[]>([])
const selectedPartida = ref<number | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    partidas.value = await api.get<any[]>('/partidas')
    if (partidas.value.length > 0) {
      selectedPartida.value = partidas.value[0].id
      await cargarDatos()
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

async function cargarDatos() {
  if (!selectedPartida.value) return
  const [pjs, npcs] = await Promise.all([
    api.get<any[]>(`/personajes/mis`),
    api.get<any[]>(`/npcs?partida_id=${selectedPartida.value}`),
  ])
  personajesPartida.value = pjs
  npcsPartida.value = npcs
}
</script>

<template>
  <div v-if="loading" class="text-center py-12 text-gray-500">Cargando...</div>
  <div v-else class="space-y-6">
    <h1 class="text-2xl font-bold text-white">Dashboard DJ</h1>

    <div class="flex items-center gap-4">
      <label class="text-sm text-gray-400">Partida:</label>
      <select v-model.number="selectedPartida" @change="cargarDatos" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-white text-sm">
        <option v-for="p in partidas" :key="p.id" :value="p.id">{{ p.nombre }}</option>
      </select>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h2 class="text-lg font-semibold text-amber-400 mb-4">Personajes ({{ personajesPartida.length }})</h2>
        <div v-if="personajesPartida.length === 0" class="text-gray-600 text-sm">Ningún personaje en esta partida</div>
        <div v-for="pj in personajesPartida" :key="pj.id" class="flex items-center justify-between py-2 border-b border-gray-800 last:border-0 text-sm">
          <div>
            <span class="text-white">{{ pj.nombre }}</span>
            <span class="text-gray-500 ml-2">Nvl {{ pj.nivel }} {{ pj.raza }}</span>
          </div>
          <div class="flex items-center gap-3">
            <span class="font-mono" :class="pj.pv_actuales > 0 ? 'text-green-400' : 'text-red-400'">{{ pj.pv_actuales }}/{{ pj.pv_maximos }} PV</span>
            <router-link :to="`/personajes/${pj.id}`" class="text-blue-400 hover:text-blue-300">Ver</router-link>
          </div>
        </div>
      </div>

      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h2 class="text-lg font-semibold text-amber-400 mb-4">NPCs ({{ npcsPartida.length }})</h2>
        <div v-if="npcsPartida.length === 0" class="text-gray-600 text-sm">Ningún NPC en esta partida</div>
        <div v-for="n in npcsPartida" :key="n.id" class="flex items-center justify-between py-2 border-b border-gray-800 last:border-0 text-sm">
          <div>
            <span class="text-white">{{ n.nombre }}</span>
            <span class="text-xs ml-2 px-1.5 py-0.5 rounded"
              :class="n.tipo === 'enemigo' ? 'bg-red-900 text-red-300' : n.tipo === 'aliado' ? 'bg-green-900 text-green-300' : 'bg-gray-700 text-gray-300'">
              {{ n.tipo }}
            </span>
          </div>
          <span class="font-mono text-gray-400">{{ n.pv }} PV</span>
        </div>
      </div>
    </div>

    <div class="border-t border-gray-800 pt-6">
      <router-link to="/personajes/crear" class="inline-block bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded-lg text-sm transition-colors">
        + Crear personaje de prueba
      </router-link>
    </div>
  </div>
</template>
