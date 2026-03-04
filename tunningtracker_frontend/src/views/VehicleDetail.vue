<template>
  <div v-if="loading" class="flex justify-center p-20">
    <div class="animate-spin w-10 h-10 border-4 border-primary border-t-transparent rounded-full"></div>
  </div>

  <div v-else-if="vehicle" class="space-y-8">
    <div class="glass-card p-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative overflow-hidden">
      <!-- Decor -->
      <div class="absolute -right-20 -bottom-20 w-64 h-64 bg-primary/10 rounded-full blur-3xl pointer-events-none z-0"></div>
      
      <div class="relative z-10">
        <div class="flex items-center gap-4 mb-2">
          <button @click="$router.push('/dashboard')" class="text-slate-400 hover:text-white transition-colors bg-white/5 p-2 rounded-lg">
            ← Voltar
          </button>
          <div class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1 font-mono text-sm text-primary font-bold uppercase tracking-widest shadow-inner shadow-black/50">
            {{ vehicle.placa }}
          </div>
        </div>
        <h2 class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-100 to-slate-400 uppercase tracking-tight">
          {{ vehicle.marca }} {{ vehicle.modelo }}
        </h2>
        <p class="text-slate-400 text-lg mt-1 font-medium">Ano: {{ vehicle.ano }}</p>
      </div>

      <button 
        @click="showActivityModal = true"
        class="bg-white/10 hover:bg-white/20 text-white font-medium py-3 px-6 rounded-xl border border-white/10 transition-colors shadow-lg shadow-black/20 relative z-10 cursor-pointer"
      >
        + Nova Atividade
      </button>
    </div>

    <!-- Timeline das Atividades -->
    <div>
      <h3 class="text-2xl font-bold text-white mb-6">
        Histórico de Manutenções e Modificações
      </h3>
      
      <div class="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-700 before:to-transparent">
        
        <div v-if="activities.length === 0" class="text-center text-slate-500 py-10">
          Nenhuma atividade registrada para este veículo.
        </div>

        <div 
          v-for="activity in activities" 
          :key="activity.id" 
          class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active"
        >
          <!-- Ícone Timeline -->
          <div class="flex items-center justify-center w-10 h-10 rounded-full border-4 border-slate-900 bg-slate-800 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-lg z-10">
            <span v-if="activity.tipo === 'Manutenção'" class="text-accent">🔧</span>
            <span v-else class="text-primary">⚡</span>
          </div>
          
          <!-- Card de Atividade -->
          <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] glass-card p-5 group-hover:-translate-y-1 transition-all duration-300">
            <div class="flex justify-between items-start mb-2">
              <span class="px-2 py-1 text-xs font-bold rounded-md bg-white/5 border border-white/10" :class="activity.tipo === 'Manutenção' ? 'text-accent' : 'text-primary'">
                {{ activity.tipo }}
              </span>
              <time class="text-sm font-medium text-slate-400">{{ formatDate(activity.data_atividade) }}</time>
            </div>
            <h4 class="text-lg font-bold text-slate-100">{{ activity.descricao }}</h4>
            <p v-if="activity.observacoes" class="text-slate-400 text-sm mt-2">{{ activity.observacoes }}</p>
            <div class="mt-4 flex justify-between items-center border-t border-slate-700/50 pt-3">
              <span class="text-slate-300 font-medium">Investimento:</span>
              <span class="text-lg font-bold text-white">R$ {{ Number(activity.valor).toFixed(2) }}</span>
            </div>
            <div v-if="activity.data_revisao_futura" class="mt-2 text-xs text-rose-400 font-medium flex items-center gap-1">
              <span>⚠️</span> Próxima revisão: {{ formatDate(activity.data_revisao_futura) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Activity Modal -->
    <Teleport to="body">
      <div v-if="showActivityModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/80 backdrop-blur-sm">
      <div class="glass-card w-full max-w-md p-6 relative max-h-[90vh] overflow-y-auto">
        <button @click="closeModal" class="absolute top-4 right-4 text-slate-400 hover:text-white">
          ✕
        </button>
        <h3 class="text-2xl font-bold text-white mb-6">Nova Atividade</h3>
        
        <form @submit.prevent="submitActivity" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Tipo da Atividade</label>
            <select v-model="form.tipo" required class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none">
              <option value="Manutenção">Manutenção</option>
              <option value="Modificação">Modificação</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Título / Descrição Curta</label>
            <input v-model="form.descricao" type="text" required class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none" placeholder="Ex: Suspensão a ar / Troca de óleo">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Observações Completas</label>
            <textarea v-model="form.observacoes" rows="2" class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none" placeholder="Opcional. Adicione notas extras..."></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Valor do Serviço/Peça (R$)</label>
            <input v-model="form.valor" type="number" step="0.01" required class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none" placeholder="0.00">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Data da Atividade</label>
            <input v-model="form.data_atividade" type="date" required class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none [color-scheme:dark]">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Revisão Futura (Opcional)</label>
            <input v-model="form.data_revisao_futura" type="date" class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none [color-scheme:dark]">
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
    </Teleport>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const loading = ref(true)
const vehicle = ref(null)
const activities = ref([])
const showActivityModal = ref(false)
const saving = ref(false)

const form = reactive({
  tipo: 'Manutenção',
  descricao: '',
  observacoes: '',
  valor: '',
  data_atividade: new Date().toISOString().split('T')[0],
  data_revisao_futura: ''
})

const fetchData = async () => {
  try {
    const [vehRes, actRes] = await Promise.all([
      axios.get(`http://127.0.0.1:8000/api/v1/vehicles/${route.params.id}/`),
      // Temporary workaround until custom nested routes are added: filter in frontend or if backend supports it
      axios.get('http://127.0.0.1:8000/api/v1/activities/')
    ])
    vehicle.value = vehRes.data
    // Filter activities belonging to this vehicle specifically since we are using DefaultRouter right now
    activities.value = actRes.data.filter(a => a.vehicle === vehicle.value.id)
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const [y, m, d] = dateStr.split('-')
  return `${d}/${m}/${y}`
}

const closeModal = () => {
  showActivityModal.value = false
  form.tipo = 'Manutenção'
  form.descricao = ''
  form.observacoes = ''
  form.valor = ''
  form.data_atividade = new Date().toISOString().split('T')[0]
  form.data_revisao_futura = ''
}

const submitActivity = async () => {
  saving.value = true
  try {
    const payload = {
      ...form,
      vehicle: vehicle.value.id,
      data_revisao_futura: form.data_revisao_futura || null
    }
    const res = await axios.post('http://127.0.0.1:8000/api/v1/activities/', payload)
    
    // Refresh the list to apply new order or just push and re-sort
    await fetchData()
    
    closeModal()
  } catch (err) {
    alert('Erro ao salvar atividade.')
    console.error(err)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>
