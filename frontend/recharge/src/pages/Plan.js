import React from "react";
import { render } from "react-dom";
import DisplayPlan from "../components/DisplayPlan";

import PlanProvider from "../context/planProvider";

const Plan = () => (
    <PlanProvider>
        <DisplayPlan />
    </PlanProvider>
  );

export default Plan;