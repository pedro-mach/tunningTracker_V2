<template>
  <div 
    @click="$router.push(`/vehicles/${vehicle.id}`)"
    class="glass-card p-6 cursor-pointer group hover:bg-white/10 transition-all duration-300 transform hover:-translate-y-1 relative overflow-hidden"
  >
    <div class="absolute -right-10 -top-10 w-40 h-40 bg-primary/10 rounded-full blur-3xl group-hover:bg-primary/20 transition-all"></div>
    
    <div class="flex justify-between items-start mb-6">
      <div>
        <h3 class="text-xl font-bold text-white group-hover:text-primary transition-colors">{{ vehicle.marca }}</h3>
        <p class="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-200 to-slate-400 mt-1 uppercase tracking-tight">{{ vehicle.modelo }}</p>
      </div>
      <div class="bg-slate-900/80 border border-slate-700/50 rounded-lg px-3 py-1 font-mono text-xs text-primary font-bold uppercase tracking-widest shadow-inner shadow-black/50">
        {{ vehicle.placa }}
      </div>
    </div>
    
    <div class="flex items-center gap-4 text-sm font-medium text-slate-400 mt-8">
      <div class="flex items-center gap-1.5 bg-slate-800/50 px-3 py-1.5 rounded-lg">
        <span class="text-slate-500">Ano:</span>
        <span class="text-slate-300">{{ vehicle.ano }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  vehicle: {
    type: Object,
    required: true
  }
})
</script>
