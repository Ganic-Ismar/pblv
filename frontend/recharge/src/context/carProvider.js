import React, { useState } from "react";
import { fetchCarData } from "../utils/dataFetcher";
export const CarContext = React.createContext([]);

const CarProvider = props => {
    const [data, setData] = useState([
        {
            id: 1,
            modell: "Toyota",
            antrieb: "Vollelektrisch",
            kapatizaet: 2022,
            verbrauch: "Silver",
            ladeleistung: 25000
        },
        {
            id: 2,
            modell: "Honda",
            antrieb: "Vollelektrisch",
            kapatizaet: 2021,
            verbrauch: "Blue",
            ladeleistung: 22000
        },
        {
            id: 3,
            modell: "Ford",
            antrieb: "Vollelektrisch",
            kapatizaet: 2023,
            verbrauch: "Red",
            ladeleistung: 35000
        }
    ]);

    const updateData = newData => {
        fetchCarData(newData)
            .then(response => {
                setData(response);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    };

    return (
        <CarContext.Provider
            value={{
                data,
                updateData: updateData
            }}
        >
            {props.children}
        </CarContext.Provider>
    );
};

export default CarProvider;
