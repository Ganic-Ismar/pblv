import React, { useState } from "react";
import { fetchCharingplanData } from "../utils/dataFetcher";
export const ChargingplanContext = React.createContext([]);

const ChargingplanProvider = props => {
    const [data, setData] = useState(
        [{
          "carId": 0,
          "items": [
            {
              "datetime": "2024-01-01T13:00:00",
              "pvPower": 0.0,
              "gridPower": 0
            }]
        }
    ]);

    const updateData = newData => {
        fetchCharingplanData(newData)
            .then(response => {
                setData(response);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    };

    return (
        <ChargingplanContext.Provider
            value={{
                data,
                updateData: updateData
            }}
        >
            {props.children}
        </ChargingplanContext.Provider>
    );
};

export default ChargingplanProvider;