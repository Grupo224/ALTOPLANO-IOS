import { reactive } from 'vue'
import { api } from '../resources/api'

const state = reactive({
  loaded: false,
  error: null,
  user: null,
  fullName: '',
  roles: [],
  company: null,
  companies: [],
  capabilities: {},
})

export function useSession() {
  async function load() {
    if (state.loaded) return state
    try {
      const boot = await api.boot()
      state.user = boot.user
      state.fullName = boot.full_name
      state.roles = boot.roles
      state.company = boot.company
      state.companies = boot.companies
      state.capabilities = boot.capabilities
      state.loaded = true
    } catch (e) {
      state.error = e
    }
    return state
  }
  return { state, load }
}
