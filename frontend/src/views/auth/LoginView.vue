<template>
  <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">NOMS</h1>
      <p class="text-gray-500 mt-1 text-sm">Network Operations & Monitoring System</p>
    </div>

    <!-- LOGIN FORM -->
    <form v-if="mode === 'login'" @submit.prevent="handleLogin" class="space-y-4">
      <BaseInput v-model="username" label="Username" placeholder="admin" required />
      <BaseInput v-model="password" type="password" label="Password" placeholder="••••••" required />

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg">
        {{ error }}
      </div>

      <BaseButton type="submit" :loading="loading" class="w-full">
        {{ loading ? 'Logging in...' : 'Login' }}
      </BaseButton>

      <div class="text-center">
        <button type="button" class="text-sm text-blue-600 hover:underline" @click="mode = 'forgot'">
          Forgot Password?
        </button>
      </div>
    </form>

    <!-- FORGOT PASSWORD - STEP 1 (Email) -->
    <form v-else-if="mode === 'forgot'" @submit.prevent="handleForgotPassword" class="space-y-4">
      <div class="text-center mb-4">
        <h2 class="text-xl font-bold text-gray-800">Forgot Password</h2>
        <p class="text-sm text-gray-500 mt-1">Enter your email to receive reset code</p>
      </div>

      <BaseInput v-model="forgotEmail" type="email" label="Email" placeholder="admin@noms.com" required />

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg">
        {{ error }}
      </div>

      <div v-if="devCode" class="bg-yellow-50 border border-yellow-200 text-yellow-800 text-sm p-3 rounded-lg">
        <p class="font-medium">🔧 Dev Mode (SMTP not configured)</p>
        <p class="mt-1">Reset code: <span class="font-mono font-bold text-lg">{{ devCode }}</span></p>
      </div>

      <BaseButton type="submit" :loading="loading" class="w-full">
        {{ loading ? 'Sending...' : 'Send Reset Code' }}
      </BaseButton>

      <div class="text-center">
        <button type="button" class="text-sm text-blue-600 hover:underline" @click="backToLogin">
          ← Back to Login
        </button>
      </div>
    </form>

    <!-- FORGOT PASSWORD - STEP 2 (Code + New Password) -->
    <form v-else-if="mode === 'reset'" @submit.prevent="handleResetPassword" class="space-y-4">
      <div class="text-center mb-4">
        <h2 class="text-xl font-bold text-gray-800">Reset Password</h2>
        <p class="text-sm text-gray-500 mt-1">Enter the code and your new password</p>
      </div>

      <BaseInput v-model="resetCode" label="Reset Code" placeholder="123456" required />
      <BaseInput v-model="newPassword" type="password" label="New Password" placeholder="Minimum 6 characters" required />

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg">
        {{ error }}
      </div>

      <BaseButton type="submit" :loading="loading" class="w-full">
        {{ loading ? 'Resetting...' : 'Reset Password' }}
      </BaseButton>

      <div class="text-center">
        <button type="button" class="text-sm text-blue-600 hover:underline" @click="backToLogin">
          ← Back to Login
        </button>
      </div>
    </form>

    <p v-if="mode === 'login'" class="text-center text-xs text-gray-400 mt-6">
      Default: admin / admin123
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { authApi } from '@/api/auth'
import { useToast } from '@/composables/useToast'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

// Login
const username = ref('')
const password = ref('')

// Forgot
const mode = ref('login') // login | forgot | reset
const forgotEmail = ref('')
const resetCode = ref('')
const newPassword = ref('')
const devCode = ref('')

// Common
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}

async function handleForgotPassword() {
  error.value = ''
  devCode.value = ''
  loading.value = true
  try {
    const { data } = await authApi.forgotPassword(forgotEmail.value)
    if (data.dev_code) {
      devCode.value = data.dev_code
      resetCode.value = data.dev_code
      toast.info('Dev mode: code shown above')
    } else {
      toast.success('Reset code sent to email')
    }
    setTimeout(() => (mode.value = 'reset'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to send code'
  } finally {
    loading.value = false
  }
}

async function handleResetPassword() {
  error.value = ''
  loading.value = true
  try {
    await authApi.resetPassword(forgotEmail.value, resetCode.value, newPassword.value)
    toast.success('Password reset! Please login.')
    backToLogin()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Reset failed'
  } finally {
    loading.value = false
  }
}

function backToLogin() {
  mode.value = 'login'
  error.value = ''
  forgotEmail.value = ''
  resetCode.value = ''
  newPassword.value = ''
  devCode.value = ''
}
</script>