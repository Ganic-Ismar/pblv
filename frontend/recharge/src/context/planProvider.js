import React, { useState } from "react";
import { fetchPlanData } from "../utils/dataFetcher";
export const PlanContext = React.createContext([]);

const PlanProvider = props => {
    const [data, setData] = useState([
        {
            id: 1,
            fahrzeug: "Car",
            ankunftTag: "Monday",
            ankunftUhrzeit: "10:00 AM",
            abfahrtTag: "Tuesday",
            abfahrtUhrzeit: "12:00 PM",
            notwendigeLadung: 80
        },
        {
            id: 2,
            fahrzeug: "Truck",
            ankunftTag: "Tuesday",
            ankunftUhrzeit: "10:00 AM",
            abfahrtTag: "Wednesday",
            abfahrtUhrzeit: "12:00 PM",
            notwendigeLadung: 80
        },
        {
            id: 3,
            fahrzeug: "Car",
            ankunftTag: "Wednesday",
            ankunftUhrzeit: "10:00 AM",
            abfahrtTag: "Thursday",
            abfahrtUhrzeit: "12:00 PM",
            notwendigeLadung: 80
        }
    ]);

    const updateData = newData => {
        fetchPlanData(newData)
            .then(response => {
                setData(response);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    };

    return (
        <PlanContext.Provider
            value={{
                data,
                updateData: updateData
            }}
        >
            {props.children}
        </PlanContext.Provider>
    );
};

export default PlanProvider;