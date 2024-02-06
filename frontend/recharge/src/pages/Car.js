import React from "react";
import { render } from "react-dom";
import DisplayCars from "../components/DisplayCars";
import AddCar from "../components/addCar";

import CarProvider from "../context/carProvider";

const Car = () => (
    <div>
        <AddCar />
        <CarProvider>
            <DisplayCars />
        </CarProvider>
    </div>
);

export default Car;