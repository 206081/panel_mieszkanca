import {useLocation, useNavigate} from "react-router-dom";
import {useContext, useEffect, useState} from "react";
import AuthContext from "../context/AuthProvider";
import useAxiosPrivate from "../hooks/useAxiosPrivate";
import Dropdown from "react-bootstrap/Dropdown"
import DropdownButton from 'react-bootstrap/DropdownButton';

const Dashboard = () => {
    const {setAuth} = useContext(AuthContext);
    const navigate = useNavigate();
    const [wholeData, setWholeData] = useState();
    const [housing, setHousing] = useState(0);
    const [apartment, setApartment] = useState(0);
    const axiosPrivate = useAxiosPrivate();
    const location = useLocation();

    const logout = async () => {
        setAuth({});
        navigate('/');
    }

    const handleHousing = (event) => {
        console.log("Set Housing ", event);
        setHousing(event);
    };

    const handleApartment = (event) => {
        setApartment(event.target.value);
    };

    const DropdownLocal = ({label, options, onChange}) => {
        return (
            <DropdownButton
                onSelect={onChange}
                title={label}
                variant="info"
                menuVariant="dark">
                {options.map((option, i) => <Dropdown.Item eventKey={i}>{option.name}</Dropdown.Item>)}
            </DropdownButton>
        )
    };

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();

        const getUsers = async () => {
            try {
                const response = await axiosPrivate.get('/api/whole', {
                    signal: controller.signal
                });
                isMounted && setWholeData(response.data);
            } catch (err) {
                navigate('/login', {state: {from: location}, replace: true});
            }
        }
        getUsers();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, [])

    return (<div className="form">
        <h1>Panel Mieszkańca</h1>
        <div>
            {wholeData?.length ? (
                <DropdownLocal label="Wybierz spółdzielnię:" options={wholeData} onChange={handleHousing}/>) : <div/>}
            {wholeData?.length ? (<p>Spółdzielnia: {wholeData[housing].name}</p>) : <div/>}
            {wholeData?.length ? (
                <DropdownLocal label="Wybierz mieszkanie:" options={wholeData[housing].data} value={apartment}
                          onChange={handleApartment}/>) : <div/>}
            {wholeData?.length ? (<p>Mieszkanie: {wholeData[housing].data[apartment].name}</p>) : <div/>}

        </div>
        <br/>
        {wholeData?.length ? (<ul> Rachunek
            {wholeData[housing].data[apartment].bills.map((bill, bill_key) => <p
                key={bill_key}> {bill.bill_type}
                <br/> Zużycie {bill.amount}{bill.unit} Koszt {bill.cost}zł Cena
                jednostkowa {bill.unit_cost}zł/{bill.unit} Okres {bill.period}</p>)}
        </ul>) : <div>No data to display</div>}
    </div>)
}

export default Dashboard
