import {useLocation, useNavigate} from "react-router-dom";
import {useContext, useEffect, useState} from "react";
import AuthContext from "../context/AuthProvider";
import useAxiosPrivate from "../hooks/useAxiosPrivate";
import Dropdown from "react-bootstrap/Dropdown"
import DropdownButton from 'react-bootstrap/DropdownButton';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Card from 'react-bootstrap/Card';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

const Dashboard = () => {
    const {setAuth} = useContext(AuthContext);
    const navigate = useNavigate();
    const [wholeData, setWholeData] = useState();
    const [housing, setHousing] = useState(0);
    const [apartment, setApartment] = useState(0);
    const [billsTypes, setBillsTypes] = useState("EmptyType");
    const [billType, setBillType] = useState(1);
    const [billAmount, setBillAmount] = useState(0);
    const [isRead, setIsRead] = useState(false);
    const [iter, setIter] = useState(0);
    const axiosPrivate = useAxiosPrivate();
    const location = useLocation();
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const logout = async () => {
        setAuth({});
        navigate('/');
    }

    const submitBill = async () => {
        const controller = new AbortController();
        try {
            const response = await axiosPrivate.post('/api/apartments/' + wholeData[housing].data[apartment].id + '/bills/', {
                "bill_type": billType, "amount": billAmount, signal: controller.signal
            });
            handleClose();
            console.log(response.data);
            getWhole(new AbortController(), true);
        } catch (err) {
            navigate('/login', {state: {from: location}, replace: true});
        }
        return () => {
            controller.abort();
        }
    }
    const handleHousing = (event) => {
        console.log("Set Housing ", event);
        setHousing(event);
        setIsRead(true);
    };

    const handleApartment = (event) => {
        setApartment(event);
    };

    const DropdownLocal = ({label, options, onChange}) => {
        return (<DropdownButton
            key={label}
            onSelect={onChange}
            title={label}
            menuVariant="dark">
            {options.map((option, i) => <Dropdown.Item key={option.name}
                                                       eventKey={i}>{option.name}</Dropdown.Item>)}
        </DropdownButton>)
    };

    const BillType = ({options, bill_type, price, unit}) => {
        console.log({"BillType": options});
        return (<Card>
            <Card.Header>{bill_type}</Card.Header>
            {options.map((option, i) => <Card.Body>Zużycie {option.amount}{option.unit} Koszt {option.cost}zł
                Okres {option.period} {option.is_paid ? "Opłacone" : "Nieopłacone"}</Card.Body>)}
        </Card>)
    };
    const News = ({options}) => {
        console.log({"BillType": options});
        return (<Card>
            <Card.Header>Aktualności</Card.Header>
            {options.map((option, i) =>
                <Card.Body><Card.Title>{option.title}</Card.Title><Card.Text>{option.text}</Card.Text></Card.Body>)}
        </Card>)
    };
    const getWhole = async (controller, mount) => {
        try {
            const response = await axiosPrivate.get('/api/whole', {
                signal: controller.signal
            });
            mount && setWholeData(response.data);
        } catch (err) {
            navigate('/login', {state: {from: location}, replace: true});
        }
    }
    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();

        if (!wholeData?.length) {
            getWhole(controller, isMounted);
        }

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, [getWhole, iter, wholeData?.length]);

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();
        const updateData = () => {
            isMounted && setBillsTypes(wholeData[housing].data[apartment].bills.map((bill, i) => bill.bill_type).filter((value, index, array) => array.indexOf(value) === index));
            setIsRead(true);
        }

        if (wholeData?.length) {
            updateData();
        }

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, [wholeData, housing, apartment])

    function getBills() {
        return billsTypes.map((_type, i) => <BillType
            options={wholeData[housing].data[apartment].bills.filter(fl => fl.bill_type === _type)}
            bill_type={_type}/>);
    }

    function getNews() {
        return <News options={wholeData[housing].data[apartment].news}/>;
    }

    function getModal() {
        return <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Dodaj rachunek</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group>
                        <Form.Label htmlFor="input_bill_type">Typ rachunku</Form.Label>
                        <Form.Control
                            as="select"
                            value={billType}
                            onChange={e => {
                                console.log("BillType:", e.target.value);
                                setBillType(e.target.value);
                            }}
                        >
                            <option value={1}>Woda</option>
                            <option value={2}>Centralne Ogrzewanie</option>
                            <option value={3}>Prąd</option>
                            <option value={4}>Śmieci</option>
                        </Form.Control>
                        <Form.Label htmlFor="input_bill_amount">Zużycie</Form.Label>
                        <Form.Control type="number"
                                      placeholder="Podaj zużycie"
                                      onChange={e => {
                                          console.log("BillAmount:", e.target.value);
                                          setBillAmount(e.target.value);
                                      }}/>
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>Zamknij</Button>
                <Button variant="primary" onClick={submitBill}>Wyślij</Button>
            </Modal.Footer>
        </Modal>
    }

    function getNavbar() {
        return <Navbar style={{top: 0, position: "sticky"}} bg="primary" variant="dark" fixed="top">
            <Container>
                <Navbar.Brand href="#home">Panel Mieszkańca</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        {wholeData?.length ? (<DropdownLocal key={"housing"}
                                                             label={"Spółdzielnia: " + wholeData[housing].name}
                                                             options={wholeData}
                                                             onChange={handleHousing}/>) : <div/>}
                        {wholeData?.length ? (<DropdownLocal key={"apartment"}
                                                             label={"Mieszkanie: " + wholeData[housing].data[apartment].name}
                                                             options={wholeData[housing].data}
                                                             onChange={handleApartment}/>) : <div/>}
                    </Nav>
                    <Button onClick={handleShow}>Dodaj rachunek</Button>
                    <Button onClick={logout}>Wyloguj</Button>
                    {getModal()}
                </Navbar.Collapse>
            </Container>
        </Navbar>;
    }

    return (<div>
        {getNavbar()}
        {isRead ? getNews() : <div/>}
        {isRead ? getBills() : <div/>}
    </div>)
}

export default Dashboard
