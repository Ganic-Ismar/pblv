import React, { useState, useEffect, useContext } from 'react';
import { Modal, Form, Button } from 'react-bootstrap';
import postSchedulePlan from '../services/postSchedulePlan';
import { CarContext } from "../context/carProvider";

const AddSchedulePlan = () => {
    const [show, setShow] = useState(false);
    const [car_id, setCar_id] = useState('1');
    const [arrival_date, setArrival_date] = useState('');
    const [arrival_time, setArrival_time] = useState('');
    const [departure_date, setDeparture_date] = useState('');
    const [departure_time, setDeparture_time] = useState('');
    const [required_charge, setRequired_charge] = useState('');
    const { data, updateData } = useContext(CarContext);


    useEffect(() => {
        updateData();
    }, []);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const validateForm = () => {
        // Check that arrival_date + arrival_time is smaller than departure_date + departure_time
        // Create timestamps from the date and time strings
        const arrivalDateTime = new Date(arrival_date + 'T' + arrival_time);
        const departureDateTime = new Date(departure_date + 'T' + departure_time);

        if(arrivalDateTime >= departureDateTime) {
            alert('Ankunft muss vor Abfahrt sein');
            return false;
        }
        
        return car_id.length > 0 && arrival_date.length > 0 && arrival_time.length > 0 && departure_date.length > 0 && departure_time.length > 0 && required_charge.length > 0 && arrivalDateTime < departureDateTime;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!validateForm()) {
            alert('Bitte füllen Sie alle Felder aus');	
            return;
        }
        // Handle form submission logic here
        //Post schedule plan as object
        const schedulePlan = {
            car_id: car_id,
            arrival_date: arrival_date,
            arrival_time: arrival_time,
            departure_date: departure_date,
            departure_time: departure_time,
            required_charge: required_charge
        };
        try {
            postSchedulePlan(schedulePlan);
            // Clear form fields
            setCar_id('');
            setArrival_date('');
            setArrival_time('');
            setDeparture_date('');
            setDeparture_time('');
            setRequired_charge('');
            handleClose();
        } catch (error) {
            alert('Fehler beim Hinzufügen des Plans');
            console.error('Error posting schedule plan:', error);
            // Handle error logic here
        }
    };

    const handleSelectChange = (e) => {
        console.log('Selected car:', e.target.value)
        setCar_id(e.target.value);
    };
    return (
        <div>
            <Button variant="primary" onClick={handleShow}>
                Plan hinzufügen
            </Button>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Plan hinzufügen</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="car_id">
                            <Form.Label>Fahrzeug</Form.Label>
                            <Form.Control as="select" value={car_id} onChange={handleSelectChange}>
                                {data.map((car) => (
                                    <option key={car.id} value={car.id}>{car.modell}</option>
                                ))}
                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId="arrival_date">
                            <Form.Label>Ankunft Tag</Form.Label>
                            <Form.Control type="date" value={arrival_date} onChange={(e) => setArrival_date(e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId="arrival_time">
                            <Form.Label>Ankunft Uhrzeit</Form.Label>
                            <Form.Control type="time" value={arrival_time} onChange={(e) => setArrival_time(e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId="departure_date">
                            <Form.Label>Abfahrt Tag</Form.Label>
                            <Form.Control type="date" value={departure_date} onChange={(e) => setDeparture_date(e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId="departure_time">
                            <Form.Label>Abfahrt Uhrzeit</Form.Label>
                            <Form.Control type="time" value={departure_time} onChange={(e) => setDeparture_time(e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId="required_charge">
                            <Form.Label>Notwendige Ladung</Form.Label>
                            <Form.Control type="number" value={required_charge} onChange={(e) => setRequired_charge(e.target.value)} />
                        </Form.Group>
                        <Button variant="primary" type="submit">
                            Plan hinzufügen
                        </Button>
                    </Form>
                </Modal.Body>
            </Modal>
        </div>
    );
}

export default AddSchedulePlan;