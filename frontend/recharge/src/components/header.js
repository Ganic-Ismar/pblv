import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
const Header = () => {
    return (
        <Navbar bg="light" expand="lg">
            <Container fluid>
            <Navbar.Brand href="#home">Recharge</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ml-auto">
                    <Nav.Link href="#home">Home</Nav.Link>
                    <Nav.Link href="#addcar">Fahrzeug hinzufügen</Nav.Link>
                    <Nav.Link href="#plan">Ladeplan anpassen</Nav.Link>
                </Nav>
            </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default Header;