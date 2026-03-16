import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Bell, User, LogOut } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import './Header.css'

const pageTitles = {
    '/': 'Dashboard',
    '/pest-scanner': 'Pest-Vision Scanner',
    '/info-harga': 'Adil-Harga Ledger',
    '/asisten-ai': 'Asisten AI Pertanian',
    '/koordinasi': 'Koordinasi & Geo-Alert',
}

function Header() {
    const location = useLocation()
    const navigate = useNavigate()
    const { user, logout } = useAuth()
    const [isOnline, setIsOnline] = useState(navigator.onLine)
    const [currentTime, setCurrentTime] = useState(new Date())

    const handleLogout = () => {
        logout();
        navigate('/login');
    }

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

    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 60000)
        return () => clearInterval(timer)
    }, [])

    const pageTitle = pageTitles[location.pathname] || 'Cocopra.id'

    return (
        <header className="header glass" role="banner">
            <div className="header__left">
                <h1 className="header__title">{pageTitle}</h1>
                <span className="header__date">
                    {currentTime.toLocaleDateString('id-ID', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    })}
                </span>
            </div>

            <div className="header__right">
                {/* Online/Offline Status */}
                <div className={`header__status ${isOnline ? 'header__status--online' : 'header__status--offline'}`}>
                    <span className="header__status-dot" />
                    <span className="header__status-text">
                        {isOnline ? 'Online' : 'Offline'}
                    </span>
                </div>

                {/* Notification Bell */}
                <button className="header__bell" aria-label="Notifikasi" id="notification-bell">
                    <Bell size={20} strokeWidth={2} className="header__bell-icon" />
                    <span className="header__bell-badge">3</span>
                </button>

                {/* User Profile & Logout */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div className="header__avatar" id="user-avatar" title={user?.nama_lengkap}>
                        <User size={20} strokeWidth={2} className="header__avatar-icon" />
                        <span style={{ fontSize: '0.85rem', fontWeight: '500', display: 'none' }} className="user-name-desktop">{user?.nama_lengkap}</span>
                    </div>
                    <button
                        onClick={handleLogout}
                        style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--color-error-base)', display: 'flex', alignItems: 'center', gap: '0.4rem', padding: '0.4rem' }}
                        title="Keluar"
                    >
                        <LogOut size={18} />
                        <span style={{ fontSize: '0.85rem', fontWeight: '600' }}>Keluar</span>
                    </button>
                </div>
            </div>
        </header>
    )
}

export default Header
