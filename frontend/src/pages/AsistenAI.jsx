import { useState, useRef, useEffect } from 'react'
import { Bot, MessageSquare, ShieldAlert, Send, CheckCircle2, AlertTriangle, Ban, BookOpen, Search, Leaf, ShieldPlus, User } from 'lucide-react'
import './PageStyles.css'

function AsistenAI() {
    const [messages, setMessages] = useState([
        {
            role: 'model',
            parts: 'Halo! Saya asisten AI pertanian Cocopra.id. Saya dapat membantu Anda dengan:\n- Identifikasi dan penanganan hama kelapa\n- Informasi regulasi pestisida (Permentan)\n- SOP budidaya kelapa dan kopra\n- Rekomendasi pengendalian hama terpadu'
        }
    ])
    const [inputValue, setInputValue] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const [regulatoryStatus, setRegulatoryStatus] = useState('unknown') // unknown, safe, warning, danger
    const chatEndRef = useRef(null)

    // Auto-scroll ke bawah saat ada pesan baru
    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    const handleSendMessage = async () => {
        if (!inputValue.trim()) return

        const userMsg = { role: 'user', parts: inputValue }
        setMessages(prev => [...prev, userMsg])
        setInputValue('')
        setIsLoading(true)

        // Reset regulatory status setiap pesan baru jika tidak ada warning sebelumnya
        if (regulatoryStatus !== 'danger') {
            setRegulatoryStatus('unknown')
        }

        try {
            // Hit backend RAG endpoint
            const response = await fetch('/api/assistant/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    history: messages.slice(1), // Kirim history tanpa pesan selamat datang pertama
                    message: userMsg.parts
                })
            })

            if (!response.ok) throw new Error('Network response was not ok')
            const data = await response.json()

            setMessages(prev => [...prev, { role: 'model', parts: data.reply }])

            if (data.regulatory_flag) {
                setRegulatoryStatus('danger')
            } else {
                setRegulatoryStatus('safe')
            }

        } catch (error) {
            console.error("Chat error:", error)
            setMessages(prev => [...prev, { role: 'model', parts: 'Maaf, sepertinya ada gangguan koneksi ke server AI.' }])
        } finally {
            setIsLoading(false)
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleSendMessage()
        }
    }

    return (
        <div className="page animate-fade-in">
            <div className="page__hero page__hero--blue">
                <span className="page__hero-icon">
                    <Bot size={40} strokeWidth={1.5} color="var(--color-info)" />
                </span>
                <div className="page__hero-content">
                    <h2 className="page__hero-title">RAG Agri-Assistant</h2>
                    <p className="page__hero-desc">
                        Chatbot pertanian yang <strong>grounded</strong> pada dokumen regulasi resmi (Permentan dan SOP Dinas Pertanian).
                        Setiap jawaban bersumber dan dapat diaudit — AI yang <strong>bertanggung jawab</strong>.
                    </p>
                </div>
            </div>

            <div className="page__content-grid">
                {/* Chat Area */}
                <div className="card page__feature-card chat-card">
                    <div className="page__feature-header">
                        <span className="page__feature-icon">
                            <MessageSquare size={24} strokeWidth={2} color="var(--color-info)" />
                        </span>
                        <h3>Konsultasi Pertanian</h3>
                    </div>
                    <div className="chat__area" id="chat-area">
                        {messages.map((msg, index) => (
                            <div key={index} className={`chat__message ${msg.role === 'model' ? 'chat__message--bot' : 'chat__message--user'}`}>
                                <span className="chat__avatar">
                                    {msg.role === 'model' ? (
                                        <Bot size={24} strokeWidth={2} color="var(--color-primary-600)" />
                                    ) : (
                                        <User size={24} strokeWidth={2} color="#fff" />
                                    )}
                                </span>
                                <div className="chat__bubble" style={{ whiteSpace: 'pre-wrap' }}>
                                    <p>{msg.parts}</p>
                                    {msg.role === 'model' && index === 0 && (
                                        <p className="chat__source">
                                            <BookOpen size={12} className="inline-icon" /> Sumber: Database Regulasi Permentan & SOP Dinas Pertanian Minahasa Utara
                                        </p>
                                    )}
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="chat__message chat__message--bot">
                                <span className="chat__avatar"><Bot size={24} strokeWidth={2} color="var(--color-primary-600)" /></span>
                                <div className="chat__bubble"><p className="chat__loading">Sedang mencari referensi hukum...</p></div>
                            </div>
                        )}
                        <div ref={chatEndRef} />
                    </div>
                    <div className="chat__input-area">
                        <input
                            type="text"
                            className="chat__input"
                            placeholder="Ketik pertanyaan Anda di sini..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyDown={handleKeyDown}
                            disabled={isLoading}
                        />
                        <button className="btn-primary chat__send" onClick={handleSendMessage} disabled={isLoading || !inputValue.trim()}>
                            <Send size={18} strokeWidth={2} />
                        </button>
                    </div>
                </div>

                {/* Regulatory Check */}
                <div className="card page__feature-card">
                    <div className="page__feature-header">
                        <span className="page__feature-icon">
                            <ShieldAlert size={24} strokeWidth={2} color="var(--color-primary-600)" />
                        </span>
                        <h3>Regulatory Compliance Check</h3>
                    </div>
                    <p className="reg__desc">Verifikasi legalitas bahan kimia pertanian dengan sistem lampu lalu lintas:</p>
                    <div className="reg__traffic-light">
                        <div className={`reg__light reg__light--green ${regulatoryStatus === 'safe' ? 'active' : ''}`} style={{ opacity: regulatoryStatus === 'safe' ? 1 : 0.4 }}>
                            <span className="reg__light-icon">
                                <CheckCircle2 size={24} strokeWidth={2} />
                            </span>
                            <div>
                                <strong>Aman / Disetujui</strong>
                                <span>Tindakan sesuai SOP/Permentan</span>
                            </div>
                        </div>
                        <div className={`reg__light reg__light--yellow ${regulatoryStatus === 'warning' ? 'active' : ''}`} style={{ opacity: regulatoryStatus === 'warning' ? 1 : 0.4 }}>
                            <span className="reg__light-icon">
                                <AlertTriangle size={24} strokeWidth={2} />
                            </span>
                            <div>
                                <strong>Dibatasi/Dievaluasi</strong>
                                <span>Penggunaan terbatas/sedang ditinjau</span>
                            </div>
                        </div>
                        <div className={`reg__light reg__light--red ${regulatoryStatus === 'danger' ? 'active' : ''}`} style={{ opacity: regulatoryStatus === 'danger' ? 1 : 0.4 }}>
                            <span className="reg__light-icon">
                                <Ban size={24} strokeWidth={2} />
                            </span>
                            <div>
                                <strong>Ilegal/Dicabut</strong>
                                <span>Dilarang keras — pelanggaran hukum</span>
                            </div>
                        </div>
                    </div>
                    <div className="reg__search">
                        <p style={{ fontSize: '0.85rem', color: 'var(--color-primary-600)' }}>Status ini otomatis dievaluasi oleh RAG Engine berdasarkan percakapan chat di atas.</p>
                    </div>
                </div>
            </div>

            <div className="card page__info-card">
                <span className="page__info-icon">
                    <BookOpen size={28} strokeWidth={2} color="var(--color-warning)" />
                </span>
                <div>
                    <h4>Responsible AI — RAG Grounded</h4>
                    <p>Setiap jawaban chatbot bersumber dari dokumen resmi yang tersimpan di knowledge base. Confidence score ditampilkan secara transparan. Jika akurasi di bawah threshold, sistem akan merujuk ke Penyuluh Lapangan.</p>
                </div>
            </div>
        </div>
    )
}

export default AsistenAI
