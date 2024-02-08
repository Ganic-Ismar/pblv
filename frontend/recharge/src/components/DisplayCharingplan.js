import React, { useContext } from "react";
import { ChargingplanContext } from "../context/chargingplanProvider";
import { Table, Button } from "react-bootstrap";

const DisplayChargingplan = () => {
    const { data, updateData } = useContext(ChargingplanContext);

    return (
        <div>
            <h2>Anzeige der Ladeplan-Tabelle</h2>

            <Button onClick={() => updateData()}>Daten aktualisieren</Button>

            <Table striped bordered>
                <thead>
                    <tr>
                        <th>Auto-ID</th>
                        <th>Datum und Uhrzeit</th>
                        <th>PV-Leistung</th>
                        <th>Netzleistung</th>
                    </tr>
                </thead>
                <tbody>
                    {data && data.map((car) => (
                        car.items.map((item) => (
                            <React.Fragment key={item.datetime}>
                                <tr key={car.carId}>
                                    <td>{car.carId}</td>
                                    <td>{item.datetime}</td>
                                    <td>{item.pvPower}</td>
                                    <td>{item.gridPower}</td>
                                </tr>
                            </React.Fragment>
                        ))
                    ))}
                </tbody>
            </Table>
        </div>
    );
}

export default DisplayChargingplan;