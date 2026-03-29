import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    userId: null,
    role: null,
    username: null
  }),

  actions: {
    loginSuccess(payload) {
      this.isLoggedIn = true
      this.userId = payload.userId
      this.role = payload.role
      this.username = payload.username

      // Save to localStorage
      localStorage.setItem('user', JSON.stringify({
        userId: this.userId,
        role: this.role,
        username: this.username
      }))
    },

    logout() {
      this.isLoggedIn = false
      this.userId = null
      this.role = null
      this.username = null
      localStorage.removeItem('user')
    },

    loadFromStorage() {
      const saved = localStorage.getItem('user')
      if (saved) {
        const user = JSON.parse(saved)
        this.isLoggedIn = true
        this.userId = user.userId
        this.role = user.role
        this.username = user.username
      }
    }
  }
})