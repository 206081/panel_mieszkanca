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
import {ListGroup} from "react-bootstrap";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck, faInfoCircle, faTimes} from "@fortawesome/free-solid-svg-icons";

const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,24}$/;

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
    const [userData, setUserData] = useState({});
    const [password, setPwd] = useState();
    const [validPwd, setValidPwd] = useState(false);
    const [pwdFocus, setPwdFocus] = useState(false);
    const [matchPwd, setMatchPwd] = useState('');
    const [validMatch, setValidMatch] = useState(false);
    const [matchFocus, setMatchFocus] = useState(false);

    const [billAmount, setBillAmount] = useState(0);
    const [billTypes, setBillTypes] = useState("EmptyType");
    const [billType, setBillType] = useState(1);

    const [issueText, setIssueText] = useState(1);
    const [issueType, setIssueType] = useState(1);

    const [billShow, setBillShow] = useState(false);
    const [issueShow, setIssueShow] = useState(false);
    const [userShow, setUserShow] = useState(false);

    const handleCloseBill = () => setBillShow(false);
    const handleShowBill = () => setBillShow(true);
    const handleCloseIssue = () => setIssueShow(false);
    const handleShowIssue = () => setIssueShow(true);
    const handleCloseUser = () => setUserShow(false);
    const handleShowUser = () => setUserShow(true);

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
                    {/*<Button onClick={handleShowBill}>Dodaj rachunek</Button>*/}
                    <Button onClick={handleShowIssue}>Dodaj usterkę</Button>
                    <Button onClick={handleShowUser}>Panel użytkownika</Button>
                    <Button onClick={handleShowUser}>Raporty</Button>
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

    const getWhole = async () => {
        try {
            let endpoints = ['/api/whole', '/api/issues', 'api/users/profile']
            Promise.all(endpoints.map((endpoint) => axiosPrivate.get(endpoint))).then(([{data: whole}, {data: issues}, {data: user}]) => {
                setIssuesData(issues);
                setUserData(user);
                setWholeData(whole);
                console.log("Issues", issues);
                console.log("User", user);
                console.log("Whole", whole);
            });
        } catch (err) {
            console.log("Whole IN", err);
            navigate('/login', {state: {from: location}, replace: true});
        }
    }

    useEffect(() => {

        if (!wholeData?.length) {
            getWhole();
        }

        return () => {
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
    }, [wholeData, housing, apartment, issuesData])

    function getApartmentInfo() {
        const apart = wholeData[housing].data[apartment]
        let variant = apart.balance >= 0 ? "success" : "danger"
        let header = apart.balance >= 0 ? "Dane mieszkania" : "Dane mieszkania, proszę uiścić należność"
        let owners;
        console.log("Length", apart.owners.length);
        if (apart.owners.length > 1) {
            owners = ["Właściciele: ", apart.owners.join(", ")].join("")
        } else {
            owners = ["Właściciel: ", apart.owners.join(", ")].join("")
        }
        console.log("Variant", variant);
        console.log("Apartment", apart);
        return (<Card bg={variant}
                      text="white">
            <Card.Header>{header}</Card.Header>
            <Card.Body key={"Info" + apart.name}>
                <Card.Title key={"Name" + apart.name}>Adres: {apart.name}</Card.Title>
                <Card.Text key={"ApartmentArea"}>
                    Powierzchnia mieszkania: {apart.area} m²<br/>
                    Saldo: {apart.balance} zł<br/>
                    Odsetki: {apart.interest} zł<br/>
                    Liczba osób zamieszkujących mieszkanie: {apart.occupant}<br/>
                    {owners}
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
            console.log("SubmitBillResponse", response.data);
            getWhole(new AbortController(), true);
        } catch (err) {
            navigate('/login', {state: {from: location}, replace: true});
        }
        return () => {
            controller.abort();
        }
    }

    const BillType = ({options, bill_type}) => {
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

    function getRents() {
        let rents = wholeData[housing].data[apartment].rent;
        let amount = 0;
        amount += rents.map(x => x.cost).reduce((amount, a) => amount + a, 0);
        console.log("Rent", rents);

        return (<Card>
            <Card.Header>Aktualne opłaty za lokal</Card.Header>
            <Card.Body>
                {rents.map(option =>
                    <Card.Text key={"bill" + option.id}>
                        {option.bill_type.padStart(20, ' ')} - {option.amount}{option.unit} Koszt {option.cost}zł
                    </Card.Text>)}

                <Card.Text>Całość: {Math.round(amount * 100) / 100}zł</Card.Text>
            </Card.Body>
        </Card>)
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
                                console.log("SetBillType:", e.target.value);
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
                                          console.log("SetBillAmount:", e.target.value);
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

    // User
    useEffect(() => {
        setValidPwd(PWD_REGEX.test(password));
        setValidMatch(password === matchPwd);
    }, [password, matchPwd])

    const submitPwd = async () => {
        const controller = new AbortController();
        try {
            const response = await axiosPrivate.post('/api/users/password_change/', {
                "password": password, signal: controller.signal
            });
            handleCloseBill();
            console.log("submitPwdResponse", response.data);
            getWhole(new AbortController(), true);
        } catch (err) {
            navigate('/login', {state: {from: location}, replace: true});
        }
        return () => {
            controller.abort();
        }
    }

    function userPanel() {
        return <Modal show={userShow} onHide={handleCloseUser}>
            <Modal.Header closeButton>
                <Modal.Title>Panel Użytkownika</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group>
                        <Form.Label htmlFor="user_panel">Dane użytkownika</Form.Label>
                        <Card style={{width: '18rem'}}>
                            <ListGroup variant="flush">
                                <ListGroup.Item>Email: {userData.email}</ListGroup.Item>
                                <ListGroup.Item>Imie i nazwisko: {userData.full_name}</ListGroup.Item>
                                <ListGroup.Item>Data rejestracji: {userData.registered_at}</ListGroup.Item>
                            </ListGroup>
                        </Card>
                        <Form.Label htmlFor="input_issue_description">Zmiana hasła</Form.Label>
                        <br/>
                        <label htmlFor="password">
                            Wprowadź hasło:
                            <FontAwesomeIcon icon={faCheck} className={validPwd ? "valid" : "hide"}/>
                            <FontAwesomeIcon icon={faTimes} className={validPwd || !password ? "hide" : "invalid"}/>
                        </label>
                        <br/>
                        <input
                            type="password"
                            id="password"
                            onChange={(e) => setPwd(e.target.value)}
                            value={password}
                            required
                            aria-invalid={validPwd ? "false" : "true"}
                            aria-describedby="pwdnote"
                            onFocus={() => setPwdFocus(true)}
                            onBlur={() => setPwdFocus(false)}
                        />
                        <p id="pwdnote" className={pwdFocus && !validPwd ? "instructions" : "offscreen"}>
                            <FontAwesomeIcon icon={faInfoCircle}/>
                            8 do 24 znaków.<br/>
                            Hasło musi zawierać małe i wielkie litery, cyfrę oraz znak specjalny.<br/>
                            Dozwolone znaki specjalne: <span aria-label="exclamation mark">!</span> <span
                            aria-label="at symbol">@</span> <span aria-label="hashtag">#</span> <span
                            aria-label="dollar sign">$</span> <span aria-label="percent">%</span>
                        </p>
                        <br/>
                        <label htmlFor="confirm_pwd">
                            Potwierdź hasło:
                            <FontAwesomeIcon icon={faCheck} className={validMatch && matchPwd ? "valid" : "hide"}/>
                            <FontAwesomeIcon icon={faTimes} className={validMatch || !matchPwd ? "hide" : "invalid"}/>
                        </label>
                        <br/>
                        <input
                            type="password"
                            id="confirm_pwd"
                            onChange={(e) => setMatchPwd(e.target.value)}
                            value={matchPwd}
                            required
                            aria-invalid={validMatch ? "false" : "true"}
                            aria-describedby="confirmnote"
                            onFocus={() => setMatchFocus(true)}
                            onBlur={() => setMatchFocus(false)}
                        />
                        <p id="confirmnote" className={matchFocus && !validMatch ? "instructions" : "offscreen"}>
                            <FontAwesomeIcon icon={faInfoCircle}/>
                            Hasła w obu polach nie są zgodne.
                        </p>

                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseUser}>Zamknij</Button>
                <Button disabled={!validPwd || !validMatch ? true : false} variant="primary" onClick={submitPwd}>Zmień
                    hasło</Button>
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
            console.log("SubmitIssueResponse", response.data);
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
                                console.log("SetIssueType:", e.target.value);
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
                                          console.log("SetIssueText:", e.target.value);
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

    const Issues = ({options}) => {
        console.log("Issues", options);
        console.log("issuesData", issuesData);
        return (<Card>
            <Card.Header>Issues</Card.Header>
            {options.map((option, i) => <Card.Body key={option.type + i}>
                <Card.Text key={option.type}>Typ uster:{option.type}</Card.Text>
                <Card.Text key={option.description}>Opis usterki: {option.description}</Card.Text>
                <Card.Text key={option.status}>Status: {option.status}</Card.Text>
            </Card.Body>)}
        </Card>)
    };

    function getIssues() {
        return <Issues options={issuesData}/>;
    }


    return (<div>
        {getNavbar()}
        {isRead ? getApartmentInfo() : <div/>}
        {isRead ? getIssues() : <div/>}
        {isRead ? getNews() : <div/>}
        {/*{isRead ? getBills() : <div/>}*/}
        {isRead ? getRents() : <div/>}
        {isRead ? userPanel() : <div/>}
    </div>)
}

export default Dashboard
