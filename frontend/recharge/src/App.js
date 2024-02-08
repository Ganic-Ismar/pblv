import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';
import Home from './pages/Home';
import Plan from './pages/Plan';
import Car from './pages/Car';


function App() {
  return (
    <Router>
      <div>
        <Navbar bg="light" expand="lg">
          <Navbar.Brand href="/">SmartCharge</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="/plan">Plan</Nav.Link>
              <Nav.Link href="/cars">Cars</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <Container className='p-3'>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/plan" element={<Plan />} />
            <Route path="/cars" element={<Car />} />
          </Routes>
        </Container>
      </div>
    </Router>
  );
}

export default App;
