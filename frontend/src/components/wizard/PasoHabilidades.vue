<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { api } from '../../api/client'

const props = defineProps<{ data: any }>()
const emit = defineEmits(['update', 'next'])

const bt2 = ref<any>(null)
const loading = ref(true)

const pd_disponibles = ref(0)
const pd_gastados = ref(0)

const habilidades = ref<Record<string, { grado: number; coste: number; carac: string; bono_carac: number; bono_profesion: number; total: number; usado: boolean }>>({})

const pdRestantes = computed(() => pd_disponibles.value - pd_gastados.value)

onMounted(async () => {
  bt2.value = await api.get<any>('/tablas/bt2')
  if (bt2.value?.habilidades) {
    for (const [nombre, info] of Object.entries(bt2.value.habilidades) as [string, any][]) {
      const coste = props.data.costes_desarrollo?.[nombre] || 6
      const caracKey = info.caracteristica === 'variable' ? 'agilidad' : info.caracteristica || 'ninguna'
      const bonoCarac = props.data.caracteristicas?.[caracKey]?.bono || 0
      const bonoProf = props.data.bono_por_nivel?.[nombre] || 0
      habilidades.value[nombre] = {
        grado: 0,
        coste,
        carac: caracKey,
        bono_carac: bonoCarac,
        bono_profesion: bonoProf * (props.data.nivel || 1),
        total: 0,
        usado: false,
      }
    }
  }
  pd_disponibles.value = 50 + (props.data.caracteristicas?.inteligencia?.bono || 0)
  loading.value = false
  recalcular()
})

function recalcular() {
  pd_gastados.value = 0
  for (const h of Object.values(habilidades.value)) {
    if (h.usado) {
      pd_gastados.value += h.grado * h.coste
    }
    const bonoGrado = h.grado === 0 ? -25
      : Math.min(h.grado, 10) * 5 + Math.max(0, Math.min(h.grado - 10, 10)) * 2 + Math.max(0, h.grado - 20) * 1
    h.total = bonoGrado + h.bono_carac + h.bono_profesion
  }
}

function toggle(habilidad: string) {
  const h = habilidades.value[habilidad]
  if (!h.usado) {
    h.usado = true
    if (h.grado === 0) h.grado = 1
  }
  recalcular()
}

function cambiarGrado(nombre: string, delta: number) {
  const h = habilidades.value[nombre]
  const nuevo = h.grado + delta
  if (nuevo < 0) return
  const costeNuevo = nuevo * h.coste - h.grado * h.coste
  if (delta > 0 && pdRestantes.value < costeNuevo) return
  h.grado = nuevo
  h.usado = h.grado > 0
  recalcular()
}

function confirmar() {
  const hb = {} as Record<string, any>
  for (const [nombre, h] of Object.entries(habilidades.value)) {
    const bonoGrado = h.grado === 0 ? -25
      : Math.min(h.grado, 10) * 5 + Math.max(0, Math.min(h.grado - 10, 10)) * 2 + Math.max(0, h.grado - 20) * 1
    hb[nombre] = {
      grado: h.grado,
      carac: h.bono_carac,
      profesion: h.bono_profesion,
      objeto: 0,
      especial: 0,
      total: bonoGrado + h.bono_carac + h.bono_profesion,
    }
  }
  emit('update', {
    habilidades: hb,
    desarrollo_fisico: habilidades.value['desarrollo_fisico']?.grado || 0,
    desarrollo_poder: habilidades.value['desarrollo_de_poder']?.grado || 0,
  })
  emit('next')
}

function categorias(): string[] {
  const cats = new Set<string>()
  for (const [nombre, h] of Object.entries(bt2.value?.habilidades || {})) {
    if ((h as any).categoria) cats.add((h as any).categoria)
  }
  return Array.from(cats)
}

function habilidadesPorCategoria(cat: string): [string, any][] {
  return (Object.entries(bt2.value?.habilidades || {}) as [string, any][])
    .filter(([_, info]) => info.categoria === cat)
    .map(([nombre, info]) => [nombre, info])
}
</script>

<template>
  <div v-if="loading" class="text-center py-8 text-gray-500">Cargando habilidades...</div>
  <div v-else class="space-y-5">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-semibold text-amber-400">Paso 4: Habilidades</h2>
      <div class="text-sm">
        <span class="text-gray-400">PD disponibles:</span>
        <span class="font-mono ml-1" :class="pdRestantes >= 0 ? 'text-green-400' : 'text-red-400'">{{ pd_disponibles }}</span>
        <span class="text-gray-600 mx-1">|</span>
        <span class="text-gray-400">Gastados:</span>
        <span class="font-mono ml-1 text-white">{{ pd_gastados }}</span>
        <span class="text-gray-600 mx-1">|</span>
        <span class="text-gray-400">Restantes:</span>
        <span class="font-mono ml-1" :class="pdRestantes >= 0 ? 'text-amber-400' : 'text-red-400'">{{ pdRestantes }}</span>
      </div>
    </div>
    <p class="text-sm text-gray-500">Asigna Puntos de Desarrollo (PD) a las habilidades. La bonificación se calcula automáticamente (Grado + Carac + Profesión × nivel).</p>

    <div v-for="cat in categorias()" :key="cat" class="bg-gray-800 border border-gray-700 rounded-lg p-4">
      <h3 class="text-sm font-semibold text-gray-200 mb-3 uppercase tracking-wider">{{ cat }}</h3>
      <div class="space-y-2">
        <div v-for="[nombre, info] in habilidadesPorCategoria(cat)" :key="nombre" class="flex items-center justify-between text-sm py-1">
          <div class="flex items-center gap-2 flex-1">
            <button @click="toggle(nombre)" class="w-5 h-5 flex items-center justify-center rounded text-xs border"
              :class="habilidades[nombre]?.usado ? 'bg-amber-700 border-amber-500 text-white' : 'bg-gray-800 border-gray-600 text-gray-500'">
              {{ habilidades[nombre]?.usado ? '✓' : '' }}
            </button>
            <span class="text-gray-300">{{ nombre.replace(/_/g, ' ') }}</span>
            <span class="text-gray-600 text-xs">(coste {{ habilidades[nombre]?.coste }})</span>
          </div>
          <div class="flex items-center gap-2" v-if="habilidades[nombre]?.usado">
            <div class="flex items-center gap-1">
              <button @click="cambiarGrado(nombre, -1)" class="px-1.5 py-0.5 bg-gray-700 rounded text-xs hover:bg-gray-600">−</button>
              <span class="font-mono w-6 text-center text-white">{{ habilidades[nombre]?.grado }}</span>
              <button @click="cambiarGrado(nombre, 1)" class="px-1.5 py-0.5 bg-gray-700 rounded text-xs hover:bg-gray-600">+</button>
            </div>
            <span class="font-mono w-12 text-right" :class="(habilidades[nombre]?.total || 0) >= 0 ? 'text-green-400' : 'text-red-400'">
              {{ habilidades[nombre]?.total >= 0 ? '+' : '' }}{{ habilidades[nombre]?.total || 0 }}
            </span>
          </div>
          <span v-else class="text-gray-600 font-mono">—</span>
        </div>
      </div>
    </div>

    <button @click="confirmar" class="w-full bg-amber-600 hover:bg-amber-500 text-white font-medium py-2 rounded-lg transition-colors">
      Confirmar habilidades
    </button>
  </div>
</template>
