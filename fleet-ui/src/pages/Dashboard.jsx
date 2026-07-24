import { useEffect, useState } from "react";

import {
  Card,
  Col,
  Row,
  Space,
  Spin,
  Table,
  Tag,
  Typography,
  Statistic,
} from "antd";
import {
  CarOutlined,
  TeamOutlined,
  UserOutlined,
  ToolOutlined,
} from "@ant-design/icons";
import { TruckFilled } from "@ant-design/icons";

import { getVehicles } from "../services/vehicleService";
import { getDrivers } from "../services/driverService";
import { getEmployees } from "../services/employeeService";
import { getComplaints } from "../services/complaintService";
import { getJobCards } from "../services/jobCardService";
import { getInspections } from "../services/inspectionService";
import { getParts } from "../services/partService";
import { getChecklists } from "../services/checklistService";
import { getAuditLogs } from "../services/auditService";

const { Title } = Typography;

const Dashboard = () => {

  const [loading, setLoading] =
    useState(false);

const [counts, setCounts] =
  useState({
    vehicles: 0,
    activeVehicles: 0,

    drivers: 0,
    activeDrivers: 0,

    employees: 0,
    activeEmployees: 0,

    complaints: 0,
    inspections: 0,

    jobCards: 0,

    checklists: 0,
    checklistsActive: 0,
    checklistsInactive: 0,

    parts: 0,
    activeParts: 0,
    inactiveParts: 0,

    auditEvents: 0,

    auditInsertCount: 0,
    auditUpdateCount: 0,
    auditDeactivateCount: 0,
  });

const getAuditOperation = (
  record
) => {

  if (
    record.operation === "UPDATE"
    &&
    record.old_data?.active_flag === true
    &&
    record.new_data?.active_flag === false
  ) {
    return "DEACTIVATE";
  }

  return record.operation;
};
  const [recentAuditLogs,
    setRecentAuditLogs] =
    useState([]);

  const loadDashboard =
    async () => {

      try {

        setLoading(true);

        const [
          vehicles,
          drivers,
          employees,
          complaints,
          jobCards,
          inspections,
          parts,
          checklists,
          auditLogs,
        ] = await Promise.all([
          getVehicles(),
          getDrivers(),
          getEmployees(),
          getComplaints(),
          getJobCards(),
          getInspections(),
          getParts(),
          getChecklists(),
          getAuditLogs(),
        ]);

        setCounts({

          vehicles:
            vehicles.length,

          activeVehicles:
            vehicles.filter(
              vehicle =>
                vehicle.active_flag
            ).length,
          inactiveVehicles:
            vehicles.filter(
              vehicle =>
                !vehicle.active_flag
            ).length,

          drivers:
            drivers.length,

          activeDrivers:
            drivers.filter(
              driver =>
                driver.active_flag
            ).length,
          inactiveDrivers:
            drivers.filter(
              driver =>
                !driver.active_flag
            ).length,

          employees:
            employees.length,

          activeEmployees:
            employees.filter(
              employee =>
                employee.active_flag
            ).length,
          inactiveEmployees:
            employees.filter(
              employee =>
                !employee.active_flag
            ).length,
          complaints:
            complaints.length,

          inspections:
            inspections.length,

          jobCards:
            jobCards.length,

          parts:
            parts.length,
          activeParts:
            parts.filter(
              part =>
                part.active_flag
            ).length,
          inactiveParts:
            parts.filter(
              part =>
                !part.active_flag
            ).length,

          checklists:
            checklists.length,
          checklistsActive:
            checklists.filter(
              checklist =>
                checklist.active_flag
            ).length,
          checklistsInactive:
            checklists.filter(
              checklist =>
                !checklist.active_flag
            ).length,

          auditEvents:
            auditLogs.length,          
          auditInsertCount:
            auditLogs.filter(
              log =>
                log.operation === "INSERT"
            ).length,
          auditUpdateCount:
            auditLogs.filter(
              log =>
                log.operation === "UPDATE"
                &&
                !(
                log.old_data?.active_flag === true
                &&
                log.new_data?.active_flag === false
                )
            ).length,
          auditDeactivateCount:
            auditLogs.filter(
              item =>
                item.operation === "UPDATE"
                &&
                item.old_data?.active_flag === true
                &&
                item.new_data?.active_flag === false
            ).length,
          }
        );
        setRecentAuditLogs(
          auditLogs.slice(
            0,
            10
          )
        );

      } catch (error) {

        console.error(
          "Dashboard load failed",
          error
        );

      } finally {

        setLoading(false);
      }
    };

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {

    return (
      <div
        style={{
          textAlign: "center",
          marginTop: 60,
        }}
      >
        <Spin size="large" />
      </div>
    );
  }

  const auditColumns = [

    {
      title: "Time",
      dataIndex: "changed_at",
      width: 200,
    },

    {
      title: "Table",
      dataIndex: "table_name",
      width: 200,
    },
    {
      title: "Schema",
      dataIndex: "schema_name",
    },
    {
      title: "Operation",

        render: (_, record) => {
        
          const operation =
            getAuditOperation(record);
        
          const colors = {
            INSERT: "green",
            UPDATE: "blue",
            DELETE: "red",
            DEACTIVATE: "volcano",
          };
        
          return (
            <Tag
              color={
                colors[operation]
              }
            >
              {operation}
            </Tag>
          );
        }
    },
    {
      title: "User",

      render: (_, record) =>
        record.changed_by ??
        "System",
    },

    {
      title: "Record ID",
      dataIndex: "record_id",
    
      render: value => (
        <Tag color="blue">
          {value}
        </Tag>
      ),
    },
  ];

  return (
    <>
      <Card
        style={{
          marginBottom: 20,
        }}
      >
        <Title
          level={2}
          style={{
            marginBottom: 0,
            textAlign: "center",
          }}
        >
          Fleet Management Dashboard
        </Title>
        
        <div
          style={{
            textAlign: "center",
            color: "#888",
          }}
        >
          Maintenance Operations Overview
        </div>
      </Card>
    <Space
        direction="vertical"
        size="large"
        style={{ width: "100%" }}
      >
        {/* Fleet Metrics */}
        <Row gutter={[16, 16]}>
          <Col span={6}>
            <Card
              hoverable
              style={{
                borderTop: "4px solid #1677ff",
                textAlign: "center",
              }}
            >
              <Title
                level={5}
                style={{
                  marginBottom: 0,
                }}
              >
                <CarOutlined />
                {""}
                Vehicles
              </Title>
              
              <Title
                level={1}
                style={{
                  marginTop: 8,
                  marginBottom: 10,
                  color: "#1677ff",
                }}
              >
                {counts.vehicles}
              </Title>
              <Space size={8}>
                <Tag color="green">
                  Active: {counts.activeVehicles}
                </Tag>
                <Tag color="red">
                  Inactive: {counts.inactiveVehicles}
                </Tag>
              </Space>
            </Card>
          </Col>

          <Col span={6}>
            <Card
              hoverable
              style={{
                borderTop: "4px solid #52c41a",
                textAlign: "center",
              }}
            >
              <Title
                level={5}
                style={{
                  marginBottom: 0,
                }}
              >
                <UserOutlined />
                {" "}
                Drivers
              </Title>
              
              <Title
                level={1}
                style={{
                  marginTop: 8,
                  marginBottom: 10,
                  color: "#1677ff",
                }}
              >
                {counts.drivers}
              </Title>
              
              <Space>
                <Tag color="green">
                  Active: {counts.activeDrivers}
                </Tag>
              
                <Tag color="red">
                  Inactive: {counts.inactiveDrivers}
                </Tag>
              </Space>
            </Card>
          </Col>

          <Col span={6}>
            <Card
              hoverable
              style={{
                borderTop: "4px solid #722ed1",
                textAlign: "center",
              }}
            >
              <Title
                level={5}
                style={{
                  marginBottom: 0,
                }}
              >
                <TeamOutlined />
                {" "}
                Employees
              </Title>
              
              <Title
                level={1}
                style={{
                  marginTop: 8,
                  marginBottom: 10,
                  color: "#1677ff",
                }}
              >
                {counts.employees}
              </Title>
              <Space size={8}>
                <Tag color="green">
                  Active: {counts.activeEmployees}
                </Tag>
                <Tag color="red">
                  Inactive: {counts.inactiveEmployees}
                </Tag>
              </Space>
            </Card>
          </Col>

          <Col span={6}>
            <Card
              hoverable
              style={{
                borderTop: "4px solid #fa8c16",
                textAlign: "center",
              }}
            >
              <Title
                level={5}
                style={{
                  marginBottom: 0,
                }}
              >
                <ToolOutlined />
                {" "}
                Parts
              </Title>
              
              <Title
                level={1}
                style={{
                  marginTop: 8,
                  marginBottom: 10,
                  color: "#1677ff",
                }}
              >
                {counts.parts}
              </Title>
              <Space size={8}>
                <Tag color="green">
                  Active: {counts.activeParts}
                </Tag>
                <Tag color="red">
                  Inactive: {counts.inactiveParts}
                </Tag>
              </Space>
            </Card>
          </Col>
        </Row>

        {/* Workflow Metrics */}

        <Row gutter={[16, 16]}>

          <Col span={6}>
            <Card
              hoverable
              style={{
                textAlign: "center",
              }}
            >
              <Title
                level={5}
                style={{
                  marginBottom: 0,
                }}
              >
                Complaints
              </Title>
              
              <Title
                level={1}
                style={{
                  marginTop: 8,
                  marginBottom: 10,
                  color: "#1677ff",
                }}
              >
                {counts.complaints}
              </Title>
            </Card>
          </Col>

          <Col span={6}>
            <Card
              hoverable
              style={{
                textAlign: "center",
              }}
            >
              <Title
                level={5}
                style={{
                  marginBottom: 0,
                }}
              >
                Inspections
              </Title>
              
              <Title
                level={1}
                style={{
                  marginTop: 8,
                  marginBottom: 10,
                  color: "#1677ff",
                }}
              >
                {counts.inspections}
              </Title>
            </Card>
          </Col>

          <Col span={6}>
            <Card
              hoverable
              style={{
                textAlign: "center",
              }}
            >
              <Title
                level={5}
                style={{
                  marginBottom: 0,
                }}
              >
                Jobcards
              </Title>
              
              <Title
                level={1}
                style={{
                  marginTop: 8,
                  marginBottom: 10,
                  color: "#1677ff",
                }}
              >
                {counts.jobCards}
              </Title>
            </Card>
          </Col>

          <Col span={6}>
            <Card
              hoverable
              style={{
                textAlign: "center",
              }}
            >
              <Title
                level={5}
                style={{
                  marginBottom: 0,
                }}
              >
                Checklists
              </Title>
              
              <Title
                level={1}
                style={{
                  marginTop: 8,
                  marginBottom: 10,
                  color: "#1677ff",
                }}
              >
                {counts.checklists}
              </Title>
              <Space size={8}>
                <Tag color="green">
                  Active: {counts.checklistsActive}
                </Tag>
                <Tag color="red">
                  Inactive: {counts.checklistsInactive}
                </Tag>
              </Space>
            </Card>
          </Col>

        </Row>

        {/* Audit Summary */}

        <Row gutter={[2, 2]}>
          <Col span={24}>
            <Card>
              <Title level={4}
                style={{
                marginBottom: 0,
                textAlign: "center",
                backgroundColor:"silver"
              }}
              >
                Audit Activity
              </Title>
              <Title level={4}
                style={{
                marginBottom: 0,
                textAlign: "center",
                backgroundColor:"silver"
              }}
              >
                <Statistic
                  title="Total Audit Events"
                  value={counts.auditEvents}
                />
              </Title>
{/*
              <Row gutter={[2, 2]}>
                          
                <Col span={8}>
                  <Card>
                    <Title level={4}
                              style={{
                          marginBottom: 0,
                          textAlign: "center",
                        }}
                    >
                      <Tag color="green">
                        INSERT
                      </Tag>
                    </Title>
                      
                    <Title level={3}
                              style={{
                          marginBottom: 0,
                          textAlign: "center",
                        }}
                    >
                      {counts.auditInsertCount}
                    </Title>
                  </Card>
                </Col>
                      
                <Col span={8}>
                  <Card>
                    <Title level={4}
                              style={{
                          marginBottom: 0,
                          textAlign: "center",
                        }}
                    >
                      <Tag color="blue">
                        UPDATE
                      </Tag>
                    </Title>
                    <Title level={3}
                              style={{
                          marginBottom: 0,
                          textAlign: "center",
                        }}
                    >
                      {counts.auditUpdateCount}
                    </Title>
                  </Card>
                </Col>
                      
                <Col span={8}>
                  <Card>
                    <Title level={4}
                              style={{
                          marginBottom: 0,
                          textAlign: "center",
                        }}
                    >
                      <Tag color="red">
                        DEACTIVATE
                      </Tag>
                    </Title>
                      
                    <Title level={3}
                              style={{
                          marginBottom: 0,
                          textAlign: "center",
                        }}
                    >
                      {counts.auditDeactivateCount}
                    </Title>
                  </Card>
                </Col>
              </Row>
*/}
              <Row gutter={16}>
              
                <Col span={8}>
                  <Card
                    size="small"
                    style={{
                      textAlign: "center",
                    }}
                  >
                    <Statistic
                      title="Inserts"
                      value={counts.auditInsertCount}
                      valueStyle={{
                        color: "#52c41a",
                        fontWeight: "bold",
                      }}
                    />
                  </Card>
                </Col>
                    
                <Col span={8}>
                  <Card
                    size="small"
                    style={{
                      textAlign: "center",
                    }}
                  >
                    <Statistic
                      title="Updates"
                      value={counts.auditUpdateCount}
                      valueStyle={{
                        color: "#1677ff",
                        fontWeight: "bold",
                      }}
                    />
                  </Card>
                </Col>
                    
                <Col span={8}>
                  <Card
                    size="small"
                    style={{
                      textAlign: "center",
                    }}
                  >
                    <Statistic
                      title="Deactivations"
                      value={counts.auditDeactivateCount}
                      valueStyle={{
                        color: "#ff4d4f",
                        fontWeight: "bold",
                      }}
                    />
                  </Card>
                </Col>
                    
              </Row>
            </Card>
          </Col>

        </Row>

        {/* Recent Activity */}

        <Row>
          <Col span={24}>
            <Card>
              <Title level={4}>
                Recent Activity
              </Title>
              <Table
                rowKey="audit_id"
                columns={auditColumns}
                dataSource={
                  recentAuditLogs
                }
                pagination={false}
                size="small"
              />
            </Card>
          </Col>
        </Row>

      </Space>
    </>
  );
};

export default Dashboard;