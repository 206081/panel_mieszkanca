import axios from '../api/axios';
import useAuth from './useAuth';

const useRefreshToken = () => {
    const { setAuth } = useAuth();

    return async () => {
        const response = await axios.get('/api/refresh', {
            withCredentials: true
        });
        setAuth(prev => {
            console.log(JSON.stringify(prev));
            console.log(response.data.access);
            return {...prev, access: response.data.access}
        });
        return response.data.access;
    };
};

export default useRefreshToken;
