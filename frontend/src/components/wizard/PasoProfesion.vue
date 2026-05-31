<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '../../api/client'

const props = defineProps<{ data: any }>()
const emit = defineEmits(['update', 'next'])

const profesiones = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  const prof = await api.get<any>('/tablas/profesiones')
  profesiones.value = prof.profesiones || []
  loading.value = false
})

function seleccionar(prof: any) {
  emit('update', {
    profesion: prof.codigo,
    profesion_nombre: prof.nombre,
    costes_desarrollo: prof.costes_desarrollo,
    bono_por_nivel: prof.bono_por_nivel,
    sortilegios_disponibles: prof.sortilegios,
  })
}
</script>

<template>
  <div v-if="loading" class="text-center py-8 text-gray-500">Cargando profesiones...</div>
  <div v-else class="space-y-4">
    <h2 class="text-xl font-semibold text-amber-400 mb-2">Paso 2: Seleccionar Profesión</h2>
    <p class="text-sm text-gray-500 mb-4">La profesión determina las habilidades en las que tu personaje destaca y su progresión por nivel.</p>
    <div class="grid gap-3 sm:grid-cols-2">
      <button
        v-for="prof in profesiones" :key="prof.codigo"
        @click="seleccionar(prof); emit('next')"
        class="bg-gray-800 border border-gray-700 hover:border-amber-600 rounded-lg p-4 text-left transition-colors"
        :class="data.profesion === prof.codigo ? 'border-amber-500' : ''"
      >
        <h3 class="font-semibold text-white">{{ prof.nombre }}</h3>
        <p class="text-xs text-gray-400 mt-1">{{ prof.descripcion }}</p>
        <p v-if="prof.sortilegios" class="text-xs text-blue-400 mt-1">✦ Puede usar magia</p>
        <p v-else class="text-xs text-gray-600 mt-1">✧ Sin capacidad mágica</p>
      </button>
    </div>
  </div>
</template>
