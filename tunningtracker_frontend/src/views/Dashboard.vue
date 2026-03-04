<template>
  <div class="space-y-8">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">Garagem</h2>
        <p class="text-slate-400 mt-2">Gerencie seus veículos e modificações</p>
      </div>
      <button 
        @click="showAddModal = true"
        class="bg-gradient-to-r from-primary to-accent hover:opacity-90 text-white font-semibold py-2 px-6 rounded-xl shadow-lg shadow-primary/20 transition-all transform hover:-translate-y-0.5 flex items-center gap-2"
      >
        <span>+ Adicionar Veículo</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center p-20">
      <div class="animate-spin w-10 h-10 border-4 border-primary border-t-transparent rounded-full"></div>
    </div>

    <!-- Vehicles Grid -->
    <div v-else-if="vehicles.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <VehicleCard 
        v-for="car in vehicles" 
        :key="car.id" 
        :vehicle="car" 
      />
    </div>

    <!-- Empty State -->
    <div v-else class="glass-card p-12 text-center mt-10">
      <div class="w-20 h-20 mx-auto bg-slate-800 rounded-full flex items-center justify-center mb-6">
        <span class="text-4xl">🚗</span>
      </div>
      <h3 class="text-2xl font-semibold mb-2 text-white">Sua garagem está vazia</h3>
      <p class="text-slate-400 mb-8 max-w-md mx-auto">
        Comece adicionando seu primeiro veículo para acompanhar manutenções e modificações incríveis.
      </p>
      <button 
        @click="showAddModal = true"
        class="bg-white/10 hover:bg-white/20 text-white font-medium py-2 px-6 rounded-xl border border-white/10 transition-colors"
      >
        Adicionar agora
      </button>
    </div>

    <!-- Add Vehicle Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/80 backdrop-blur-sm">
      <div class="glass-card w-full max-w-md p-6 relative">
        <button @click="closeModal" class="absolute top-4 right-4 text-slate-400 hover:text-white">
          ✕
        </button>
        <h3 class="text-2xl font-bold text-white mb-6">Novo Veículo</h3>
        
        <form @submit.prevent="submitVehicle" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Placa</label>
            <input v-model="form.placa" type="text" required class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none uppercase" placeholder="ABC1234">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Marca</label>
            <input v-model="form.marca" type="text" required class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none" placeholder="Ex: Volkswagen">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Modelo</label>
            <input v-model="form.modelo" type="text" required class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none" placeholder="Ex: Golf GTI">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Ano</label>
            <input v-model="form.ano" type="number" required class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none" placeholder="Ex: 2020">
          </div>
          
          <div class="pt-4 flex gap-3">
            <button type="button" @click="closeModal" class="flex-1 px-4 py-2 border border-slate-600 rounded-lg text-slate-300 hover:bg-slate-800 transition-colors">Cancelar</button>
            <button type="submit" :disabled="saving" class="flex-1 bg-primary hover:bg-opacity-90 text-white font-medium py-2 px-4 rounded-lg transition-colors flex justify-center items-center">
              <span v-if="saving" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              <span v-else>Salvar</span>
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'
import VehicleCard from '../components/VehicleCard.vue'

const vehicles = ref([])
const loading = ref(true)
const showAddModal = ref(false)
const saving = ref(false)

const form = reactive({
  placa: '',
  marca: '',
  modelo: '',
  ano: ''
})

const fetchVehicles = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/vehicles/')
    vehicles.value = res.data
  } catch (err) {
    console.error('Erro ao buscar veículos', err)
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  showAddModal.value = false
  form.placa = ''
  form.marca = ''
  form.modelo = ''
  form.ano = ''
}

const submitVehicle = async () => {
  saving.value = true
  try {
    // Force uppercase placa to conform to standards
    const payload = { ...form, placa: form.placa.toUpperCase() }
    const res = await axios.post('http://127.0.0.1:8000/api/v1/vehicles/', payload)
    vehicles.value.push(res.data)
    closeModal()
  } catch (err) {
    alert('Erro ao salvar veículo. Verifique se a placa já não existe.')
    console.error(err)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchVehicles()
})
</script>
