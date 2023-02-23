import {useRef, useState, useEffect} from 'react';
import useAuth from '../hooks/useAuth';
import {useNavigate, useLocation} from 'react-router-dom';
import jwt from 'jwt-decode' // import dependency

import axios from '../api/axios';

const LOGIN_URL = '/api/login/';

const Login = () => {
    const {setAuth} = useAuth();

    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname;

    const userRef = useRef();
    const errRef = useRef();

    const [email, setUser] = useState('');
    const [password, setPwd] = useState('');
    const [errMsg, setErrMsg] = useState('');

    useEffect(() => {
        userRef.current.focus();
    }, [])

    useEffect(() => {
        setErrMsg('');
    }, [email, password])

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post(LOGIN_URL,
                JSON.stringify({email, password}),
                {
                    headers: {'Content-Type': 'application/json'},
                    withCredentials: true
                }
            );
            const access = response?.data?.access;
            const refresh_token = response?.data?.refresh;
            const roles = jwt(access)?.role;
            setAuth({roles, access, refresh_token});
            localStorage.setItem('roles', roles);
            localStorage.setItem('access', access);
            localStorage.setItem('refresh_token', refresh_token);
            setUser('');
            setPwd('');
            navigate(from || roles.includes("admin") ? "/dashboard" : "/dashboard", {replace: true});
        } catch (err) {
            if (!err?.response) {
                setErrMsg('No Server Response');
            } else if (err.response?.status === 400) {
                setErrMsg('Missing Username or Password');
            } else if (err.response?.status === 401) {
                setErrMsg(err.response?.detail);
            } else {
                setErrMsg('Login Failed');
            }
            errRef.current.focus();
        }
    }

    return (

        <section>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
            <h1>Logowanie</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">Email:</label>
                <input
                    type="text"
                    id="username"
                    ref={userRef}
                    autoComplete="off"
                    onChange={(e) => setUser(e.target.value)}
                    value={email}
                    required
                />

                <label htmlFor="password">Hasło:</label>
                <input
                    type="password"
                    id="password"
                    onChange={(e) => setPwd(e.target.value)}
                    value={password}
                    required
                />
                <button>Zaloguj</button>
            </form>
        </section>

    )
}

export default Login
