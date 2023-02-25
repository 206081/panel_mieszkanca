import {createContext, useState} from "react";

const AuthContext = createContext({});

export const AuthProvider = ({children}) => {
    const roles = localStorage.getItem("roles")
    const access = localStorage.getItem("access")
    const refresh_token = localStorage.getItem("refresh_token")
    const [auth, setAuth] = useState({roles, access, refresh_token});

    return (
        <AuthContext.Provider value={{auth, setAuth}}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthContext;
