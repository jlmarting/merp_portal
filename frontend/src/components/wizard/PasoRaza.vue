<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '../../api/client'

const props = defineProps<{ data: any }>()
const emit = defineEmits(['update', 'next'])

const razas = ref<any[]>([])
const bt3 = ref<any>(null)
const loading = ref(true)

onMounted(async () => {
  const cgt3 = await api.get<any>('/tablas/cgt3')
  razas.value = cgt3.razas || []
  bt3.value = await api.get<any>('/tablas/bt3')
  loading.value = false
})

function seleccionar(raza: any) {
  const mods = bt3.value?.razas?.[raza.codigo]?.modificadores_caracteristicas || {}
  emit('update', {
    raza: raza.codigo,
    raza_nombre: raza.nombre,
    caracteristicas_raza_mods: mods,
  })
}
</script>

<template>
  <div v-if="loading" class="text-center py-8 text-gray-500">Cargando razas...</div>
  <div v-else class="space-y-4">
    <h2 class="text-xl font-semibold text-amber-400 mb-2">Paso 1: Seleccionar Raza</h2>
    <p class="text-sm text-gray-500 mb-4">Elige la raza de tu personaje. Esto determinará sus modificadores raciales y bonificaciones iniciales.</p>
    <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      <button
        v-for="raza in razas" :key="raza.codigo"
        @click="seleccionar(raza); emit('next')"
        class="bg-gray-800 border border-gray-700 hover:border-amber-600 rounded-lg p-4 text-left transition-colors"
        :class="data.raza === raza.codigo ? 'border-amber-500' : ''"
      >
        <h3 class="font-semibold text-white">{{ raza.nombre }}</h3>
        <p class="text-xs text-gray-500 mt-1">{{ raza.descripcion }}</p>
        <p class="text-xs text-gray-600 mt-2">Historial: {{ raza.puntos_historial }} pts</p>
      </button>
    </div>
  </div>
</template>
