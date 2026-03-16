import { useState, useEffect } from 'react'
import { ScanSearch, DollarSign, AlertTriangle, MessageSquare, Camera, ClipboardEdit, Map, Sprout, Lightbulb } from 'lucide-react'
import './Dashboard.css'

function Dashboard() {
    const [stats, setStats] = useState({
        totalScan: '...',
        hargaHariIni: '...',
        peringatanAktif: '...',
        konsultasiAI: '0',
    })

    useEffect(() => {
        // Fetch harga terbaru
        fetch('/api/harga/?limit=1')
            .then(res => res.json())
            .then(data => {
                if (data.length > 0) {
                    setStats(prev => ({ ...prev, hargaHariIni: `Rp ${data[0].harga.toLocaleString('id-ID')}` }))
                } else {
                    setStats(prev => ({ ...prev, hargaHariIni: '—' }))
                }
            })
            .catch(() => setStats(prev => ({ ...prev, hargaHariIni: '—' })))

        // Fetch geo dashboard stats
        fetch('/api/geo/dashboard')
            .then(res => res.json())
            .then(data => {
                setStats(prev => ({
                    ...prev,
                    totalScan: String(data.total_scan_hama || 0),
                    peringatanAktif: String(data.peringatan_aktif || 0),
                }))
            })
            .catch(() => {
                setStats(prev => ({ ...prev, totalScan: '0', peringatanAktif: '0' }))
            })
    }, [])

    const quickStats = [
        { icon: <ScanSearch size={26} strokeWidth={2} />, label: 'Total Scan Hama', value: stats.totalScan, color: 'green' },
        { icon: <DollarSign size={26} strokeWidth={2} />, label: 'Harga Kopra Terbaru', value: stats.hargaHariIni, color: 'amber' },
        { icon: <AlertTriangle size={26} strokeWidth={2} />, label: 'Peringatan Aktif', value: stats.peringatanAktif, color: 'red' },
        { icon: <MessageSquare size={26} strokeWidth={2} />, label: 'Konsultasi AI', value: stats.konsultasiAI, color: 'blue' },
    ]

    const quickActions = [
        {
            icon: <Camera size={28} strokeWidth={1.5} />,
            title: 'Scan Hama Baru',
            desc: 'Ambil foto tanaman kelapa untuk mendeteksi hama Pseudococcus secara instan menggunakan AI.',
            link: '/pest-scanner',
            color: 'green',
        },
        {
            icon: <ClipboardEdit size={28} strokeWidth={1.5} />,
            title: 'Laporkan Harga',
            desc: 'Input harga kopra hari ini di desa Anda untuk membangun transparansi pasar komunitas.',
            link: '/info-harga',
            color: 'amber',
        },
        {
            icon: <MessageSquare size={28} strokeWidth={1.5} />,
            title: 'Tanya Asisten AI',
            desc: 'Konsultasi regulasi pestisida, SOP penanganan hama, atau informasi pertanian lainnya.',
            link: '/asisten-ai',
            color: 'blue',
        },
        {
            icon: <Map size={28} strokeWidth={1.5} />,
            title: 'Lihat Peta Sebaran',
            desc: 'Pantau peta sebaran hama dan peringatan dini di radius 5-10 km dari lokasi Anda.',
            link: '/koordinasi',
            color: 'teal',
        },
    ]

    return (
        <div className="dashboard animate-fade-in">
            {/* Welcome Banner */}
            <section className="dashboard__welcome">
                <div className="dashboard__welcome-content">
                    <h2 className="dashboard__welcome-title">
                        Selamat Datang di <span className="text-gradient">Cocopra.id</span>
                    </h2>
                    <p className="dashboard__welcome-desc">
                        Platform perlindungan ekosistem kelapa berbasis AI untuk petani, penyuluh, dan Dinas Pertanian Kabupaten Minahasa Utara.
                    </p>
                    <div className="dashboard__welcome-badges">
                        <span className="badge badge--success">Intelligence for Justice</span>
                        <span className="badge badge--warning">Responsible AI</span>
                        <span className="badge badge--success">Offline-First</span>
                    </div>
                </div>
                <div className="dashboard__welcome-art">
                    <Sprout size={160} color="var(--color-primary-700)" strokeWidth={1} />
                </div>
            </section>

            {/* Statistics Cards */}
            <section className="dashboard__stats stagger">
                {quickStats.map((stat, i) => (
                    <div className={`dashboard__stat-card card stat--${stat.color}`} key={i}>
                        <div className="dashboard__stat-icon">{stat.icon}</div>
                        <div className="dashboard__stat-info">
                            <span className="dashboard__stat-value">{stat.value}</span>
                            <span className="dashboard__stat-label">{stat.label}</span>
                        </div>
                    </div>
                ))}
            </section>

            {/* Quick Actions */}
            <section className="dashboard__actions">
                <h3 className="dashboard__section-title">Aksi Cepat</h3>
                <div className="dashboard__actions-grid stagger">
                    {quickActions.map((action, i) => (
                        <a href={action.link} className={`dashboard__action-card card action--${action.color}`} key={i}>
                            <span className="dashboard__action-icon">{action.icon}</span>
                            <h4 className="dashboard__action-title">{action.title}</h4>
                            <p className="dashboard__action-desc">{action.desc}</p>
                            <span className="dashboard__action-arrow">→</span>
                        </a>
                    ))}
                </div>
            </section>

            {/* Info Banner */}
            <section className="dashboard__info card">
                <div className="dashboard__info-icon">
                    <Lightbulb size={28} strokeWidth={2} color="var(--color-info)" />
                </div>
                <div className="dashboard__info-content">
                    <h4>Citizen Science as Data Engine</h4>
                    <p>Setiap laporan hama dan input harga dari Anda menjadi data berharga yang memperkuat model AI kami. Anda bukan hanya pengguna — Anda adalah kontributor aktif.</p>
                </div>
            </section>
        </div>
    )
}

export default Dashboard
