import { useState, useEffect } from 'react'
import { CircleDollarSign, ClipboardEdit, TrendingUp, ShieldCheck, Wifi, WifiOff } from 'lucide-react'
import { saveToQueue, STORES } from '../lib/db'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import './PageStyles.css'

function InfoHarga() {
    const [harga, setHarga] = useState('')
    const [lokasi, setLokasi] = useState('')
    const [pembeli, setPembeli] = useState('')
    const [isOnline, setIsOnline] = useState(navigator.onLine)
    const [statusMsg, setStatusMsg] = useState(null)
    const [trendData, setTrendData] = useState([])
    const [medianData, setMedianData] = useState(null)

    useEffect(() => {
        const handleOnline = () => setIsOnline(true)
        const handleOffline = () => setIsOnline(false)
        window.addEventListener('online', handleOnline)
        window.addEventListener('offline', handleOffline)

        // Fetch trend data
        fetch('/api/harga/trend')
            .then(res => res.json())
            .then(data => setTrendData(data))
            .catch(err => console.error("Gagal memuat tren", err))

        // Fetch median data
        fetch('/api/harga/median')
            .then(res => res.json())
            .then(data => setMedianData(data))
            .catch(err => console.error("Gagal memuat median", err))

        return () => {
            window.removeEventListener('online', handleOnline)
            window.removeEventListener('offline', handleOffline)
        }
    }, [])

    const handleSubmit = async () => {
        if (!harga || !lokasi) {
            setStatusMsg({ type: 'error', text: 'Harga dan Lokasi wajib diisi.' })
            return
        }

        const payload = {
            harga: parseInt(harga),
            lokasi,
            pembeli,
            timestamp: new Date().toISOString()
        }

        try {
            if (isOnline) {
                // Tembak langsung ke API Backend FastAPI
                const response = await fetch('/api/harga/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) throw new Error('API request failed');

                setStatusMsg({ type: 'success', text: 'Laporan berhasil terkirim ke server!' })
            } else {
                throw new Error('Offline')
            }
        } catch (error) {
            // Fallback to IndexedDB queue if offline or API fails
            await saveToQueue(STORES.HARGA, payload)
            setStatusMsg({ type: 'warning', text: 'Tersimpan Offline. Data akan dikirim otomatis saat sinyal kembali.' })

            // Register background sync if supported
            if ('serviceWorker' in navigator && 'SyncManager' in window) {
                const sw = await navigator.serviceWorker.ready
                sw.sync.register('sync-harga-input').catch(console.error)
            }
        }

        // Reset form
        setHarga('')
        setLokasi('')
        setPembeli('')
        setTimeout(() => setStatusMsg(null), 5000)
    }
    return (
        <div className="page animate-fade-in">
            <div className="page__hero page__hero--amber">
                <span className="page__hero-icon">
                    <CircleDollarSign size={40} strokeWidth={1.5} color="var(--color-accent-500)" />
                </span>
                <div className="page__hero-content">
                    <h2 className="page__hero-title">Adil-Harga Ledger</h2>
                    <p className="page__hero-desc">
                        Dashboard transparansi harga kopra regional. Input harga harian secara <strong>crowdsourced</strong> dan
                        pantau anomali harga yang dideteksi oleh algoritma <strong>Isolation Forest</strong>.
                    </p>
                </div>
            </div>

            <div className="page__content-grid">
                {/* Input Harga */}
                <div className="card page__feature-card">
                    <div className="page__feature-header">
                        <span className="page__feature-icon">
                            <ClipboardEdit size={24} strokeWidth={2} color="var(--color-accent-500)" />
                        </span>
                        <h3>Input Harga Hari Ini</h3>
                    </div>
                    <div className="harga__form">
                        <div className="harga__field">
                            <label className="harga__label">Harga Kopra (Rp/kg)</label>
                            <input type="number" className="harga__input" placeholder="Contoh: 8500" value={harga} onChange={e => setHarga(e.target.value)} id="harga-input" />
                        </div>
                        <div className="harga__field">
                            <label className="harga__label">Lokasi Desa</label>
                            <input type="text" className="harga__input" placeholder="Nama desa/kecamatan" value={lokasi} onChange={e => setLokasi(e.target.value)} id="harga-location" />
                        </div>
                        <div className="harga__field">
                            <label className="harga__label">Pembeli/Tengkulak</label>
                            <input type="text" className="harga__input" placeholder="Nama pembeli (opsional)" value={pembeli} onChange={e => setPembeli(e.target.value)} id="harga-buyer" />
                        </div>
                        <button className="btn-primary harga__submit" onClick={handleSubmit} id="harga-submit-btn">
                            Kirim Laporan Harga
                        </button>

                        {statusMsg && (
                            <div className={`form__feedback form__feedback--${statusMsg.type}`}>
                                {statusMsg.type === 'error' ? '❌' : statusMsg.type === 'warning' ? <WifiOff size={16} /> : <Wifi size={16} />}
                                <span>{statusMsg.text}</span>
                            </div>
                        )}
                    </div>
                    <div className="page__feature-badges">
                        <span className="badge badge--success">Offline-Ready</span>
                        <span className="badge badge--success">Anomaly Protected</span>
                    </div>
                </div>

                {/* Grafik Harga */}
                <div className="card page__feature-card">
                    <div className="page__feature-header">
                        <span className="page__feature-icon">
                            <TrendingUp size={24} strokeWidth={2} color="var(--color-primary-500)" />
                        </span>
                        <h3>Tren Harga 30 Hari</h3>
                    </div>
                    <div className="harga__chart-container" style={{ width: '100%', height: 250, marginTop: '2rem' }}>
                        {trendData.length > 0 ? (
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={trendData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                                    <XAxis dataKey="date" stroke="var(--color-text-muted)" fontSize={12} tickLine={false} />
                                    <YAxis stroke="var(--color-text-muted)" fontSize={12} tickLine={false} axisLine={false} domain={['dataMin - 100', 'dataMax + 100']} />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: 'var(--color-surface)', border: '1px solid var(--color-surface-hover)', borderRadius: '8px', color: '#fff' }}
                                        itemStyle={{ color: 'var(--color-primary-400)' }}
                                    />
                                    <Line type="monotone" dataKey="harga" stroke="var(--color-primary-500)" strokeWidth={3} dot={{ r: 4, fill: 'var(--color-surface)', strokeWidth: 2 }} activeDot={{ r: 6 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        ) : (
                            <p style={{ textAlign: 'center', color: 'var(--color-text-muted)', paddingTop: '5rem' }}>Memuat grafik interaktif...</p>
                        )}
                    </div>
                    <div className="harga__median">
                        <span>Median Regional:</span>
                        <strong>{medianData ? `Rp ${medianData.median.toLocaleString('id-ID')}/kg` : 'Memuat...'}</strong>
                        {medianData && <span style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', marginLeft: '0.5rem' }}>({medianData.count} data, Min: Rp {medianData.min.toLocaleString('id-ID')}, Max: Rp {medianData.max.toLocaleString('id-ID')})</span>}
                    </div>
                </div>
            </div>

            <div className="card page__info-card">
                <span className="page__info-icon">
                    <ShieldCheck size={28} strokeWidth={2} color="var(--color-warning)" />
                </span>
                <div>
                    <h4>Intelligence for Justice — Anomaly Detection</h4>
                    <p>Algoritma Isolation Forest dan Z-Score secara otomatis menyaring input harga yang mencurigakan (terlalu tinggi/rendah). Data yang lolos validasi membangun indeks harga regional yang adil untuk semua petani.</p>
                </div>
            </div>
        </div>
    )
}

export default InfoHarga
