import {Link} from "react-router-dom";
import Users from './Users';

const Administration = () => {
    return (<section>
        <h1>Admins Page</h1>
        <br/>
        <Users/>
        <br/>
        <div className="flexGrow">
        <span>
          <li>
        <Link to="/">Home</Link>
          </li>
          <li>
        <Link to="/dashboard">Dashboard</Link>
          </li>
        </span>
        </div>
    </section>)
}

export default Administration
