import {Link} from "react-router-dom";

const Home = () => {
    return (
        <div>
            <p>Welcome on the Panel Mieszkańca!</p>
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
