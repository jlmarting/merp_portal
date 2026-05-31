<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../../api/client'

const route = useRoute()

const sesiones = ref<any[]>([])
const sesionActiva = ref<any>(null)
const acciones = ref<any[]>([])
const partidaId = ref(1)
const loading = ref(true)

const nuevaSesion = ref({ nombre: '' })
const nuevaAccion = ref({
  personaje_id: null as number | null,
  npc_id: null as number | null,
  tipo_accion: 'ataque_fisico',
  tirada_sin_modificar: 50,
  modificadores_json: {},
  resultado_final: 50,
  tabla_ataque: 'AT-1',
  tipo_armadura_oponente: 5,
  resultado_tabla: '',
  dano: 0,
  critico: false,
  tipo_critico: '',
  gravedad_critico: '',
  descripcion: '',
})

onMounted(async () => {
  try {
    const sesionId = route.params.sesionId
    if (sesionId) {
      sesionActiva.value = await api.get<any>(`/sesiones/${sesionId}`)
      acciones.value = await api.get<any[]>(`/sesiones/${sesionId}/acciones`)
    }
    const ses = await api.get<any[]>(`/sesiones?partida_id=${partidaId.value}`)
    sesiones.value = ses
  } finally {
    loading.value = false
  }
})

async function crearSesion() {
  const s = await api.post<any>('/sesiones', { partida_id: partidaId.value, nombre: nuevaSesion.value.nombre })
  sesiones.value.unshift(s)
  nuevaSesion.value.nombre = ''
}

async function seleccionarSesion(sesion: any) {
  sesionActiva.value = sesion
  acciones.value = await api.get<any[]>(`/sesiones/${sesion.id}/acciones`)
}

async function registrarAccion() {
  const a = await api.post<any>(`/sesiones/${sesionActiva.value.id}/acciones`, nuevaAccion.value)
  acciones.value.push(a)
  nuevaAccion.value = {
    personaje_id: null, npc_id: null, tipo_accion: 'ataque_fisico',
    tirada_sin_modificar: 50, modificadores_json: {}, resultado_final: 50,
    tabla_ataque: 'AT-1', tipo_armadura_oponente: 5, resultado_tabla: '',
    dano: 0, critico: false, tipo_critico: '', gravedad_critico: '', descripcion: '',
  }
}

async function cerrarSesion() {
  if (!sesionActiva.value) return
  await api.put(`/sesiones/${sesionActiva.value.id}`, { estado: 'cerrada' })
  sesionActiva.value.estado = 'cerrada'
}
</script>

<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-white">Registro de Combate</h1>

    <div class="flex gap-4 items-end">
      <div class="flex-1">
        <label class="text-xs text-gray-500 block mb-1">Nueva sesión</label>
        <input v-model="nuevaSesion.nombre" placeholder="Ej. Combate en Moria" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm" />
      </div>
      <button @click="crearSesion" class="bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded-lg text-sm">Crear sesión</button>
    </div>

    <div class="grid gap-6 md:grid-cols-3">
      <div class="bg-gray-900 border border-gray-800 rounded-xl p-4">
        <h2 class="text-sm font-semibold text-gray-200 mb-3 uppercase">Sesiones</h2>
        <div class="space-y-1">
          <button v-for="s in sesiones" :key="s.id"
            @click="seleccionarSesion(s)"
            class="w-full text-left px-3 py-2 rounded-lg text-sm transition-colors"
            :class="sesionActiva?.id === s.id ? 'bg-amber-900/50 text-amber-200 border border-amber-700' : 'text-gray-400 hover:bg-gray-800'">
            <div class="flex items-center justify-between">
              <span>{{ s.nombre }}</span>
              <span class="text-xs px-1.5 py-0.5 rounded" :class="s.estado === 'activa' ? 'bg-green-900 text-green-300' : 'bg-gray-700 text-gray-400'">{{ s.estado }}</span>
            </div>
          </button>
        </div>
      </div>

      <div class="md:col-span-2 space-y-4">
        <div v-if="sesionActiva" class="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-lg font-semibold text-amber-400">{{ sesionActiva.nombre }}</h2>
            <button v-if="sesionActiva.estado === 'activa'" @click="cerrarSesion" class="text-xs text-red-400 hover:text-red-300">Cerrar sesión</button>
          </div>

          <div class="space-y-2 text-sm">
            <div v-for="a in acciones" :key="a.id" class="bg-gray-800 rounded-lg p-3">
              <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
                <span>{{ a.tipo_accion }}</span>
                <span>{{ new Date(a.timestamp).toLocaleString() }}</span>
              </div>
              <p v-if="a.descripcion" class="text-gray-300">{{ a.descripcion }}</p>
              <div class="flex gap-4 text-xs mt-1">
                <span v-if="a.tirada_sin_modificar">Tirada: <span class="font-mono text-white">{{ a.tirada_sin_modificar }}</span></span>
                <span v-if="a.resultado_tabla">Resultado: <span class="font-mono text-amber-400">{{ a.resultado_tabla }}</span></span>
                <span v-if="a.dano > 0">Daño: <span class="font-mono text-red-400">{{ a.dano }}</span></span>
                <span v-if="a.critico" class="text-orange-400">CRÍTICO {{ a.gravedad_critico }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="sesionActiva?.estado === 'activa'" class="bg-gray-900 border border-gray-800 rounded-xl p-4 space-y-3">
          <h3 class="text-sm font-semibold text-gray-200 uppercase">Registrar Acción</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div>
              <label class="text-xs text-gray-500 block mb-1">Tipo</label>
              <select v-model="nuevaAccion.tipo_accion" class="w-full bg-gray-800 border border-gray-700 rounded px-2 py-1.5 text-white text-xs">
                <option value="ataque_fisico">Ataque Físico</option>
                <option value="ataque_magico">Ataque Mágico</option>
                <option value="maniobra">Maniobra</option>
                <option value="sortilegio">Sortilegio</option>
                <option value="otro">Otro</option>
              </select>
            </div>
            <div>
              <label class="text-xs text-gray-500 block mb-1">Tirada 1d100</label>
              <input v-model.number="nuevaAccion.tirada_sin_modificar" type="number" class="w-full bg-gray-800 border border-gray-700 rounded px-2 py-1.5 text-white text-xs" />
            </div>
            <div>
              <label class="text-xs text-gray-500 block mb-1">Resultado final</label>
              <input v-model.number="nuevaAccion.resultado_final" type="number" class="w-full bg-gray-800 border border-gray-700 rounded px-2 py-1.5 text-white text-xs" />
            </div>
            <div>
              <label class="text-xs text-gray-500 block mb-1">Daño</label>
              <input v-model.number="nuevaAccion.dano" type="number" class="w-full bg-gray-800 border border-gray-700 rounded px-2 py-1.5 text-white text-xs" />
            </div>
          </div>
          <div>
            <label class="text-xs text-gray-500 block mb-1">Descripción</label>
            <input v-model="nuevaAccion.descripcion" placeholder="Espadón vs Troll de las Cavernas..." class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-1.5 text-white text-xs" />
          </div>
          <button @click="registrarAccion" class="bg-green-700 hover:bg-green-600 text-white px-4 py-1.5 rounded-lg text-xs">Registrar</button>
        </div>

        <p v-if="!sesionActiva" class="text-gray-600 text-center py-8">Selecciona una sesión o crea una nueva para empezar.</p>
      </div>
    </div>
  </div>
</template>
