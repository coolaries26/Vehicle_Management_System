import { Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Vehicles from "./pages/Vehicles";
import Drivers from "./pages/Drivers";
import Employees from "./pages/Employees";
import Complaints from "./pages/Complaints";
import Maintenance from "./pages/Maintenance";
import Inspections from "./pages/Inspections";
import JobCards from "./pages/JobCards";
import JobCardParts from "./pages/JobCardParts";
import Parts from "./pages/Parts";
import Checklists from "./pages/Checklists";
import AuditLogs  from "./pages/AuditLogs";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="vehicles" element={<Vehicles />} />
        <Route path="drivers" element={<Drivers />} />
        <Route path="employees" element={<Employees />} />
        <Route path="complaints" element={<Complaints />} />
        <Route path="maintenance" element={<Maintenance />} />
        <Route path="inspections" element={<Inspections />}/>
        <Route path="jobcards" element={<JobCards />}/>
        <Route path="jobcardparts" element={<JobCardParts />}/>
        <Route path="parts" element={<Parts />}/>
        <Route path="checklists" element={<Checklists />}/>
        <Route path="audit-logs" element={<AuditLogs />}/>
      </Route>
    </Routes>
  );
};

export default App;