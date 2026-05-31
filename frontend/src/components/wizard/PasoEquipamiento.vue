<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { api } from '../../api/client'

const props = defineProps<{ data: any }>()
const emit = defineEmits(['update', 'next'])

const armas = ref<any[]>([])
const armaduras = ref<any[]>([])
const loading = ref(true)

const armaduraSeleccionada = ref<any>(null)
const armasSeleccionadas = ref<any[]>([])
const pesoTotal = ref(0)

onMounted(async () => {
  try {
    const [cst1, armData] = await Promise.all([
      api.get<any>('/tablas/cst1'),
      api.get<any>('/tablas/armaduras'),
    ])
    armas.value = cst1.armas || []
    armaduras.value = armData.armaduras || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

const pvCalculados = computed(() => {
  const df = props.data.desarrollo_fisico || 0
  const bonoCO = props.data.caracteristicas?.constitucion?.bono || 0
  let total = 0
  for (let i = 0; i < df; i++) total += Math.floor(Math.random() * 10) + 1 + bonoCO
  return total || df * 6 + bonoCO * df
})

const ppCalculados = computed(() => {
  const dpp = props.data.desarrollo_poder || 0
  const bonoIT = props.data.caracteristicas?.intuicion?.bono || 0
  let total = 0
  for (let i = 0; i < dpp; i++) total += Math.floor(Math.random() * 10) + 1 + bonoIT
  return total || dpp * 6 + bonoIT * dpp
})

function toggleArma(arma: any) {
  const idx = armasSeleccionadas.value.findIndex(a => a.nombre === arma.nombre)
  if (idx >= 0) armasSeleccionadas.value.splice(idx, 1)
  else armasSeleccionadas.value.push({ ...arma })
  recalcularPeso()
}

function selectArmadura(arm: any) {
  armaduraSeleccionada.value = arm
  recalcularPeso()
}

function recalcularPeso() {
  let p = armaduraSeleccionada.value?.peso_kg || 0
  for (const a of armasSeleccionadas.value) p += a.peso_kg
  pesoTotal.value = Math.round(p * 10) / 10
}

function confirmar() {
  let mmPen = armaduraSeleccionada.value?.penalizacion_mm || 0
  emit('update', {
    equipo: {
      armas: armasSeleccionadas.value,
      armadura: armaduraSeleccionada.value,
      escudo: null,
      peso_total: pesoTotal.value,
    },
    pv_actuales: pvCalculados.value,
    pv_maximos: pvCalculados.value,
    pp_actuales: ppCalculados.value,
    pp_maximos: ppCalculados.value,
  })
  emit('next')
}
</script>

<template>
  <div v-if="loading" class="text-center py-8 text-gray-500">Cargando equipo...</div>
  <div v-else class="space-y-6">
    <h2 class="text-xl font-semibold text-amber-400">Paso 5: Equipamiento</h2>

    <div class="bg-gray-800 border border-gray-700 rounded-lg p-4">
      <h3 class="text-sm font-semibold text-gray-200 mb-3 uppercase">Armaduras</h3>
      <div class="grid gap-2 sm:grid-cols-2">
        <button v-for="arm in armaduras" :key="arm.nombre"
          @click="selectArmadura(arm)"
          class="text-left p-3 rounded-lg border transition-colors text-sm"
          :class="armaduraSeleccionada?.nombre === arm.nombre ? 'border-amber-500 bg-gray-700' : 'border-gray-600 bg-gray-900 hover:border-gray-500'">
          <p class="text-white font-medium">{{ arm.nombre }}</p>
          <p class="text-gray-500 text-xs">Tipo {{ arm.tipo_armadura }} | Pen MM: {{ arm.penalizacion_mm }} | Peso: {{ arm.peso_kg }} kg</p>
        </button>
      </div>
    </div>

    <div class="bg-gray-800 border border-gray-700 rounded-lg p-4">
      <h3 class="text-sm font-semibold text-gray-200 mb-3 uppercase">Armas</h3>
      <div class="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
        <button v-for="arma in armas" :key="arma.nombre"
          @click="toggleArma(arma)"
          class="text-left p-3 rounded-lg border transition-colors text-sm"
          :class="armasSeleccionadas.find(a => a.nombre === arma.nombre) ? 'border-amber-500 bg-gray-700' : 'border-gray-600 bg-gray-900 hover:border-gray-500'">
          <p class="text-white font-medium">{{ arma.nombre }}</p>
          <p class="text-gray-500 text-xs">{{ arma.tabla_ataque }} | {{ arma.tipo_critico }} | {{ arma.peso_kg }} kg</p>
        </button>
      </div>
    </div>

    <div class="bg-gray-800 border border-gray-700 rounded-lg p-4">
      <h3 class="text-sm font-semibold text-gray-200 mb-3 uppercase">Resumen</h3>
      <div class="grid grid-cols-3 gap-4 text-center">
        <div>
          <p class="text-gray-500 text-xs">PV</p>
          <p class="text-green-400 font-mono text-lg font-bold">{{ pvCalculados }}</p>
        </div>
        <div>
          <p class="text-gray-500 text-xs">PP</p>
          <p class="text-blue-400 font-mono text-lg font-bold">{{ ppCalculados }}</p>
        </div>
        <div>
          <p class="text-gray-500 text-xs">Peso</p>
          <p class="text-white font-mono text-lg font-bold">{{ pesoTotal }} kg</p>
        </div>
      </div>
    </div>

    <div class="bg-gray-800 border border-gray-700 rounded-lg p-4">
      <h3 class="text-sm font-semibold text-gray-200 mb-2 uppercase">Nombre del Personaje</h3>
      <input v-model="data.nombre" placeholder="Ej. Théodred, hijo de Théoden" required
        class="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-500" />
    </div>

    <button @click="confirmar"
      :disabled="!data.nombre"
      class="w-full bg-green-700 hover:bg-green-600 text-white font-medium py-2 rounded-lg transition-colors disabled:opacity-50">
      Finalizar creación
    </button>
  </div>
</template>
