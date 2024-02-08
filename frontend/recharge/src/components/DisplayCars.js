import React, { useContext, useEffect } from "react";
import { CarContext } from "../context/carProvider";
import { Table, Button, Container } from "react-bootstrap";

const DisplayCars = () => {
    const { data, updateData } = useContext(CarContext);

    useEffect(() => {
        updateData();
    }, []);

    return (
        <div>
            <h1>Fahrzeuge anzeigen</h1>

            <Button onClick={() => updateData()}>Daten aktualisieren</Button>

            <Container className="mt-3">

                <Table striped bordered>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Modell</th>
                            <th>Antrieb</th>
                            <th>Kapazität</th>
                            <th>Verbrauch</th>
                            <th>Ladeleistung</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map((item, index) => (
                            <tr key={index}>
                                <td>{item.id}</td>
                                <td>{item.modell}</td>
                                <td>{item.antrieb}</td>
                                <td>{item.kapatizaet}</td>
                                <td>{item.verbrauch}</td>
                                <td>{item.ladeleistung}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </Container>
        </div>
    );
}

export default DisplayCars;
