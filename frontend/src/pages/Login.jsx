import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sprout, Map, LogIn } from 'lucide-react';
import '../App.css'; // Menerapkan CSS yang sudah ada

function Login() {
    const { login } = useAuth();
    const navigate = useNavigate();

    const [role, setRole] = useState('petani'); // 'petani' or 'dinas'
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMsg, setErrorMsg] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrorMsg(null);
        setIsLoading(true);

        const result = await login(username, password);

        setIsLoading(false);

        if (result.success) {
            navigate('/'); // Arahkan ke Dashboard
        } else {
            setErrorMsg(result.message);
        }
    };

    // Auto-fill untuk demonstrasi kemudahan testing
    const setDemoCredentials = (selectedRole) => {
        setRole(selectedRole);
        if (selectedRole === 'petani') {
            setUsername('petani1');
            setPassword('password123');
        } else {
            setUsername('dinas_minut');
            setPassword('admin123');
        }
    };

    return (
        <div className="page" style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'linear-gradient(145deg, var(--color-surface) 0%, var(--color-background) 100%)'
        }}>
            <div className="card" style={{ maxWidth: '400px', width: '100%', padding: '2rem' }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <div style={{ fontSize: '3rem', animation: 'float 3s ease-in-out infinite' }}>🌴</div>
                    <h1 style={{ color: 'var(--color-primary-600)', marginTop: '0.5rem', fontSize: '1.8rem' }}>Cocopra.id</h1>
                    <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>Smart Agritech Minahasa Utara</p>
                </div>

                {errorMsg && (
                    <div className="form__feedback form__feedback--error" style={{ marginBottom: '1.5rem' }}>
                        ❌ {errorMsg}
                    </div>
                )}

                <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
                    <button
                        type="button"
                        className={`btn-${role === 'petani' ? 'primary' : 'outline'}`}
                        style={{ flex: 1, padding: '0.5rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}
                        onClick={() => setDemoCredentials('petani')}
                    >
                        <Sprout size={16} /> Petani
                    </button>
                    <button
                        type="button"
                        className={`btn-${role === 'dinas' ? 'primary' : 'outline'}`}
                        style={{ flex: 1, padding: '0.5rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}
                        onClick={() => setDemoCredentials('dinas')}
                    >
                        <Map size={16} /> Dinas
                    </button>
                </div>

                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div className="form__group">
                        <label className="form__label">Username</label>
                        <input
                            type="text"
                            className="form__input"
                            placeholder="Masukkan username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>

                    <div className="form__group">
                        <label className="form__label">Password</label>
                        <input
                            type="password"
                            className="form__input"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn-primary"
                        style={{ marginTop: '1rem', width: '100%', display: 'flex', justifyContent: 'center', gap: '0.5rem' }}
                        disabled={isLoading}
                    >
                        {isLoading ? 'Sedang Masuk...' : <><LogIn size={18} /> Masuk</>}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                    Pilih tab di atas untuk menggunakan akun demo otomatis.
                </div>
            </div>
        </div>
    );
}

export default Login;
