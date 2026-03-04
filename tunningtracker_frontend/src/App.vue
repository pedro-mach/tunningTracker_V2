<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-slate-100 font-sans selection:bg-primary selection:text-white">
    <!-- Navbar (condicional, só se estiver logado) -->
    <header v-if="authStore.isAuthenticated" class="sticky top-0 z-50 w-full backdrop-blur-xl bg-slate-900/60 border-b border-white/10 shadow-lg">
      <div class="container mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary to-accent shadow-lg shadow-primary/30 flex items-center justify-center font-bold text-xl">
            T
          </div>
          <h1 class="text-2xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-primary via-blue-400 to-accent">
            Tunning<span class="font-normal text-slate-300">Tracker</span>
          </h1>
        </div>
        
        <nav class="flex items-center gap-6">
          <router-link to="/dashboard" class="text-sm font-medium text-slate-300 hover:text-white transition-colors">
            Meus Veículos
          </router-link>
          <button @click="handleLogout" class="text-sm px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 transition-all font-medium text-slate-300 hover:text-white">
            Sair
          </button>
        </nav>
      </div>
    </header>

    <!-- App Content -->
    <main class="container mx-auto p-6 md:p-10">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  if (authStore.token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${authStore.token}`
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
