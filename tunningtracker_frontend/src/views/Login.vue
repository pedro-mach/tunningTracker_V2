<template>
  <div class="max-w-md w-full mx-auto mt-20">
    <div class="glass-card p-10 relative overflow-hidden group">
      <!-- Glow effect -->
      <div class="absolute -inset-1 bg-gradient-to-r from-primary to-accent opacity-0 group-hover:opacity-20 transition duration-1000 blur-2xl"></div>
      
      <div class="relative z-10 flex flex-col items-center">
        <div class="w-16 h-16 mb-6 rounded-2xl bg-gradient-to-tr from-primary to-accent shadow-lg shadow-primary/30 flex items-center justify-center font-black text-3xl">
          T
        </div>
        <h2 class="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 mb-8">
          Acesso
        </h2>

        <form @submit.prevent="submit" class="w-full flex flex-col gap-5">
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-2">Usuário</label>
            <input 
              v-model="username" 
              type="text" 
              class="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all font-medium"
              placeholder="Digite seu usuário"
              required 
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-2">Senha</label>
            <input 
              v-model="password" 
              type="password" 
              class="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all font-medium"
              placeholder="Digite sua senha"
              required 
            />
          </div>

          <div v-if="errorMsg" class="text-rose-400 text-sm font-medium text-center bg-rose-500/10 py-2 rounded-lg border border-rose-500/20">
            {{ errorMsg }}
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="mt-4 w-full bg-gradient-to-r from-primary to-accent hover:opacity-90 text-white font-bold py-3 px-4 rounded-xl shadow-lg shadow-primary/20 transition-all transform hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50"
          >
            <span v-if="!loading">Entrar</span>
            <span v-else class="animate-pulse">Autenticando...</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

const router = useRouter()
const authStore = useAuthStore()

const submit = async () => {
  loading.value = true
  errorMsg.value = ''
  
  const success = await authStore.login(username.value, password.value)
  if (success) {
    router.push('/dashboard')
  } else {
    errorMsg.value = 'Credenciais inválidas. Tente novamente.'
  }
  loading.value = false
}
</script>
