<template>
  <Teleport to="body">
    <div v-if="isOpen"
      class="fixed inset-0 z-[9999] flex items-center justify-center p-4"
      style="background: rgba(0,0,0,0.7); backdrop-filter: blur(4px);"
      @click.self="close">

      <div class="relative w-full max-w-3xl flex rounded-3xl overflow-hidden shadow-2xl"
        style="max-height: 90vh;">

        <!-- TOMBOL CLOSE -->
        <button @click="close"
          class="absolute top-4 right-4 z-10 w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition">
          <X class="w-4 h-4 text-white" />
        </button>

        <!-- KIRI: FORM -->
        <div class="flex-1 bg-white p-8 md:p-10 overflow-y-auto">

          <!-- ===== STEP: LOGIN ===== -->
          <div v-if="step === 'login'">
            <h2 class="text-2xl font-bold text-gray-900 mb-1">{{ $t('auth.loginTitle') }}</h2>
            <p class="text-gray-500 text-sm mb-6">{{ $t('auth.loginDesc') }}</p>
            <div class="flex flex-col gap-4">
              <div>
                <label class="text-xs font-medium text-gray-600 mb-1 block">{{ $t('auth.email') }}</label>
                <input v-model="form.email" type="email" placeholder="email@gmail.com"
                  class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-amber-400 transition" />
              </div>
              <div>
                <label class="text-xs font-medium text-gray-600 mb-1 block">{{ $t('auth.password') }}</label>
                <div class="relative">
                  <input v-model="form.password" :type="showPass ? 'text' : 'password'" placeholder="••••••••"
                    class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-amber-400 transition pr-10" />
                  <button @click="showPass = !showPass" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                    <Eye v-if="!showPass" class="w-4 h-4" />
                    <EyeOff v-else class="w-4 h-4" />
                  </button>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <label class="flex items-center gap-2 text-xs text-gray-500 cursor-pointer">
                  <input type="checkbox" v-model="form.remember" class="accent-amber-500" />
                  {{ $t('auth.rememberMe') }}
                </label>
                <!-- Lupa password disembunyikan sementara karena email service belum aktif -->
                <!-- <button @click="step = 'forgot'" class="text-xs text-amber-500 hover:text-amber-600 font-medium transition">
                  {{ $t('auth.forgotPassword') }}
                </button> -->
              </div>
              <button @click="handleLogin"
                :disabled="authStore.loading"
                class="w-full bg-amber-500 hover:bg-amber-400 text-white font-semibold py-3 rounded-xl transition text-sm disabled:opacity-50 disabled:cursor-not-allowed">
                {{ authStore.loading ? 'Memproses...' : $t('auth.loginBtn') }}
              </button>
              <p v-if="errorMsg" class="text-red-400 text-xs text-center -mt-2">{{ errorMsg }}</p>
              <div class="relative flex items-center gap-3">
                <div class="flex-1 h-px bg-gray-200"></div>
                <span class="text-xs text-gray-400 whitespace-nowrap">{{ $t('auth.orLoginWith') }}</span>
                <div class="flex-1 h-px bg-gray-200"></div>
              </div>
              <!-- Google login disembunyikan sementara (Coming Soon) -->
              <button disabled
                class="w-full border border-gray-200 rounded-xl py-3 text-sm font-medium text-gray-300 flex items-center justify-center gap-2 cursor-not-allowed opacity-50">
                <img src="https://www.google.com/favicon.ico" class="w-4 h-4 opacity-50" />
                {{ $t('auth.loginGoogle') }} (Coming Soon)
              </button>
              <p class="text-center text-xs text-gray-500">
                {{ $t('auth.noAccount') }}
                <button @click="step = 'register'" class="text-amber-500 hover:text-amber-600 font-medium">
                  {{ $t('auth.registerNow') }}
                </button>
              </p>
            </div>
          </div>

          <!-- ===== STEP: REGISTER ===== -->
          <div v-if="step === 'register'">
            <h2 class="text-2xl font-bold text-gray-900 mb-1">{{ $t('auth.registerTitle') }}</h2>
            <p class="text-gray-500 text-sm mb-6">{{ $t('auth.registerDesc') }}</p>
            <div class="flex flex-col gap-4">
              <div>
                <label class="text-xs font-medium text-gray-600 mb-1 block">{{ $t('auth.fullName') }}</label>
                <input v-model="form.name" type="text" :placeholder="$t('auth.fullNamePlaceholder')"
                  class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-amber-400 transition" />
              </div>
              <div>
                <label class="text-xs font-medium text-gray-600 mb-1 block">{{ $t('auth.email') }}</label>
                <input v-model="form.email" type="email" placeholder="email@gmail.com"
                  class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-amber-400 transition" />
              </div>
              <div>
                <label class="text-xs font-medium text-gray-600 mb-1 block">{{ $t('auth.village') }}</label>
                <input v-model="form.village" type="text" :placeholder="$t('auth.villagePlaceholder')"
                  class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-amber-400 transition" />
              </div>
              <div>
                <label class="text-xs font-medium text-gray-600 mb-1 block">{{ $t('auth.password') }}</label>
                <div class="relative">
                  <input v-model="form.password" :type="showPass ? 'text' : 'password'" :placeholder="$t('auth.passwordMin')"
                    class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-amber-400 transition pr-10" />
                  <button @click="showPass = !showPass" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                    <Eye v-if="!showPass" class="w-4 h-4" />
                    <EyeOff v-else class="w-4 h-4" />
                  </button>
                </div>
              </div>
              <button @click="handleRegister"
                :disabled="authStore.loading"
                class="w-full bg-amber-500 hover:bg-amber-400 text-white font-semibold py-3 rounded-xl transition text-sm disabled:opacity-50 disabled:cursor-not-allowed">
                {{ authStore.loading ? 'Memproses...' : $t('auth.registerBtn') }}
              </button>
              <p v-if="errorMsg" class="text-red-400 text-xs text-center -mt-2">{{ errorMsg }}</p>
              <div class="relative flex items-center gap-3">
                <div class="flex-1 h-px bg-gray-200"></div>
                <span class="text-xs text-gray-400 whitespace-nowrap">{{ $t('auth.orRegisterWith') }}</span>
                <div class="flex-1 h-px bg-gray-200"></div>
              </div>
              <!-- Google register disembunyikan sementara (Coming Soon) -->
              <button disabled
                class="w-full border border-gray-200 rounded-xl py-3 text-sm font-medium text-gray-300 flex items-center justify-center gap-2 cursor-not-allowed opacity-50">
                <img src="https://www.google.com/favicon.ico" class="w-4 h-4 opacity-50" />
                {{ $t('auth.registerGoogle') }} (Coming Soon)
              </button>
              <p class="text-center text-xs text-gray-500">
                {{ $t('auth.hasAccount') }}
                <button @click="step = 'login'" class="text-amber-500 hover:text-amber-600 font-medium">
                  {{ $t('auth.loginLink') }}
                </button>
              </p>
            </div>
          </div>

          <!-- ===== STEP: NEW PASSWORD ===== -->
          <div v-if="step === 'newpass'">
            <h2 class="text-2xl font-bold text-gray-900 mb-1">{{ $t('auth.newPassTitle') }}</h2>
            <p class="text-gray-500 text-sm mb-6">{{ $t('auth.newPassDesc') }}</p>
            <div class="flex flex-col gap-4">
              <div>
                <label class="text-xs font-medium text-gray-600 mb-1 block">{{ $t('auth.newPassword') }}</label>
                <div class="relative">
                  <input v-model="form.newPassword" :type="showPass ? 'text' : 'password'" placeholder="••••••••"
                    class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-amber-400 transition pr-10" />
                  <button @click="showPass = !showPass" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                    <Eye v-if="!showPass" class="w-4 h-4" />
                    <EyeOff v-else class="w-4 h-4" />
                  </button>
                </div>
                <div class="mt-2">
                  <div class="flex gap-1 mb-1">
                    <div class="h-1 flex-1 rounded-full" :class="passStrength >= 1 ? 'bg-amber-400' : 'bg-gray-200'"></div>
                    <div class="h-1 flex-1 rounded-full" :class="passStrength >= 2 ? 'bg-amber-400' : 'bg-gray-200'"></div>
                    <div class="h-1 flex-1 rounded-full" :class="passStrength >= 3 ? 'bg-emerald-400' : 'bg-gray-200'"></div>
                  </div>
                  <span class="text-xs" :class="passStrength >= 3 ? 'text-emerald-500' : 'text-amber-500'">
                    {{ passStrength >= 3 ? $t('auth.passStrengthStrong') : passStrength >= 2 ? $t('auth.passStrengthMedium') : $t('auth.passStrengthWeak') }}
                  </span>
                </div>
              </div>
              <div>
                <label class="text-xs font-medium text-gray-600 mb-1 block">{{ $t('auth.confirmPassword') }}</label>
                <input v-model="form.confirmPassword" type="password" placeholder="••••••••"
                  class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-amber-400 transition" />
              </div>
              <div class="flex flex-col gap-1">
                <div class="flex items-center gap-2 text-xs" :class="form.newPassword?.length >= 8 ? 'text-emerald-500' : 'text-gray-400'">
                  <CheckCircle class="w-3 h-3" /> {{ $t('auth.passReq1') }}
                </div>
                <div class="flex items-center gap-2 text-xs" :class="/[A-Z]/.test(form.newPassword||'') && /[a-z]/.test(form.newPassword||'') ? 'text-emerald-500' : 'text-gray-400'">
                  <CheckCircle class="w-3 h-3" /> {{ $t('auth.passReq2') }}
                </div>
                <div class="flex items-center gap-2 text-xs" :class="/\d/.test(form.newPassword||'') ? 'text-emerald-500' : 'text-gray-400'">
                  <CheckCircle class="w-3 h-3" /> {{ $t('auth.passReq3') }}
                </div>
              </div>
              <button @click="step = 'success'"
                class="w-full bg-amber-500 hover:bg-amber-400 text-white font-semibold py-3 rounded-xl transition text-sm">
                {{ $t('auth.savePassBtn') }}
              </button>
            </div>
            <div class="flex justify-center gap-2 mt-8">
              <div class="w-2 h-2 rounded-full bg-amber-400"></div>
              <div class="w-2 h-2 rounded-full bg-amber-400"></div>
              <div class="w-2 h-2 rounded-full bg-amber-400"></div>
              <div class="w-2 h-2 rounded-full bg-gray-200"></div>
            </div>
          </div>

          <!-- ===== STEP: SUCCESS ===== -->
          <div v-if="step === 'success'" class="flex flex-col items-center justify-center py-8 text-center">
            <div class="w-16 h-16 rounded-full border-2 border-amber-400 flex items-center justify-center mb-6">
              <CheckCircle class="w-8 h-8 text-amber-400" />
            </div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('auth.successTitle') }}</h2>
            <p class="text-gray-500 text-sm mb-8">{{ $t('auth.successDesc') }}</p>
            <button @click="step = 'login'"
              class="w-full bg-amber-500 hover:bg-amber-400 text-white font-semibold py-3 rounded-xl transition text-sm">
              {{ $t('auth.backToLoginBtn') }}
            </button>
            <div class="flex justify-center gap-2 mt-8">
              <div class="w-2 h-2 rounded-full bg-amber-400"></div>
              <div class="w-2 h-2 rounded-full bg-amber-400"></div>
              <div class="w-2 h-2 rounded-full bg-amber-400"></div>
              <div class="w-2 h-2 rounded-full bg-amber-400"></div>
            </div>
          </div>

        </div>

        <!-- KANAN: BRANDING -->
        <div class="hidden md:flex w-64 flex-col items-center justify-center p-8 text-center"
          style="background: linear-gradient(180deg, #1a4a2e 0%, #0d2818 100%);">
          <img src="/Logo-Cocopra.id.png" alt="Logo" class="w-64 h-64 object-contain mb-4" />
          <span class="text-white font-bold text-2xl mb-1">Cocopra<span class="text-amber-400">.id</span></span>
          <div class="w-8 h-0.5 bg-amber-400 mb-4"></div>
          <p class="text-emerald-300 text-xs font-medium tracking-widest uppercase leading-relaxed">
            {{ $t('auth.brandTagline') }}
          </p>
          <p class="text-amber-400 text-xs font-semibold mt-2 tracking-widest">{{ $t('auth.brandPowered') }}</p>
        </div>

      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { X, Eye, EyeOff, ArrowLeft, CheckCircle } from 'lucide-vue-next'

