import {useLocation, Navigate, Outlet} from "react-router-dom";
import useAuth from "../hooks/useAuth";

const RequireAuth = () => {
    const {auth} = useAuth();
    const location = useLocation();

    console.log("Access", auth?.access);
    return (
        auth?.access ? <Outlet/> : auth?.access ?
            <Navigate to="/unauthorized" state={{from: location}} replace/> :
            <Navigate to="/login" state={{from: location}} replace/>);
}

export default RequireAuth;
