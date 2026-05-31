<script setup lang="ts">
import { ref, computed } from 'vue'
import { api } from '../../api/client'
import { useRouter } from 'vue-router'
import PasoRaza from './PasoRaza.vue'
import PasoProfesion from './PasoProfesion.vue'
import PasoCaracteristicas from './PasoCaracteristicas.vue'
import PasoHabilidades from './PasoHabilidades.vue'
import PasoEquipamiento from './PasoEquipamiento.vue'

const router = useRouter()
const paso = ref(1)
const totalPasos = 5
const enviando = ref(false)
const error = ref('')

const wizardData = ref({
  partida_id: 0,
  nombre: '',
  raza: '',
  profesion: '',
  nivel: 1,
  caracteristicas: {} as Record<string, any>,
  habilidades: {} as Record<string, any>,
  equipo: { armas: [], armadura: null, escudo: null, peso_total: 0 },
  desarrollo_fisico: 0,
  desarrollo_poder: 0,
  pv_actuales: 0,
  pv_maximos: 0,
  pp_actuales: 0,
  pp_maximos: 0,
  movimiento_base: 10,
  sortilegios: [] as any[],
})

const pasoComponentes = [PasoRaza, PasoProfesion, PasoCaracteristicas, PasoHabilidades, PasoEquipamiento]

function siguiente() { if (paso.value < totalPasos) paso.value++ }
function anterior() { if (paso.value > 1) paso.value-- }

async function guardarPersonaje() {
  enviando.value = true
  error.value = ''
  try {
    const res = await api.post<{ id: number }>('/personajes', wizardData.value)
    router.push(`/personajes/${res.id}`)
  } catch (e: any) {
    error.value = e.message
  } finally {
    enviando.value = false
  }
}

function onDataChange(data: any) {
  Object.assign(wizardData.value, data)
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-6 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-white mb-4">Crear Personaje</h1>
      <div class="flex gap-2">
        <div v-for="i in totalPasos" :key="i" class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors"
            :class="i === paso ? 'bg-amber-600 text-white' : i < paso ? 'bg-green-700 text-green-200' : 'bg-gray-800 text-gray-500'">
            {{ i < paso ? '✓' : i }}
          </div>
          <span v-if="i < totalPasos" class="w-8 h-0.5" :class="i < paso ? 'bg-green-700' : 'bg-gray-800'"></span>
        </div>
      </div>
    </div>

    <p v-if="error" class="text-red-400 text-sm mb-4 bg-red-900/30 border border-red-900 rounded-lg px-4 py-2">{{ error }}</p>

    <div class="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <component
        :is="pasoComponentes[paso - 1]"
        :data="wizardData"
        @update="onDataChange"
        @next="siguiente"
        @prev="anterior"
      />
    </div>

    <div class="flex justify-between mt-6">
      <button v-if="paso > 1" @click="anterior" class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-gray-300 transition-colors">Anterior</button>
      <div v-else></div>
      <button v-if="paso < totalPasos" @click="siguiente" class="px-4 py-2 bg-amber-600 hover:bg-amber-500 rounded-lg text-white font-medium transition-colors">Siguiente</button>
      <button v-else @click="guardarPersonaje" :disabled="enviando"
        class="px-6 py-2 bg-green-700 hover:bg-green-600 rounded-lg text-white font-medium transition-colors disabled:opacity-50">
        {{ enviando ? 'Guardando...' : 'Guardar Personaje' }}
      </button>
    </div>
  </div>
</template>
