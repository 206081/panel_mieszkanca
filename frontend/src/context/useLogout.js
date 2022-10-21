import useAuth from '../hooks/useAuth';
import {useNavigate} from "react-router-dom";
import useAxiosPrivate from "../hooks/useAxiosPrivate";

const LOGOUT_URL = '/api/logout/';

const useLogout = async () => {
    const controller = new AbortController();
    const navigate = useNavigate();
    const {auth} = useAuth();
    const axiosPrivate = useAxiosPrivate();

    await axiosPrivate.post(LOGOUT_URL, JSON.stringify({
            refresh: auth?.refresh_token
        }),
        {
            signal: controller.signal
        }
    );
    // setAuth({});
    navigate('/linkpage');
}

export default useLogout
