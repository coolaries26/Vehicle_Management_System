import { useEffect, useState } from "react";
import { Card, Col, Row, Space, Spin, Typography } from "antd";

import { getVehicles } from "../services/vehicleService";
import { getDrivers } from "../services/driverService";
import { getEmployees } from "../services/employeeService";
import { getComplaints } from "../services/complaintService";
import { getJobCards } from "../services/jobCardService";
import { getInspections } from "../services/inspectionService";
import { DoubleLeftOutlined, TruckFilled } from "@ant-design/icons";

const { Title } = Typography;

const Dashboard = () => {
  const [loading, setLoading] = useState(false);

  const [counts, setCounts] = useState({
    vehicles: 0,
    drivers: 0,
    employees: 0,
    complaints: 0,
    jobCards: 0,
    inspections: 0,
  });

  const loadDashboard = async () => {
    try {
      setLoading(true);

      const [vehicles, drivers, employees, complaints, jobCards, inspections] = await Promise.all([
        getVehicles(),
        getDrivers(),
        getEmployees(),
        getComplaints(),
        getJobCards(),
        getInspections(),
      ]);

      setCounts({
        vehicles: vehicles.length,
        drivers: drivers.length,
        employees: employees.length,
        complaints: complaints.length,
        jobCards: jobCards.length,
        inspections: inspections.length,
      });
    } catch (error) {
      console.error("Dashboard load failed:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return <Spin size="large" />;
  }

  return (
    <>
      <Title level={3}>Dashboard</Title>

      <Row gutter={26}>
        <Col span={6} gutter={16}>
          <Card title="Vehicles" bordered={false}>
            <Title level={2}>{counts.vehicles}</Title>
          </Card>
        </Col>

        <Col span={6} gutter={16}>
          <Card title="Drivers" bordered={false}>
            <Title level={2} alignment="center">
              {counts.drivers}
            </Title>
          </Card>
        </Col>

        <Col span={6} gutter={16}>
          <Card title="Employees" bordered={false}>
            <Title level={2}>{counts.employees}</Title>
          </Card>
        </Col>

        <Col span={6} gutter={16}>
          <Card title="Complaints" bordered={false}>
            <Title level={2}>{counts.complaints}</Title>
          </Card>
        </Col>
      </Row>
      <Space> 

      </Space>
      <Row gutter={26} spacing="justify">

        <Col span={6} gutter={16}>
          <Card title="Job Cards" bordered={false}>
            <Title level={2}>{counts.jobCards}</Title>
          </Card>
        </Col>

        <Col span={6} gutter={16}>
          <Card title="Inspections" bordered={false}>
            <Title level={2}>{counts.inspections}</Title>
          </Card>
        </Col>
      </Row>
    </>
  );
};

export default Dashboard;