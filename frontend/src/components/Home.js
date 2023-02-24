import {Link} from "react-router-dom";

const Home = () => {
    return (
        <div>
            <h1>Witamy w Panelu Mieszkańca!</h1>
            <p>
                <span className="line">
                    <Link to="/login">Zaloguj się</Link>
                </span>
            </p>
            <p>
                <span className="line">
                    <Link to="/password_reset">Nie pamiętasz hasła? Przypomnij je</Link>
                </span>
            </p>
        </div>
    )
}

export default Home
