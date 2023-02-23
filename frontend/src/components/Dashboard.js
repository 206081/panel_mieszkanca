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
    const location = useLocation();
    const axiosPrivate = useAxiosPrivate();

    const [isRead, setIsRead] = useState(false);

    const [apartment, setApartment] = useState(0);
    const [housing, setHousing] = useState(0);
    const [wholeData, setWholeData] = useState();
    const [issuesData, setIssuesData] = useState();

    const [billAmount, setBillAmount] = useState(0);
    const [billTypes, setBillTypes] = useState("EmptyType");
    const [billType, setBillType] = useState(1);

    const [issueText, setIssueText] = useState(1);
    const [issueType, setIssueType] = useState(1);

    const [billShow, setBillShow] = useState(false);
    const [issueShow, setIssueShow] = useState(false);

    const handleCloseBill = () => setBillShow(false);
    const handleShowBill = () => setBillShow(true);
    const handleCloseIssue = () => setIssueShow(false);
    const handleShowIssue = () => setIssueShow(true);

    const logout = async () => {
        setAuth({});
        navigate('/');
    }

    // Navbar
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
                    <Button onClick={handleShowBill}>Dodaj rachunek</Button>
                    <Button onClick={handleShowIssue}>Dodaj usterkę</Button>
                    <Button onClick={logout}>Wyloguj</Button>
                    {getBillModal()}
                    {getIssueModal()}
                </Navbar.Collapse>
            </Container>
        </Navbar>;
    }


    // Whole data
    const handleHousing = (event) => {
        console.log("Set Housing ", event);
        if (housing !== event) {
            setHousing(event);
            setApartment(0);
        }
        setIsRead(true);

    };

    const handleApartment = (event) => {
        setApartment(event);
    };

    const getWhole = async (controller, mount) => {
        try {
            const response = await axiosPrivate.get('/api/whole', {
                signal: controller.signal
            });
            setWholeData(response.data);
        } catch (err) {
            console.log("Whole IN");
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
    });

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();
        const updateData = () => {
            isMounted && setBillTypes(wholeData[housing].data[apartment].bills.map((bill, i) => bill.bill_type).filter((value, index, array) => array.indexOf(value) === index));
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

    function getApartmentInfo() {
        const apart = wholeData[housing].data[apartment]
        console.log(apart);
        return (<Card>
            <Card.Header>Dane mieszkania</Card.Header>
            <Card.Body key={"Info" + apart.name}>
                <Card.Title key={"Name" + apart.name}>Adres: {apart.name}</Card.Title>
                <Card.Text key={"ApartmentArea"}>
                    Powierzchnia mieszkania: {apart.area} m²<br/>
                    Saldo: {apart.balance} zł<br/>
                    Odsetki: {apart.interest} zł<br/>
                    Ilość osób zamieszkujących mieszkanie: {apart.occupant}<br/>
                    Właściciele: {apart.owners.join(", ")}
                </Card.Text>
            </Card.Body>
        </Card>)
    }

    // News
    const News = ({options}) => {
        return (<Card>
            <Card.Header>Aktualności</Card.Header>
            {options.map((option, i) => <Card.Body key={option.name}>
                <Card.Title key={option.title}>{option.title}</Card.Title>
                <Card.Text key={option.text}>{option.text}</Card.Text>
            </Card.Body>)}
        </Card>)
    };

    function getNews() {
        return <News options={wholeData[housing].data[apartment].news}/>;
    }


    // Bills
    const submitBill = async () => {
        const controller = new AbortController();
        try {
            const response = await axiosPrivate.post('/api/apartments/' + wholeData[housing].data[apartment].id + '/bills/', {
                "bill_type": billType, "amount": billAmount, signal: controller.signal
            });
            handleCloseBill();
            console.log(response.data);
            getWhole(new AbortController(), true);
        } catch (err) {
            navigate('/login', {state: {from: location}, replace: true});
        }
        return () => {
            controller.abort();
        }
    }

    const BillType = ({options, bill_type}) => {
        console.log({"BillType": options});
        return (<Card>
            <Card.Header>{bill_type}</Card.Header>
            {options.map((option, i) => <Card.Body key={option.name}>
                Zużycie {option.amount}{option.unit} Koszt {option.cost}zł
                Okres {option.period} {option.is_paid ? "Opłacone" : "Nieopłacone"}
            </Card.Body>)}
        </Card>)
    };

    function getBills() {
        return billTypes.map((_type, i) => <BillType
            options={wholeData[housing].data[apartment].bills.filter(fl => fl.bill_type === _type)}
            bill_type={_type}/>);
    }

    function getBillModal() {
        return <Modal show={billShow} onHide={handleCloseBill}>
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
                            <option value={1}>Woda zimna</option>
                            <option value={5}>Woda ciepła</option>
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
                <Button variant="secondary" onClick={handleCloseBill}>Zamknij</Button>
                <Button variant="primary" onClick={submitBill}>Wyślij</Button>
            </Modal.Footer>
        </Modal>
    }

    // Issues
    const submitIssue = async () => {
        const controller = new AbortController();
        try {
            const response = await axiosPrivate.post('/api/issues/', {
                "issue_type": issueType, "description": issueText, signal: controller.signal
            });
            handleCloseIssue();
            console.log(response.data);
            getWhole(new AbortController(), true);
        } catch (err) {
            navigate('/login', {state: {from: location}, replace: true});
        }
        return () => {
            controller.abort();
        }
    }

    function getIssueModal() {
        return <Modal show={issueShow} onHide={handleCloseIssue}>
            <Modal.Header closeButton>
                <Modal.Title>Dodaj usterkę</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group>
                        <Form.Label htmlFor="input_issue_type">Typ usterki</Form.Label>
                        <Form.Control
                            as="select"
                            value={issueType}
                            onChange={e => {
                                console.log("IssueType:", e.target.value);
                                setIssueType(e.target.value);
                            }}
                        >
                            <option value={1}>Elektryka</option>
                            <option value={2}>Hydraulika</option>
                            <option value={3}>Czystość</option>
                            <option value={4}>Winda</option>
                            <option value={5}>Plac zabaw</option>
                            <option value={6}>Inny</option>
                        </Form.Control>
                        <Form.Label htmlFor="input_issue_description">Opis</Form.Label>
                        <Form.Control type="text"
                                      placeholder="Podaj opis usterki"
                                      onChange={e => {
                                          console.log("Issue text:", e.target.value);
                                          setIssueText(e.target.value);
                                      }}/>
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseIssue}>Zamknij</Button>
                <Button variant="primary" onClick={submitIssue}>Wyślij</Button>
            </Modal.Footer>
        </Modal>
    }


    return (<div>
        {getNavbar()}
        {isRead ? getApartmentInfo() : <div/>}
        {isRead ? getNews() : <div/>}
        {isRead ? getBills() : <div/>}
    </div>)
}

export default Dashboard
