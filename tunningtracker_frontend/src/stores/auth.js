import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('access_token') || null,
        refreshToken: localStorage.getItem('refresh_token') || null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
    },
    actions: {
        async login(username, password) {
            try {
                const response = await axios.post('http://127.0.0.1:8000/api/v1/token/', {
                    username,
                    password
                })
                this.token = response.data.access
                this.refreshToken = response.data.refresh
                localStorage.setItem('access_token', this.token)
                localStorage.setItem('refresh_token', this.refreshToken)

                // Setup default auth header
                axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
                return true
            } catch (error) {
                console.error('Falha no login', error)
                return false
            }
        },
        logout() {
            this.token = null
            this.refreshToken = null
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            delete axios.defaults.headers.common['Authorization']
        }
    }
})
