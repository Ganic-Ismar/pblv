import React from "react";
import { render } from "react-dom";
import DisplayPlan from "../components/DisplayPlan";

import PlanProvider from "../context/planProvider";
import AddSchedulePlan from "../components/addSchedulePlan";
import CarProvider from "../context/carProvider";

const Plan = () => (
  <div>
    <CarProvider>
      <AddSchedulePlan />
    </CarProvider>
    <PlanProvider>
      <DisplayPlan />
    </PlanProvider>
  </div>
);

export default Plan;