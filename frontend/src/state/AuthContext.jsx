import { createContext, useContext, useState } from 'react';
const AuthContext = createContext(null);
export function AuthProvider({ children }) { const [token, setTokenState] = useState(localStorage.getItem('token')); const setToken = (value) => { value ? localStorage.setItem('token', value) : localStorage.removeItem('token'); setTokenState(value); }; return <AuthContext.Provider value={{ token, setToken, isAuthenticated: Boolean(token) }}>{children}</AuthContext.Provider>; }
export const useAuth = () => useContext(AuthContext);