const { t } = useI18n()
const authStore = useAuthStore()
const router = useRouter()

defineProps({
  isOpen: Boolean,
  initialStep: { type: String, default: 'login' }
})

const emit = defineEmits(['close'])

const step = ref('login')
const showPass = ref(false)
const errorMsg = ref('')

const form = ref({
  name: '',
  email: '',
  password: '',
  newPassword: '',
  confirmPassword: '',
  village: '',
  remember: false,
})

const passStrength = computed(() => {
  const p = form.value.newPassword || ''
  let score = 0
  if (p.length >= 8) score++
  if (/[A-Z]/.test(p) && /[a-z]/.test(p)) score++
  if (/\d/.test(p)) score++
  return score
})

async function handleLogin() {
  errorMsg.value = ''
  if (!form.value.email || !form.value.password) {
    errorMsg.value = 'Email dan password wajib diisi.'
    return
  }
  const result = await authStore.login(form.value.email, form.value.password)
  if (result.success) {
    close()
    router.push('/dashboard')
  } else {
    errorMsg.value = result.message
  }
}

async function handleRegister() {
  errorMsg.value = ''
  if (!form.value.name || !form.value.email || !form.value.password) {
    errorMsg.value = 'Semua field wajib diisi.'
    return
  }
  const result = await authStore.register({
    name: form.value.name,
    email: form.value.email,
    password: form.value.password,
    village: form.value.village,
    role: 'petani',
  })
  if (result.success) {
    close()
    router.push('/dashboard')
  } else {
    errorMsg.value = result.message
  }
}

function focusNext(e, index) {
  if (e.target.value && index < 6) {
    const inputs = e.target.parentElement.querySelectorAll('input')
    inputs[index]?.focus()
  }
}

function close() {
  emit('close')
  errorMsg.value = ''
  setTimeout(() => {
    step.value = 'login'
    showPass.value = false
    form.value = {
      name: '', email: '', password: '',
      newPassword: '', confirmPassword: '',
      village: '', remember: false,
    }
  }, 300)
}
</script>