import Register from './components/Register';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Layout from './components/Layout';
import Home from './components/Home';
import Administration from './components/Administration';
import Missing from './components/Missing';
import Unauthorized from './components/Unauthorized';
import RequireAuth from './components/RequireAuth';
import {Routes, Route} from 'react-router-dom';
import Users from "./components/Users";
import {AuthProvider} from "./context/AuthProvider";
import Password from "./components/Password";

const ROLES = {
    "admin": "admin",
    "stuff": "stuff",
    "user": "user",
}

function App() {

    return (
        <AuthProvider>
            <Routes>
                <Route path="/" element={<Layout/>}>
                    <Route index element={<Home/>}/>

                    {/* public routes */}
                    <Route path="login" element={<Login/>}/>
                    <Route path="unauthorized" element={<Unauthorized/>}/>
                    <Route path="password_reset" element={<Password/>}/>

                    {/* we want to protect these routes */}
                    <Route element={<RequireAuth allowedRoles={[ROLES.user, ROLES.admin]}/>}>
                        <Route path="dashboard" element={<Dashboard/>}/>
                    </Route>

                    <Route element={<RequireAuth allowedRoles={[ROLES.admin]}/>}>
                        <Route path="administration" element={<Administration/>}/>
                        <Route path="users" element={<Users/>}/>
                        <Route path="register" element={<Register/>}/>
                    </Route>

                    {/* catch all */}
                    <Route path="*" element={<Missing/>}/>
                </Route>
            </Routes>
        </AuthProvider>
    );
}

export default App;
