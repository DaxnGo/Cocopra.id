import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { WifiOff } from 'lucide-react'
import { AuthProvider, useAuth } from './context/AuthContext'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import PestScanner from './pages/PestScanner'
import InfoHarga from './pages/InfoHarga'
import AsistenAI from './pages/AsistenAI'
import Koordinasi from './pages/Koordinasi'
import Login from './pages/Login'
import RegulatoryCheck from './pages/RegulatoryCheck'
import './App.css'

// Komponen Pelindung Rute
const ProtectedRoute = ({ children, allowedRoles }) => {
    const { isAuthenticated, user, loading } = useAuth();

    if (loading) {
        return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'var(--color-primary-600)' }}>Memuat Sesi...</div>;
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    if (allowedRoles && !allowedRoles.includes(user.role)) {
        return <Navigate to="/" replace />; // Role tidak diizinkan, kembalikan ke Home
    }

    return children;
};

// Komponen Layout Utama (Hanya terlihat jika login)
const AppLayout = () => {
    const [isOnline, setIsOnline] = useState(navigator.onLine)

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

    return (
        <div className="app-layout">
            {/* Global Offline Banner */}
            {!isOnline && (
                <div className="offline-banner">
                    <WifiOff size={18} />
                    <span>Anda sedang Offline. Fitur input data (Harga & Hama) tetap akan disimpan.</span>
                </div>
            )}

            <Sidebar />
            <div className="app-main">
                <Header />
                <main className="app-content">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/pest-scanner" element={<ProtectedRoute allowedRoles={['petani']}><PestScanner /></ProtectedRoute>} />
                        <Route path="/info-harga" element={<ProtectedRoute allowedRoles={['petani']}><InfoHarga /></ProtectedRoute>} />
                        <Route path="/asisten-ai" element={<ProtectedRoute allowedRoles={['petani']}><AsistenAI /></ProtectedRoute>} />
                        <Route path="/regulatory" element={<ProtectedRoute allowedRoles={['petani', 'dinas']}><RegulatoryCheck /></ProtectedRoute>} />
                        <Route path="/koordinasi" element={<ProtectedRoute allowedRoles={['dinas']}><Koordinasi /></ProtectedRoute>} />
                    </Routes>
                </main>
            </div>
        </div>
    )
}

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/*" element={
                        <ProtectedRoute>
                            <AppLayout />
                        </ProtectedRoute>
                    } />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    )
}

export default App
