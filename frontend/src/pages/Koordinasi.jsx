import { useState, useEffect } from 'react'
import { Map, Globe, ShieldAlert, Building2, MapPin, AlertTriangle, Search } from 'lucide-react'
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import './PageStyles.css'

// Safer fix for Leaflet Vite import issues (Use CDN)
import L from 'leaflet'
const safetyIcon = L.icon({
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41]
})
L.Marker.prototype.options.icon = safetyIcon

function Koordinasi() {
    const [alerts, setAlerts] = useState([])
    const [stats, setStats] = useState({ total_desa_terpantau: 0, total_laporan_bulan_ini: 0, peringatan_aktif: 0 })

    useEffect(() => {
        // Fetch alerts for the Map
        fetch('/api/geo/alerts')
            .then(res => res.json())
            .then(data => setAlerts(data.alerts || []))
            .catch(err => console.error("Gagal memuat map alerts", err))

        // Fetch dashboard stats
        fetch('/api/geo/dashboard')
            .then(res => res.json())
            .then(data => setStats(data))
            .catch(err => console.error("Gagal memuat stats", err))
    }, [])

    return (
        <div className="page animate-fade-in">
            <div className="page__hero page__hero--teal">
                <span className="page__hero-icon">
                    <Map size={40} strokeWidth={1.5} color="#00897B" />
                </span>
                <div className="page__hero-content">
                    <h2 className="page__hero-title">Koordinasi & Geo-Alert EWS</h2>
                    <p className="page__hero-desc">
                        Sistem peringatan dini (<strong>Early Warning System</strong>) dan dashboard governance untuk
                        Dinas Pertanian. Pantau sebaran hama dan koordinasi penanganan lintas desa dalam radius <strong>5-10 km</strong>.
                    </p>
                </div>
            </div>

            <div className="page__content-grid">
                {/* Map Area */}
                <div className="card page__feature-card map-card">
                    <div className="page__feature-header">
                        <span className="page__feature-icon">
                            <Globe size={24} strokeWidth={2} color="#00897B" />
                        </span>
                        <h3>Peta Sebaran Hama</h3>
                    </div>
                    <div className="map__container-wrapper" style={{ height: '350px', width: '100%', marginTop: '1rem', borderRadius: '12px', overflow: 'hidden' }}>
                        <MapContainer center={[1.4000, 125.0000]} zoom={11} scrollWheelZoom={true} style={{ height: '100%', width: '100%' }}>
                            <TileLayer
                                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            />
                            {alerts.map(alert => (
                                <Marker key={alert.id} position={[alert.latitude, alert.longitude]}>
                                    <Popup>
                                        <strong>{alert.title} ({alert.desa})</strong><br />
                                        {alert.description}<br />
                                        <em>Status: {alert.severity}</em>
                                    </Popup>
                                    <Circle
                                        center={[alert.latitude, alert.longitude]}
                                        radius={alert.radius_km * 1000}
                                        pathOptions={{
                                            color: alert.severity === 'critical' ? 'red' : 'orange',
                                            fillColor: alert.severity === 'critical' ? 'red' : 'orange',
                                            fillOpacity: 0.2
                                        }}
                                    />
                                </Marker>
                            ))}
                        </MapContainer>
                    </div>
                    <div className="page__feature-badges" style={{ marginTop: '1rem' }}>
                        <span className="badge badge--danger">{alerts.filter(a => a.severity === 'critical').length} Titik Alert Aktif</span>
                        <span className="badge badge--warning">{alerts.filter(a => a.severity === 'warning').length} Titik Dalam Investigasi</span>
                    </div>
                </div>

                {/* Alert Dashboard */}
                <div className="card page__feature-card">
                    <div className="page__feature-header">
                        <span className="page__feature-icon">
                            <ShieldAlert size={24} strokeWidth={2} color="var(--color-danger)" />
                        </span>
                        <h3>Smart Control Dashboard</h3>
                    </div>

                    <div className="alert__list">
                        <div className="alert__item alert__item--critical">
                            <div className="alert__dot"></div>
                            <div className="alert__content">
                                <strong>Desa Kema — Serangan Masif</strong>
                                <span>Pseudococcus terdeteksi, radius 5km</span>
                                <span className="alert__time">Hari ini, 14:30</span>
                            </div>
                        </div>
                        <div className="alert__item alert__item--warning">
                            <div className="alert__dot"></div>
                            <div className="alert__content">
                                <strong>Desa Likupang — Pemantauan</strong>
                                <span>Indikasi awal, perlu verifikasi lapangan</span>
                                <span className="alert__time">Kemarin, 09:15</span>
                            </div>
                        </div>
                        <div className="alert__item alert__item--info">
                            <div className="alert__dot"></div>
                            <div className="alert__content">
                                <strong>Desa Wori — Status Aman</strong>
                                <span>Tidak ada laporan 30 hari terakhir</span>
                                <span className="alert__time">3 hari lalu</span>
                            </div>
                        </div>
                    </div>

                    <div className="governance__stats">
                        <div className="governance__stat">
                            <span className="governance__stat-value">{stats.total_desa_terpantau || 0}</span>
                            <span className="governance__stat-label">Desa Terpantau</span>
                        </div>
                        <div className="governance__stat">
                            <span className="governance__stat-value">{stats.total_laporan_bulan_ini || 0}</span>
                            <span className="governance__stat-label">Laporan Bulan Ini</span>
                        </div>
                        <div className="governance__stat">
                            <span className="governance__stat-value">{stats.peringatan_aktif || 0}</span>
                            <span className="governance__stat-label">Peringatan Aktif</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="card page__info-card">
                <span className="page__info-icon">
                    <Building2 size={28} strokeWidth={2} color="var(--color-warning)" />
                </span>
                <div>
                    <h4>Dashboard Governance — Dinas Pertanian</h4>
                    <p>Data agregat dari seluruh petani membentuk peta heatmap sebaran ancaman hama. Dinas Pertanian dapat menggunakan data ini untuk penentuan target distribusi subsidi dan bantuan teknis secara presisi.</p>
                </div>
            </div>
        </div>
    )
}

export default Koordinasi
