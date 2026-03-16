import { useState, useEffect } from 'react';
import { ShieldCheck, Search, Info, CheckCircle2, AlertTriangle, ShieldX } from 'lucide-react';
import './PageStyles.css';

function RegulatoryCheck() {
    const [searchQuery, setSearchQuery] = useState('');
    const [results, setResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isOnline, setIsOnline] = useState(navigator.onLine);

    // Deteksi konektivitas
    useEffect(() => {
        const handleOnline = () => setIsOnline(true);
        const handleOffline = () => setIsOnline(false);
        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);
        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, []);

    // Efek debounce otomatis untuk Live Search
    useEffect(() => {
        if (!searchQuery.trim() || searchQuery.length < 2) {
            setResults([]);
            return;
        }

        const timerId = setTimeout(() => {
            fetchResults(searchQuery);
        }, 400); // 400ms delay agar tidak membanjiri API

        return () => clearTimeout(timerId);
    }, [searchQuery, isOnline]);

    const fetchResults = async (query) => {
        if (!isOnline) {
            setError('Pencarian database regulasi membutuhkan koneksi internet aktif.');
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch(`/api/regulatory/search?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Gagal mengambil data dari server');

            const data = await response.json();
            setResults(data);
        } catch (err) {
            console.error("Regulatory API Error:", err);
            setError('Sistem pencarian sedang mengalami gangguan. Coba lagi nanti.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="page animate-fade-in">
            {/* Hero Section */}
            <div className="page__hero" style={{ background: 'linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-800) 100%)' }}>
                <span className="page__hero-icon" style={{ background: 'rgba(255,255,255,0.15)', color: 'white' }}>
                    <ShieldCheck size={40} strokeWidth={1.5} />
                </span>
                <div className="page__hero-content" style={{ color: 'white' }}>
                    <h2 className="page__hero-title">Katalog Pestisida Resmi</h2>
                    <p className="page__hero-desc" style={{ color: 'rgba(255,255,255,0.85)' }}>
                        Cek legalitas dan keamanan produk pestisida. Terhubung langsung dengan
                        Database Kementerian Pertanian (Kementan) Republik Indonesia.
                    </p>
                </div>
            </div>

            <div className="page__content-grid" style={{ gridTemplateColumns: 'minmax(0, 1fr)' }}>
                {/* Panel Pencarian */}
                <div className="card" style={{ padding: '2rem' }}>
                    <div style={{ position: 'relative', marginBottom: '1.5rem' }}>
                        <div style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--color-primary-600)' }}>
                            <Search size={22} />
                        </div>
                        <input
                            type="text"
                            className="form__input"
                            placeholder="Ketik nama pestisida... (Misal: Roundup, Decis, dll)"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            style={{
                                width: '100%',
                                paddingLeft: '3.5rem',
                                paddingRight: '3.5rem',
                                fontSize: '1.15rem',
                                height: '4rem',
                                borderRadius: '99px',
                                border: '2px solid transparent',
                                boxShadow: '0 8px 24px rgba(0,0,0,0.08)',
                                transition: 'all 0.3s ease',
                                outline: 'none'
                            }}
                            autoComplete="off"
                            onFocus={(e) => e.target.style.borderColor = 'var(--color-primary-400)'}
                            onBlur={(e) => e.target.style.borderColor = 'transparent'}
                        />
                        {isLoading && (
                            <div style={{ position: 'absolute', right: '1.5rem', top: '50%', transform: 'translateY(-50%)' }}>
                                <span style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', fontWeight: 500 }}>Mencari...</span>
                            </div>
                        )}
                    </div>

                    {/* Menampilkan Peringatan Offline / Error */}
                    {error && (
                        <div className="form__feedback form__feedback--error" style={{ marginBottom: '1rem' }}>
                            <AlertTriangle size={18} /> {error}
                        </div>
                    )}

                    {/* Placeholder Jika Kosong */}
                    {!isLoading && results.length === 0 && searchQuery.length > 1 && !error && (
                        <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--color-text-muted)' }}>
                            <ShieldX size={48} style={{ opacity: 0.5, margin: '0 auto 1rem' }} />
                            <h4 style={{ color: 'var(--color-danger)' }}>Produk Tidak Ditemukan</h4>
                            <p style={{ fontSize: '0.9rem', maxWidth: '400px', margin: '0 auto' }}>
                                Pestisida "{searchQuery}" tidak terdaftar di database Kementan.
                                Berhati-hatilah terhadap produk palsu atau ilegal yang dapat merusak lingkungan.
                            </p>
                        </div>
                    )}

                    {!isLoading && results.length === 0 && searchQuery.length <= 1 && !error && (
                        <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--color-text-muted)' }}>
                            <Info size={48} style={{ opacity: 0.5, margin: '0 auto 1rem' }} />
                            <p>Ketik minimal 2 karakter untuk memulai pencarian instan.</p>
                        </div>
                    )}

                    {/* Grid Hasil Pencarian */}
                    {results.length > 0 && (
                        <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
                            {results.map((item) => (
                                <div key={item.id} className="card" style={{ padding: '1.5rem', border: '1px solid var(--color-border)', boxShadow: 'none' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                                        <h3 style={{ fontSize: '1.1rem', color: 'var(--color-text)' }}>{item.nama_pestisida}</h3>
                                        <span className="badge badge--success" style={{ display: 'flex', gap: '0.25rem', alignItems: 'center' }}>
                                            <CheckCircle2 size={14} /> Terdaftar
                                        </span>
                                    </div>

                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.9rem' }}>
                                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                                            <span style={{ color: 'var(--color-text-muted)', width: '85px' }}>Kategori</span>
                                            <span style={{ fontWeight: 500 }}>{item.kategori || 'N/A'}</span>
                                        </div>
                                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                                            <span style={{ color: 'var(--color-text-muted)', width: '85px' }}>Bahan Aktif</span>
                                            <span style={{ color: 'var(--color-primary-700)' }}>{item.bahan_aktif || 'N/A'}</span>
                                        </div>
                                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                                            <span style={{ color: 'var(--color-text-muted)', width: '85px' }}>Produsen</span>
                                            <span>{item.nama_perusahaan || 'N/A'}</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default RegulatoryCheck;
