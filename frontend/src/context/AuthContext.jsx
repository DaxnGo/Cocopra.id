import { createContext, useState, useEffect, useContext } from 'react';

// Create Context
const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Initialize state from local storage on mount
    useEffect(() => {
        const storedUser = localStorage.getItem('cocopra_user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    // Login function
    const login = async (username, password) => {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login gagal.');
            }

            const data = await response.json();

            const userData = {
                token: data.access_token,
                role: data.role,
                nama_lengkap: data.nama_lengkap,
                username: username
            };

            // Save to localStorage for Offline-first mechanism
            localStorage.setItem('cocopra_user', JSON.stringify(userData));
            setUser(userData);

            return { success: true };
        } catch (error) {
            console.error("Login failed:", error);
            return { success: false, message: error.message };
        }
    };

    // Logout function
    const logout = () => {
        localStorage.removeItem('cocopra_user');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
