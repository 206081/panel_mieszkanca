import {Link} from "react-router-dom";

const Home = () => {
    return (
        <div>
            <h1>Welcome on the Panel Mieszkańca!</h1>
            <p>
                Already have an account?<br/>
                <span className="line">
                    <Link to="/login">Sign In</Link>
                </span>
            </p>
        </div>
    )
}

export default Home
