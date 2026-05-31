<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '../../api/client'

const props = defineProps<{ data: any }>()
const emit = defineEmits(['update', 'next'])

const bt1 = ref<any>(null)
const loading = ref(true)

const caracteristicas = ref<Record<string, { valor_base: number; bonif_raza: number; total: number; bono: number; bonif_normal: number }>>({
  fuerza: { valor_base: 50, bonif_raza: 0, total: 50, bono: 0, bonif_normal: 0 },
  agilidad: { valor_base: 50, bonif_raza: 0, total: 50, bono: 0, bonif_normal: 0 },
  constitucion: { valor_base: 50, bonif_raza: 0, total: 50, bono: 0, bonif_normal: 0 },
  inteligencia: { valor_base: 50, bonif_raza: 0, total: 50, bono: 0, bonif_normal: 0 },
  intuicion: { valor_base: 50, bonif_raza: 0, total: 50, bono: 0, bonif_normal: 0 },
  presencia: { valor_base: 50, bonif_raza: 0, total: 50, bono: 0, bonif_normal: 0 },
})

const caracKeys: Record<string, string> = {
  fuerza: 'Fuerza (FO)', agilidad: 'Agilidad (AG)', constitucion: 'Constitución (CO)',
  inteligencia: 'Inteligencia (IG)', intuicion: 'Intuición (IT)', presencia: 'Presencia (PR)'
}

onMounted(async () => {
  bt1.value = await api.get<any>('/tablas/bt1')
  if (props.data.caracteristicas_raza_mods) {
    for (const k of Object.keys(caracteristicas.value)) {
      caracteristicas.value[k].bonif_raza = props.data.caracteristicas_raza_mods[k] || 0
    }
  }
  loading.value = false
})

function obtenerBono(valor: number): number {
  if (!bt1.value?.rangos) return 0
  for (const r of bt1.value.rangos) {
    if (valor >= r.valor_min && valor <= r.valor_max) return r.bonificacion
  }
  return 0
}

function calcular() {
  for (const k of Object.keys(caracteristicas.value)) {
    const c = caracteristicas.value[k]
    c.total = c.valor_base + c.bonif_raza
    c.bonif_normal = obtenerBono(c.total)
    c.bono = c.bonif_normal + c.bonif_raza
  }
}

function generarTirada() {
  for (const k of Object.keys(caracteristicas.value)) {
    const base = Math.floor(Math.random() * 50) + 50
    caracteristicas.value[k].valor_base = base
  }
  calcular()
  emit('update', { caracteristicas: JSON.parse(JSON.stringify(caracteristicas.value)) })
}

function confirmar() {
  calcular()
  emit('update', { caracteristicas: JSON.parse(JSON.stringify(caracteristicas.value)) })
  emit('next')
}
</script>

<template>
  <div v-if="loading" class="text-center py-8 text-gray-500">Cargando tablas...</div>
  <div v-else class="space-y-5">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-semibold text-amber-400">Paso 3: Características</h2>
      <button @click="generarTirada" class="px-3 py-1.5 bg-blue-700 hover:bg-blue-600 rounded-lg text-xs text-white transition-colors">
        Generar tiradas
      </button>
    </div>
    <p class="text-sm text-gray-500">Asigna los valores base (1-100) para cada característica. Los bonos se calculan automáticamente según BT-1 y modificadores raciales.</p>

    <div class="space-y-3">
      <div v-for="(val, key) in caracteristicas" :key="key" class="bg-gray-800 border border-gray-700 rounded-lg p-4">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-300">{{ caracKeys[key] }}</span>
        </div>
        <div class="flex items-center gap-4">
          <div class="flex-1">
            <label class="text-xs text-gray-500 block mb-1">Valor base</label>
            <input type="number" v-model.number="val.valor_base" min="1" max="110" @input="calcular"
              class="w-full bg-gray-900 border border-gray-600 rounded px-2 py-1 text-white text-sm" />
          </div>
          <div class="text-center">
            <span class="text-xs text-gray-500 block mb-1">Mod. raza</span>
            <span class="text-sm font-mono" :class="val.bonif_raza >= 0 ? 'text-green-400' : 'text-red-400'">{{ val.bonif_raza >= 0 ? '+' : '' }}{{ val.bonif_raza }}</span>
          </div>
          <div class="text-center">
            <span class="text-xs text-gray-500 block mb-1">Total</span>
            <span class="text-sm font-mono text-white">{{ val.total }}</span>
          </div>
          <div class="text-center min-w-[60px]">
            <span class="text-xs text-gray-500 block mb-1">Bono</span>
            <span class="text-sm font-mono text-amber-400">{{ val.bono >= 0 ? '+' : '' }}{{ val.bono }}</span>
          </div>
        </div>
      </div>
    </div>

    <button @click="confirmar" class="w-full bg-amber-600 hover:bg-amber-500 text-white font-medium py-2 rounded-lg transition-colors">
      Confirmar características
    </button>
  </div>
</template>
