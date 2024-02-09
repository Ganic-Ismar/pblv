import React, { useContext, useEffect } from "react";
import { PlanContext } from "../context/planProvider";
import { Table, Button, Container } from "react-bootstrap";

const DisplayPlan = () => {
  const { data, updateData } = useContext(PlanContext);

  useEffect(() => {
    updateData();
  }, []);

  return (
    <div>
      <h1>Display Plan</h1>

      <Button onClick={() => updateData()}>Update Data</Button>

      <Container className="mt-3">

        <Table striped bordered>
          <thead>
            <tr>
              <th>ID</th>
              <th>Fahrzeug</th>
              <th>Ankunft Tag</th>
              <th>Ankunft Uhrzeit</th>
              <th>Abfahrt Tag</th>
              <th>Abfahrt Uhrzeit</th>
              <th>Notwendige Ladung</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                <td>{item.id}</td>
                <td>{item.car_id}</td>
                <td>{item.arrival_date}</td>
                <td>{item.arrival_time}</td>
                <td>{item.departure_date}</td>
                <td>{item.departure_time}</td>
                <td>{item.required_charge}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    </div>
  );
};

export default DisplayPlan;