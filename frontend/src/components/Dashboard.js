import useLogout from "../context/useLogout";

const Dashboard = () => {

    return (
        <section>
            <h1>Dashboard</h1>
            <br/>
            <p>You are logged in!</p>
            <br/>
            <div className="flexGrow">
                <button onClick={useLogout}>Sign Out</button>
            </div>
        </section>
    )
}

export default Dashboard
