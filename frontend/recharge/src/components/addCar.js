import { useState } from 'react';
import { Modal, Form, Button } from 'react-bootstrap';

function AddCar() {
    const [show, setShow] = useState(false);
    const [modell, setModell] = useState('');
    const [antrieb, setAntrieb] = useState('');
    const [kapatizaet, setKapatizaet] = useState('');
    const [verbrauch, setVerbrauch] = useState('');
    const [ladeleistung, setLadeleistung] = useState('');

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const validateForm = () => {
        return modell.length > 0 && antrieb.length > 0 && kapatizaet.length > 0 && verbrauch.length > 0 && ladeleistung.length > 0;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!validateForm()) {
            alert('Please fill out all fields');
            return;
        }
        // Handle form submission logic here
        console.log('Submitted:', modell, antrieb, kapatizaet, verbrauch, ladeleistung);
        // Clear form fields
        setModell('');
        handleClose();
    };

    return (
        <div>
            <Button variant="primary" onClick={handleShow}>
                Add Car
            </Button>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Add Car</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="modell">
                            <Form.Label>Modell</Form.Label>
                            <Form.Control type="text" value={modell} onChange={(e) => setModell(e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId="antrieb">
                            <Form.Label>Antrieb</Form.Label>
                            <Form.Control type="text" value={antrieb} onChange={(e) => setAntrieb(e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId="kapatizaet">
                            <Form.Label>Kapatizaet</Form.Label>
                            <Form.Control type="text" value={kapatizaet} onChange={(e) => setKapatizaet(e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId="verbrauch">
                            <Form.Label>Verbrauch</Form.Label>
                            <Form.Control type="text" value={verbrauch} onChange={(e) => setVerbrauch(e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId="ladeleistung">
                            <Form.Label>Ladeleistung</Form.Label>
                            <Form.Control type="text" value={ladeleistung} onChange={(e) => setLadeleistung(e.target.value)} />
                        </Form.Group>
                        <Button variant="secondary" onClick={handleClose}>
                            Close
                        </Button>
                        <Button variant="primary" type="submit" className='m-3'>
                            Save Changes
                        </Button>
                    </Form>
                </Modal.Body>
            </Modal>
        </div>
    )
}

export default AddCar;