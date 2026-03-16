import { NavLink, useLocation } from 'react-router-dom'
import { LayoutDashboard, ScanSearch, LineChart, Bot, Map, Sprout, ShieldCheck } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import './Sidebar.css'

const navItems = [
    { path: '/', icon: <LayoutDashboard size={22} strokeWidth={1.5} />, label: 'Dashboard', desc: 'Ringkasan' },
    { path: '/pest-scanner', icon: <ScanSearch size={22} strokeWidth={1.5} />, label: 'Pest Scanner', desc: 'Deteksi Hama' },
    { path: '/info-harga', icon: <LineChart size={22} strokeWidth={1.5} />, label: 'Info Harga', desc: 'Harga Kopra' },
    { path: '/asisten-ai', icon: <Bot size={22} strokeWidth={1.5} />, label: 'Asisten AI', desc: 'Konsultasi' },
    { path: '/regulatory', icon: <ShieldCheck size={22} strokeWidth={1.5} />, label: 'Regulatory', desc: 'Cek Pestisida' },
    { path: '/koordinasi', icon: <Map size={22} strokeWidth={1.5} />, label: 'Koordinasi', desc: 'Peta & Alert' },
]

function Sidebar() {
    const location = useLocation()
    const { user } = useAuth()

    // Filter items based on role
    const filteredNavItems = navItems.filter(item => {
        if (!user) return false; // Prevent errors during loading
        if (item.path === '/koordinasi' && user.role !== 'dinas') return false;
        if ((item.path === '/pest-scanner' || item.path === '/info-harga' || item.path === '/asisten-ai') && user.role !== 'petani') return false;
        return true;
    });

    return (
        <nav className="sidebar" role="navigation" aria-label="Navigasi Utama">
            {/* Logo */}
            <div className="sidebar__logo">
                <span className="sidebar__logo-icon">
                    <Sprout size={28} color="var(--color-primary-400)" strokeWidth={2} />
                </span>
                <div className="sidebar__logo-text">
                    <span className="sidebar__brand">Cocopra<span className="sidebar__brand-dot">.id</span></span>
                    <span className="sidebar__tagline">Agritech Kelapa</span>
                </div>
            </div>

            {/* Navigation Items */}
            <ul className="sidebar__nav">
                {filteredNavItems.map((item) => (
                    <li key={item.path}>
                        <NavLink
                            to={item.path}
                            className={({ isActive }) =>
                                `sidebar__link ${isActive ? 'sidebar__link--active' : ''}`
                            }
                            end={item.path === '/'}
                        >
                            <span className="sidebar__link-icon">{item.icon}</span>
                            <div className="sidebar__link-text">
                                <span className="sidebar__link-label">{item.label}</span>
                                <span className="sidebar__link-desc">{item.desc}</span>
                            </div>
                            {location.pathname === item.path && (
                                <span className="sidebar__active-indicator" />
                            )}
                        </NavLink>
                    </li>
                ))}
            </ul>

            {/* Footer */}
            <div className="sidebar__footer">
                <div className="sidebar__version">
                    <span className="sidebar__version-badge">MVP v1.0</span>
                    <span className="sidebar__version-label">Minahasa Utara</span>
                </div>
            </div>
        </nav>
    )
}

export default Sidebar
