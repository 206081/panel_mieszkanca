import {useRef, useState, useEffect} from 'react';
import useAuth from '../hooks/useAuth';
import {useNavigate, useLocation} from 'react-router-dom';

import axios from '../api/axios';

const PASSWORD_RESET_URL = '/api/users/password_reset';

const Password = () => {
    const {setAuth} = useAuth();

    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname;

    const userRef = useRef();
    const errRef = useRef();

    const [email, setUser] = useState('');
    const [message, setMessage] = useState('');
    const [errMsg, setErrMsg] = useState('');

    useEffect(() => {
        userRef.current.focus();
    }, [])

    useEffect(() => {
        setErrMsg('');
        setMessage("")
    }, [email])

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post(PASSWORD_RESET_URL,
                JSON.stringify({email}),
                {
                    headers: {'Content-Type': 'application/json'},
                    withCredentials: true
                }
            );
            setMessage(response.data);
            console.log(response.data);
        } catch (err) {
            if (!err?.response) {
                setErrMsg('No Server Response');
            } else if (err.response?.status === 404) {
                setErrMsg('Username not available');
            } else {
                setErrMsg('Failed');
            }
            errRef.current.focus();
        }
    }

    return (
        <section>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
            <p ref={errRef} className={message ? "successmsg" : "offscreen"} aria-live="assertive">{message}</p>
            <h1>Reset hasła</h1>
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
                <button>Przypomnij</button>
            </form>
        </section>

    )
}

export default Password
