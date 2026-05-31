<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '../../api/client'

const npcs = ref<any[]>([])
const loading = ref(true)
const editando = ref<any | null>(null)
const formVisible = ref(false)

const nuevoNPC = ref({
  partida_id: 0,
  nombre: '',
  raza: '',
  profesion: '',
  nivel: 1,
  pv: 10,
  pp: 0,
  tipo: 'enemigo',
  datos_json: {},
})

onMounted(async () => {
  try {
    const partidas = await api.get<any[]>('/partidas')
    if (partidas.length > 0) {
      nuevoNPC.value.partida_id = partidas[0].id
      await cargarNPCs()
    }
  } finally {
    loading.value = false
  }
})

async function cargarNPCs() {
  npcs.value = await api.get<any[]>(`/npcs?partida_id=${nuevoNPC.value.partida_id}`)
}

async function crearNPC() {
  await api.post('/npcs', nuevoNPC.value)
  formVisible.value = false
  nuevoNPC.value.nombre = ''
  nuevoNPC.value.raza = ''
  nuevoNPC.value.profesion = ''
  await cargarNPCs()
}

async function eliminarNPC(id: number) {
  await api.delete(`/npcs/${id}`)
  await cargarNPCs()
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-white">Gestión de NPCs</h1>
      <button @click="formVisible = !formVisible"
        class="bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded-lg text-sm transition-colors">
        + Nuevo NPC
      </button>
    </div>

    <div v-if="formVisible" class="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-4">
      <h2 class="text-lg font-semibold text-amber-400">Crear NPC</h2>
      <div class="grid gap-4 sm:grid-cols-2">
        <div>
          <label class="text-xs text-gray-500 block mb-1">Nombre</label>
          <input v-model="nuevoNPC.nombre" class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white text-sm" />
        </div>
        <div>
          <label class="text-xs text-gray-500 block mb-1">Raza</label>
          <input v-model="nuevoNPC.raza" class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white text-sm" />
        </div>
        <div>
          <label class="text-xs text-gray-500 block mb-1">Profesión</label>
          <input v-model="nuevoNPC.profesion" class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white text-sm" />
        </div>
        <div>
          <label class="text-xs text-gray-500 block mb-1">Nivel</label>
          <input v-model.number="nuevoNPC.nivel" type="number" min="1" class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white text-sm" />
        </div>
        <div>
          <label class="text-xs text-gray-500 block mb-1">PV</label>
          <input v-model.number="nuevoNPC.pv" type="number" class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white text-sm" />
        </div>
        <div>
          <label class="text-xs text-gray-500 block mb-1">PP</label>
          <input v-model.number="nuevoNPC.pp" type="number" class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white text-sm" />
        </div>
        <div>
          <label class="text-xs text-gray-500 block mb-1">Tipo</label>
          <select v-model="nuevoNPC.tipo" class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white text-sm">
            <option value="enemigo">Enemigo</option>
            <option value="aliado">Aliado</option>
            <option value="neutral">Neutral</option>
          </select>
        </div>
      </div>
      <div class="flex gap-3">
        <button @click="crearNPC" class="bg-green-700 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm">Guardar</button>
        <button @click="formVisible = false" class="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm">Cancelar</button>
      </div>
    </div>

    <div v-if="loading" class="text-gray-500 text-center py-8">Cargando NPCs...</div>
    <div v-else-if="npcs.length === 0" class="bg-gray-900 border border-gray-800 rounded-xl p-8 text-center text-gray-600">
      No hay NPCs creados. Crea uno para empezar.
    </div>
    <div v-else class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-800 text-gray-400 text-left">
          <tr>
            <th class="px-4 py-3">Nombre</th>
            <th class="px-4 py-3">Raza</th>
            <th class="px-4 py-3">Profesión</th>
            <th class="px-4 py-3">Nivel</th>
            <th class="px-4 py-3">PV</th>
            <th class="px-4 py-3">Tipo</th>
            <th class="px-4 py-3">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-800">
          <tr v-for="n in npcs" :key="n.id" class="text-gray-300 hover:bg-gray-800/50">
            <td class="px-4 py-3 font-medium text-white">{{ n.nombre }}</td>
            <td class="px-4 py-3">{{ n.raza || '—' }}</td>
            <td class="px-4 py-3">{{ n.profesion || '—' }}</td>
            <td class="px-4 py-3">{{ n.nivel }}</td>
            <td class="px-4 py-3 font-mono">{{ n.pv }}</td>
            <td class="px-4 py-3">
              <span class="text-xs px-2 py-0.5 rounded" :class="n.tipo === 'enemigo' ? 'bg-red-900 text-red-300' : n.tipo === 'aliado' ? 'bg-green-900 text-green-300' : 'bg-gray-700 text-gray-300'">{{ n.tipo }}</span>
            </td>
            <td class="px-4 py-3">
              <button @click="eliminarNPC(n.id)" class="text-red-400 hover:text-red-300 text-xs">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
