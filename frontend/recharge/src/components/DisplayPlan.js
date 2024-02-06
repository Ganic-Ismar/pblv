import React, { useContext } from "react";
import { PlanContext } from "../context/planProvider";
import { Table, Button, Container } from "react-bootstrap";

const DisplayPlan = () => {
  const { data, updateData } = useContext(PlanContext);

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
                <td>{item.fahrzeug}</td>
                <td>{item.ankunftTag}</td>
                <td>{item.ankunftUhrzeit}</td>
                <td>{item.abfahrtTag}</td>
                <td>{item.abfahrtUhrzeit}</td>
                <td>{item.notwendigeLadung}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    </div>
  );
};

export default DisplayPlan;