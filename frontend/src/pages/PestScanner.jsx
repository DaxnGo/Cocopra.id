import { useState, useEffect } from 'react'
import { ScanSearch, Camera, Image, ShieldCheck, Activity, AlertCircle, Wifi, WifiOff, XCircle } from 'lucide-react'
import { saveToQueue, STORES } from '../lib/db'
import './PageStyles.css'

function PestScanner() {
    const [file, setFile] = useState(null)
    const [isOnline, setIsOnline] = useState(navigator.onLine)
    const [statusMsg, setStatusMsg] = useState(null)
    const [scanResult, setScanResult] = useState(null)

    useEffect(() => {
        const handleOnline = () => setIsOnline(true)
        const handleOffline = () => setIsOnline(false)
        window.addEventListener('online', handleOnline)
        window.addEventListener('offline', handleOffline)
        return () => {
            window.removeEventListener('online', handleOnline)
            window.removeEventListener('offline', handleOffline)
        }
    }, [])

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0])
        }
    }

    const handleScan = async () => {
        if (!file) {
            setStatusMsg({ type: 'error', text: 'Pilih foto tanaman terlebih dahulu.' })
            return
        }

        // Simulate reading file as base64 for offline storage
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onloadend = async () => {
            const base64data = reader.result

            const payload = {
                image_data: base64data,
                filename: file.name,
                timestamp: new Date().toISOString()
            }

            try {
                if (isOnline) {
                    const response = await fetch('/api/pest/scan', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    })

                    if (!response.ok) throw new Error('API request failed')

                    const result = await response.json()
                    setScanResult(result)

                    setStatusMsg({ type: 'success', text: `Analisis selesai!` })
                } else {
                    throw new Error('Offline')
                }
            } catch (error) {
                // Save to IDB Queue
                await saveToQueue(STORES.PEST, payload)
                setStatusMsg({ type: 'warning', text: 'Tersimpan Offline. Akan dianalisis otomatis saat sinyal kembali.' })

                if ('serviceWorker' in navigator && 'SyncManager' in window) {
                    try {
                        const sw = await navigator.serviceWorker.ready
                        await sw.sync.register('sync-pest-scan')
                    } catch (e) {
                        console.error('BG Sync failed:', e)
                    }
                }
            }

            setFile(null)
            setTimeout(() => setStatusMsg(null), 5000)
        }
    }
    return (
        <div className="page animate-fade-in">
            <div className="page__hero page__hero--green">
                <span className="page__hero-icon">
                    <ScanSearch size={40} strokeWidth={1.5} color="var(--color-primary-600)" />
                </span>
                <div className="page__hero-content">
                    <h2 className="page__hero-title">Pest-Vision Scanner</h2>
                    <p className="page__hero-desc">
                        Deteksi hama <strong>Pseudococcus</strong> dan penyakit kelapa lainnya secara instan menggunakan
                        kecerdasan buatan Gemini Vision API. Cukup arahkan kamera ke tanaman yang terinfeksi.
                    </p>
                </div>
            </div>

            {/* Scanner Area */}
            <div className="page__content-grid">
                <div className="card page__feature-card">
                    <div className="page__feature-header">
                        <span className="page__feature-icon">
                            <Camera size={24} strokeWidth={2} color="var(--color-primary-600)" />
                        </span>
                        <h3>Ambil Foto Tanaman</h3>
                    </div>
                    <div className="scanner__upload-area" id="pest-upload-area" style={{ position: 'relative' }}>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                            style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', opacity: 0, cursor: 'pointer' }}
                            id="pest-file-input"
                        />
                        <div className="scanner__upload-placeholder">
                            <span className="scanner__upload-icon">
                                <Image size={48} strokeWidth={1} color="var(--color-text-muted)" />
                            </span>
                            <p className="scanner__upload-text">
                                {file ? `File terpilih: ${file.name}` : 'Ketuk untuk mengambil foto atau unggah dari galeri'}
                            </p>
                            <span className="scanner__upload-hint">Format: JPG, PNG — Max 10MB</span>
                        </div>
                    </div>
                    {file && (
                        <div style={{ marginTop: 'var(--space-4)', textAlign: 'center' }}>
                            <button className="btn-primary" onClick={handleScan} id="pest-scan-btn">
                                <ScanSearch size={20} /> Mulai Analisis AI
                            </button>
                        </div>
                    )}

                    {statusMsg && (
                        <div className={`form__feedback form__feedback--${statusMsg.type}`}>
                            {statusMsg.type === 'error' ? '❌' : statusMsg.type === 'warning' ? <WifiOff size={16} /> : <Wifi size={16} />}
                            <span>{statusMsg.text}</span>
                        </div>
                    )}
                    <div className="page__feature-badges">
                        <span className="badge badge--success">Offline-Ready</span>
                        <span className="badge badge--warning">Auto-Sync saat Online</span>
                    </div>
                </div>

                <div className="card page__feature-card">
                    <div className="page__feature-header">
                        <span className="page__feature-icon">
                            <Activity size={24} strokeWidth={2} color="var(--color-primary-600)" />
                        </span>
                        <h3>Hasil Analisis AI</h3>
                    </div>
                    <div className="scanner__result-area">
                        {scanResult ? (
                            <div className="scanner__result-content">
                                <span className="scanner__result-icon">
                                    {scanResult.confidence_score === 0 ? (
                                        <XCircle size={32} strokeWidth={2} color="var(--color-danger, #ef4444)" />
                                    ) : scanResult.confidence_score > 0.5 ? (
                                        <AlertCircle size={32} strokeWidth={2} color="var(--color-warning)" />
                                    ) : (
                                        <ShieldCheck size={32} strokeWidth={2} color="var(--color-primary-600)" />
                                    )}
                                </span>
                                <p style={{ fontSize: '0.95rem', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>{scanResult.result_label}</p>
                            </div>
                        ) : (
                            <div className="scanner__result-placeholder">
                                <span className="scanner__result-icon">
                                    <ScanSearch size={40} strokeWidth={1} color="var(--color-text-muted)" />
                                </span>
                                <p>Hasil deteksi akan muncul di sini setelah analisis</p>
                            </div>
                        )}
                    </div>
                    <div className="scanner__confidence">
                        <span className="scanner__confidence-label">Confidence Score</span>
                        <div className="scanner__confidence-bar">
                            <div className="scanner__confidence-fill" style={{ width: scanResult ? `${Math.round(scanResult.confidence_score * 100)}%` : '0%', transition: 'width 0.8s ease' }}></div>
                        </div>
                        <span className="scanner__confidence-value">{scanResult ? `${Math.round(scanResult.confidence_score * 100)}%` : '—'}</span>
                    </div>
                </div>
            </div>

            {/* Info */}
            <div className="card page__info-card">
                <span className="page__info-icon">
                    <AlertCircle size={28} strokeWidth={2} color="var(--color-warning)" />
                </span>
                <div>
                    <h4>Responsible AI — Transparansi Penuh</h4>
                    <p>Jika confidence score di bawah threshold, sistem akan merekomendasikan untuk menghubungi Penyuluh Lapangan terdekat melalui WhatsApp. AI adalah alat bantu, bukan pengganti keahlian manusia.</p>
                </div>
            </div>
        </div>
    )
}

export default PestScanner
