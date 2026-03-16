<template>
  <div class="min-h-screen flex" style="background: #0d2818;">
    <div v-if="sidebarOpen" class="fixed inset-0 z-30 bg-black/60 lg:hidden" @click="sidebarOpen = false"></div>
    <DashboardSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />

    <!-- Mobile Drawer Overlay -->
    <div v-if="drawerOpen"
      class="fixed inset-0 z-40 bg-black/70 md:hidden"
      @click="drawerOpen = false">
    </div>

    <!-- Mobile Bottom Drawer -->
    <div class="fixed bottom-0 left-0 right-0 z-50 md:hidden transition-transform duration-300 rounded-t-2xl overflow-hidden"
      :class="drawerOpen ? 'translate-y-0' : 'translate-y-full'"
      style="background: #0a1f12; border-top: 1px solid rgba(255,255,255,0.08); max-height: 70vh;">

      <!-- Drawer Handle -->
      <div class="flex justify-center pt-3 pb-2">
        <div class="w-10 h-1 bg-white/20 rounded-full"></div>
      </div>

      <div class="overflow-y-auto px-4 pb-6" style="max-height: calc(70vh - 40px);">
        <!-- Chat Baru -->
        <button @click="newChat(); drawerOpen = false"
          class="w-full flex items-center justify-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold py-2.5 rounded-xl text-sm transition mb-4">
          <Plus class="w-4 h-4" /> Chat Baru
        </button>

        <!-- Sumber Dokumen -->
        <div class="mb-4">
          <div class="flex items-center justify-between mb-3">
            <span class="text-gray-500 text-xs font-semibold tracking-widest uppercase">Sumber Dokumen</span>
            <span class="text-xs text-emerald-400 border border-emerald-700 bg-emerald-900/30 px-2 py-0.5 rounded-full font-medium">
              {{ activeDocs }} Aktif
            </span>
          </div>
          <div class="flex flex-col gap-2">
            <div v-for="doc in documents" :key="doc.id"
              class="flex items-center gap-2 px-3 py-2.5 rounded-xl border transition cursor-pointer"
              :class="doc.active ? 'border-emerald-700/50 bg-emerald-900/20' : 'border-white/5 hover:bg-white/5'"
              @click="doc.active = !doc.active">
              <component :is="doc.icon" class="w-4 h-4 shrink-0"
                :class="doc.active ? 'text-emerald-400' : 'text-gray-500'" />
              <span class="text-xs font-medium" :class="doc.active ? 'text-white' : 'text-gray-400'">{{ doc.name }}</span>
              <div v-if="doc.active" class="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0"></div>
            </div>
          </div>
        </div>

        <!-- Pertanyaan Populer -->
        <div class="mb-4">
          <div class="text-gray-500 text-xs font-semibold tracking-widest uppercase mb-3">Pertanyaan Populer</div>
          <div class="flex flex-col gap-2">
            <button v-for="q in popularQuestions" :key="q"
              @click="askQuestion(q); drawerOpen = false"
              class="text-left text-xs text-gray-400 hover:text-white px-3 py-2.5 rounded-lg hover:bg-white/5 transition border border-white/5">
              {{ q }}
            </button>
          </div>
        </div>

        <!-- Riwayat Chat -->
        <div>
          <div class="text-gray-500 text-xs font-semibold tracking-widest uppercase mb-3">Riwayat Chat</div>
          <div class="flex flex-col gap-1">
            <button v-for="h in chatHistory" :key="h.id"
              class="text-left text-xs text-gray-500 hover:text-gray-300 px-3 py-2 rounded-lg hover:bg-white/5 transition flex items-center gap-2">
              <MessageSquare class="w-3 h-3 shrink-0" />
              <span class="truncate">{{ h.title }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="flex-1 lg:ml-52 flex flex-col min-h-screen">
      <DashboardHeader title="Asisten AI" subtitle="Ask farming questions from verified documents"
        userName="Budi Pratama" userRole="Petani Kelapa" @toggle-sidebar="sidebarOpen = !sidebarOpen" />

      <main class="flex-1 flex overflow-hidden" style="height: calc(100vh - 65px);">

        <!-- SIDEBAR KIRI: Desktop only -->
        <div class="w-64 shrink-0 border-r border-white/5 flex-col overflow-y-auto hidden md:flex"
          style="background: #0a1f12;">
          <div class="p-4">
            <button @click="newChat"
              class="w-full flex items-center justify-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold py-2.5 rounded-xl text-sm transition">
              <Plus class="w-4 h-4" /> Chat Baru
            </button>
          </div>
          <div class="px-4 pb-4">
            <div class="flex items-center justify-between mb-3">
              <span class="text-gray-500 text-xs font-semibold tracking-widest uppercase">Sumber Dokumen</span>
              <span class="text-xs text-emerald-400 border border-emerald-700 bg-emerald-900/30 px-2 py-0.5 rounded-full font-medium">
                {{ activeDocs }} Aktif
              </span>
            </div>
            <div class="flex flex-col gap-2">
              <div v-for="doc in documents" :key="doc.id"
                class="flex items-center gap-2 px-3 py-2.5 rounded-xl border transition cursor-pointer"
                :class="doc.active ? 'border-emerald-700/50 bg-emerald-900/20' : 'border-white/5 hover:bg-white/5'"
                @click="doc.active = !doc.active">
                <component :is="doc.icon" class="w-4 h-4 shrink-0"
                  :class="doc.active ? 'text-emerald-400' : 'text-gray-500'" />
                <span class="text-xs font-medium truncate"
                  :class="doc.active ? 'text-white' : 'text-gray-400'">{{ doc.name }}</span>
                <div v-if="doc.active" class="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0"></div>
              </div>
            </div>
          </div>
          <div class="px-4 pb-4">
            <div class="text-gray-500 text-xs font-semibold tracking-widest uppercase mb-3">Pertanyaan Populer</div>
            <div class="flex flex-col gap-2">
              <button v-for="q in popularQuestions" :key="q"
                @click="askQuestion(q)"
                class="text-left text-xs text-gray-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition border border-white/5 hover:border-white/10">
                {{ q }}
              </button>
            </div>
          </div>
          <div class="px-4 pb-4 flex-1">
            <div class="text-gray-500 text-xs font-semibold tracking-widest uppercase mb-3">Riwayat Chat</div>
            <div class="flex flex-col gap-1">
              <button v-for="h in chatHistory" :key="h.id"
                class="text-left text-xs text-gray-500 hover:text-gray-300 px-3 py-2 rounded-lg hover:bg-white/5 transition flex items-center gap-2">
                <MessageSquare class="w-3 h-3 shrink-0" />
                <span class="truncate">{{ h.title }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- AREA CHAT UTAMA -->
        <div class="flex-1 flex flex-col overflow-hidden">

          <!-- Chat Header -->
          <div class="px-4 md:px-6 py-3 border-b border-white/5 flex items-center justify-between"
            style="background: #0d2818;">
            <div class="flex items-center gap-3">
              <div class="relative">
                <div class="w-9 h-9 rounded-xl bg-emerald-900/50 border border-emerald-700/50 flex items-center justify-center">
                  <Bot class="w-5 h-5 text-emerald-400" />
                </div>
                <div class="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border border-emerald-900"></div>
              </div>
              <div>
                <div class="text-white text-sm font-semibold">Grounded AI</div>
                <div class="flex items-center gap-1">
                  <div class="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse"></div>
                  <span class="text-emerald-400 text-xs font-medium">LIVE RESPONSE</span>
                </div>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <!-- Badge dokumen aktif -->
              <div class="hidden sm:flex items-center gap-2 text-xs text-emerald-400 border border-emerald-700/50 bg-emerald-900/20 px-3 py-1.5 rounded-full">
                <FileText class="w-3 h-3" />
                {{ activeDocs }} Dokumen Aktif
              </div>
              <!-- Tombol menu mobile -->
              <button @click="drawerOpen = true"
                class="md:hidden flex items-center gap-1.5 text-xs text-gray-400 hover:text-white border border-white/10 hover:border-white/20 px-3 py-1.5 rounded-full transition">
                <BookOpen class="w-3 h-3" />
                Menu
              </button>
            </div>
          </div>

          <!-- Messages -->
          <div ref="chatContainer" class="flex-1 overflow-y-auto px-4 md:px-6 py-4 flex flex-col gap-4"
            :style="{ paddingBottom: drawerOpen ? '0' : '1rem' }">

            <!-- Welcome state -->
            <div v-if="messages.length === 0"
              class="flex-1 flex flex-col items-center justify-center text-center py-12">
              <div class="w-16 h-16 rounded-2xl bg-emerald-900/30 border border-emerald-700/30 flex items-center justify-center mb-4">
                <Bot class="w-8 h-8 text-emerald-400" />
              </div>
              <h3 class="text-white font-semibold text-lg mb-2">RAG Agri-Assistant</h3>
              <p class="text-gray-500 text-sm max-w-sm leading-relaxed mb-6">
                Tanyakan apa saja seputar pertanian kelapa. Jawaban saya berdasarkan dokumen resmi Kementan yang terverifikasi.
              </p>
              <div class="flex flex-wrap justify-center gap-2">
                <button v-for="q in popularQuestions" :key="q"
                  @click="askQuestion(q)"
                  class="text-xs text-emerald-400 border border-emerald-700/50 bg-emerald-900/20 hover:bg-emerald-900/40 px-3 py-2 rounded-full transition">
                  {{ q }}
                </button>
              </div>
            </div>

            <!-- Verified badge -->
            <div v-if="messages.length > 0" class="flex justify-center">
              <div class="flex items-center gap-2 text-xs text-gray-500 border border-white/5 px-3 py-1.5 rounded-full">
                <ShieldCheck class="w-3 h-3 text-emerald-400" />
                Jawaban Terverifikasi Dokumen Resmi
              </div>
            </div>

            <!-- Chat messages -->
            <template v-for="msg in messages" :key="msg.id">
              <div v-if="msg.role === 'user'" class="flex justify-end">
                <div class="flex items-end gap-2 max-w-[85%] md:max-w-[75%]">
                  <div class="bg-emerald-800/60 border border-emerald-700/40 rounded-2xl rounded-br-sm px-4 py-3 text-sm text-white">
                    {{ msg.content }}
                  </div>
                  <div class="w-8 h-8 rounded-full bg-amber-500 flex items-center justify-center text-black font-bold text-xs shrink-0">
                    B
                  </div>
                </div>
              </div>
              <div v-if="msg.role === 'ai'" class="flex justify-start">
                <div class="flex items-start gap-2 max-w-[90%] md:max-w-[80%]">
                  <div class="w-8 h-8 rounded-xl bg-emerald-900/50 border border-emerald-700/50 flex items-center justify-center shrink-0 mt-1">
                    <Bot class="w-4 h-4 text-emerald-400" />
                  </div>
                  <div class="rounded-2xl rounded-tl-sm px-4 py-3 text-sm text-gray-200 leading-relaxed border border-white/5"
                    style="background: rgba(255,255,255,0.05);">
                    <div v-html="msg.content"></div>
                    <div v-if="msg.source" class="mt-3 pt-3 border-t border-white/5 flex items-center gap-2">
                      <FileText class="w-3 h-3 text-amber-400 shrink-0" />
                      <span class="text-xs text-amber-400 font-medium">Sumber Terverifikasi:</span>
                      <span class="text-xs text-amber-300">{{ msg.source }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <!-- Typing indicator -->
            <div v-if="isTyping" class="flex justify-start">
              <div class="flex items-start gap-2">
                <div class="w-8 h-8 rounded-xl bg-emerald-900/50 border border-emerald-700/50 flex items-center justify-center shrink-0">
                  <Bot class="w-4 h-4 text-emerald-400" />
                </div>
                <div class="rounded-2xl rounded-tl-sm px-4 py-3 border border-white/5" style="background: rgba(255,255,255,0.05);">
                  <div class="flex items-center gap-1">
                    <div class="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
                    <div class="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
                    <div class="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input Area -->
          <div class="px-4 md:px-6 py-3 md:py-4 border-t border-white/5" style="background: #0d2818;">
            <div class="flex items-end gap-3 rounded-2xl border border-white/10 px-4 py-3"
              style="background: rgba(255,255,255,0.04);">
              <textarea
                v-model="inputMessage"
                @keydown.enter.prevent="sendMessage"
                placeholder="Tanyakan seputar pertanian atau regulasi..."
                rows="1"
                class="flex-1 bg-transparent text-sm text-white placeholder-gray-600 outline-none resize-none leading-relaxed"
                style="max-height: 120px;"
                @input="autoResize"
                ref="textarea"
              ></textarea>
              <div class="flex items-center gap-2 shrink-0">
                <button class="text-gray-500 hover:text-gray-300 transition p-1">
                  <Mic class="w-4 h-4" />
                </button>
                <button @click="sendMessage"
                  :disabled="!inputMessage.trim() || isTyping"
                  class="w-8 h-8 rounded-xl flex items-center justify-center transition"
                  :class="inputMessage.trim() && !isTyping
                    ? 'bg-amber-500 hover:bg-amber-400 text-black'
                    : 'bg-white/5 text-gray-600 cursor-not-allowed'">
                  <Send class="w-4 h-4" />
                </button>
              </div>
            </div>
            <p class="text-center text-gray-700 text-xs mt-2">POWERED BY COCOPRA SECURE RAG</p>
          </div>

        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { Bot, Plus, FileText, MessageSquare, ShieldCheck, Mic, Send, BookOpen } from 'lucide-vue-next'
import DashboardSidebar from '../../components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '../../components/dashboard/DashboardHeader.vue'
import api from '../../api/axios.js'

const sidebarOpen = ref(false)
const drawerOpen = ref(false)
const inputMessage = ref('')
const isTyping = ref(false)
const chatContainer = ref(null)
const textarea = ref(null)
const messages = ref([])

const documents = ref([
  { id: 1, name: 'SOP PHT 2023', icon: FileText, active: true },
  { id: 2, name: 'Regulasi Pestisida v4', icon: ShieldCheck, active: true },
  { id: 3, name: 'Panduan Balitka', icon: FileText, active: true },
])

const activeDocs = computed(() => documents.value.filter(d => d.active).length)

const popularQuestions = [
  'Dosis pupuk NPK?',
  'Gejala Brontispa',
  'Masa panen ideal',
]

const chatHistory = ref([
  { id: 1, title: 'Penanganan hama kelapa...' },
  { id: 2, title: 'Standar kualitas kopra...' },
])

async function sendMessage() {
  if (!inputMessage.value.trim() || isTyping.value) return
  const userMsg = inputMessage.value.trim()
  inputMessage.value = ''
  if (textarea.value) textarea.value.style.height = 'auto'

  messages.value.push({ id: Date.now(), role: 'user', content: userMsg })
  await scrollToBottom()

  isTyping.value = true
  await scrollToBottom()

  try {
    // Bangun history format backend: [{ role: "user"|"model", parts: "..." }]
    const chatHistoryForAPI = messages.value
      .filter(m => m.role === 'user' || m.role === 'ai')
      .slice(0, -1) // Jangan sertakan pesan terakhir (sudah jadi `message`)
      .map(m => ({
        role: m.role === 'ai' ? 'model' : 'user',
        parts: m.content.replace(/<[^>]*>/g, '') // Strip HTML tags untuk history
      }))

    const res = await api.post('/assistant/chat', {
      history: chatHistoryForAPI,
      message: userMsg,
    })

    const data = res.data
    isTyping.value = false

    // Format reply — ganti newline dengan <br/> untuk tampilan HTML
    const formattedReply = data.reply
      .replace(/\n/g, '<br/>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')

    const source = data.regulatory_flag ? 'Peringatan Regulasi Terdeteksi' : null

    messages.value.push({
      id: Date.now() + 1,
      role: 'ai',
      content: formattedReply,
      source: source,
    })
  } catch (err) {
    console.error('Chat API error, fallback ke mock:', err)
    isTyping.value = false

    // Fallback mock response
    const fallbackResponse = getFallbackResponse(userMsg)
    messages.value.push({
      id: Date.now() + 1,
      role: 'ai',
      content: fallbackResponse.content,
      source: fallbackResponse.source,
    })
  }

  if (chatHistory.value.length < 5) {
    chatHistory.value.unshift({ id: Date.now(), title: userMsg.substring(0, 30) + '...' })
  }

  await scrollToBottom()
}

// Fallback jika API tidak tersedia
function getFallbackResponse(question) {
  const q = question.toLowerCase()
  if (q.includes('brontispa') || q.includes('hama')) {
    return {
      content: `Berdasarkan <span class="text-amber-400 font-medium">SOP PHT Kelapa 2023</span>, penanganan hama meliputi:<br/><br/>
      <ol class="list-decimal list-inside space-y-2">
        <li><strong>Mekanis:</strong> Pemangkasan pelepah terserang.</li>
        <li><strong>Hayati:</strong> Jamur entomopatogen <em class="text-emerald-400">Beauveria bassiana</em>.</li>
        <li><strong>Kimiawi:</strong> Insektisida sistemik (Imidakloprid) 1-2 ml/liter air.</li>
      </ol><br/><em class="text-gray-500 text-xs">[Mode Offline — Backend tidak tersedia]</em>`,
      source: 'SOP PHT Kelapa 2023 (Offline Cache)'
    }
  }
  if (q.includes('pupuk') || q.includes('npk')) {
    return {
      content: `Berdasarkan <span class="text-amber-400 font-medium">Panduan Balitka</span>, dosis pupuk NPK kelapa:<br/><br/>
      <ul class="list-disc list-inside space-y-2">
        <li><strong>Kelapa Muda (0-3 tahun):</strong> 500g NPK 15-15-15/pohon/tahun</li>
        <li><strong>Kelapa Produktif (>3 tahun):</strong> 1-2 kg NPK 15-15-15/pohon/tahun</li>
        <li><strong>Waktu:</strong> 2x setahun, awal & akhir musim hujan</li>
      </ul><br/><em class="text-gray-500 text-xs">[Mode Offline — Backend tidak tersedia]</em>`,
      source: 'Panduan Teknis Pemupukan Kelapa, Balitka 2022 (Offline Cache)'
    }
  }
  return {
    content: `Maaf, saya tidak dapat menghubungi server AI saat ini. Silakan periksa koneksi Anda atau coba lagi nanti.<br/><br/>
    <em class="text-gray-500 text-xs">[Mode Offline — Backend tidak tersedia]</em>`,
    source: null
  }
}

function askQuestion(q) {
  inputMessage.value = q
  sendMessage()
}

function newChat() {
  messages.value = []
  inputMessage.value = ''
}

async function scrollToBottom() {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

function autoResize(e) {
  e.target.style.height = 'auto'
  e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px'
}
</script>