import {useNavigate} from "react-router-dom";
import useAxiosPrivate from "./useAxiosPrivate";
import {useContext} from "react";
import AuthContext from "../context/AuthProvider";

const LOGOUT_URL = '/api/logout/';

const useLogout = async () => {
    const {auth} = useContext(AuthContext);
    const controller = new AbortController();
    const navigate = useNavigate();
    const axiosPrivate = useAxiosPrivate();

    await axiosPrivate.post(LOGOUT_URL, JSON.stringify({
            refresh: auth?.refresh_token
        }),
        {
            signal: controller.signal
        }
    );
    auth({});
    navigate('/linkpage');
}

export default useLogout
