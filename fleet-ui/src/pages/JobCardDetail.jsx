import dayjs from "dayjs";

import {
  Button,
  Card,
  Col,
  Descriptions,
  Row,
  Space,
  Spin,
  Table,
  Tag,
  Typography,
  message,
} from "antd";

import {  useNavigate,} from "react-router-dom";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getJobCards } from "../services/jobCardService";
import { getVehicles } from "../services/vehicleService";
import { getDrivers } from "../services/driverService";
import { getEmployees } from "../services/employeeService";
import { getJobCardParts } from "../services/jobCardPartService";
import { getParts }  from "../services/partService";
import {  API_BASE_URL,} from "../utils/config";


const { Title } = Typography;

const JobCardDetail = () => {

  const { jobCardId } =
    useParams();

  const [loading,
    setLoading] =
    useState(true);

  const [jobCard,
    setJobCard] =
    useState(null);

  const [vehicles,
    setVehicles] =
    useState([]);

  const [drivers,
    setDrivers] =
    useState([]);

  const [employees,
    setEmployees] =
    useState([]);

  const [parts,
    setParts] =
    useState([]);
  const [partMaster,
    setPartMaster] =
    useState([]);  
  const navigate =
    useNavigate();

  const getStatusColor =
    (status) => {

      switch (status) {      
        case "OPEN":
          return "blue";
        case "IN_PROGRESS":
          return "orange";
        case "WAITING_PARTS":
          return "gold";
        case "COMPLETED":
          return "green";
        case "CANCELLED":
          return "red";
        default:
          return "default";
      }
    };
  const loadData =
    async () => {
      try {
        setLoading(true);
        const [
          jobCards,
          vehiclesData,
          driversData,
          employeesData,
          partsData,
          partMasterData,
        ] = await Promise.all([
          getJobCards(),
          getVehicles(),
          getDrivers(),
          getEmployees(),
          getJobCardParts(),
          getParts(),
        ]);
        const currentJobCard =
          jobCards.find(
            item =>
              String(
                item.job_card_id
              ) ===
              String(
                jobCardId
              )
          );
        setJobCard(
          currentJobCard
        );
        setVehicles(
          vehiclesData
        );
        setDrivers(
          driversData
        );
        setEmployees(
          employeesData
        );
        setPartMaster(
          partMasterData
        );
        setParts(
          partsData.filter(
            part =>
              String(
                part.job_card_id
              ) ===
              String(
                jobCardId
              )
          )
        );
      } catch (error) {

        console.error(error);

        message.error(
          "Failed to load Job Card"
        );

      } finally {

        setLoading(false);
      }
    };

  useEffect(() => {
    loadData();
  }, [jobCardId]);

  if (loading) {

    return (
      <div
        style={{
          textAlign: "center",
          marginTop: 100,
        }}
      >
        <Spin size="large" />
      </div>
    );
  }

  if (!jobCard) {

    return (
      <Card>
        Job Card not found
      </Card>
    );
  }

  const vehicle =
    vehicles.find(
      v =>
        v.vehicle_id ===
        jobCard.vehicle_id
    );

  const driver =
    drivers.find(
      d =>
        d.driver_id ===
        jobCard.driver_id
    );

  const technician1 =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.technician1_id
    );

  const technician2 =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.technician2_id
    );

  const partMap =
    Object.fromEntries(
      partMaster.map(
        (part) => [
          part.part_id,
          part.part_name,
        ]
      )
    );
  const requestedBy =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.requested_by_employee_id
    );

  const verifiedBy =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.verified_by_employee_id
    );

  const approvedBy =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.approved_by_employee_id
    );

  const partColumns = [

{
  title:
    "Part",

  render:
    (_, record) =>
      partMap[
        record.part_id
      ] ?? "-",
},

{
  title:
    "Quantity",

  dataIndex:
    "quantity",
},

{
  title:
    "Unit Price",

  dataIndex:
    "unit_price",
},

{
  title:
    "Total",

  render:
    (_, record) =>
      (
        record.quantity
        *
        record.unit_price
      ).toFixed(2),
},
  ];
const getApprovalTag =
  (employee) => {

    if (employee) {

      return (
        <Tag color="green">
          Approved
        </Tag>
      );
    }

    return (
      <Tag color="orange">
        Pending
      </Tag>
    );
  };
  return (
    <Space
      direction="vertical"
      size="large"
      style={{
        width: "100%",
      }}
    >

      <Card>
<Row
  justify="space-between"
  style={{
    marginBottom: 1,
  }}
>
            <Button
              onClick={() =>
                navigate(
                  "/jobcards"
                )
              }
            >
              Back To Job Cards
            </Button>

<Button
  type="primary"
  onClick={() =>
    window.open(
      `${API_BASE_URL}/jobcards_print/${
        jobCard.job_card_id
      }/pdf`,
      "_blank"
    )
  }
>
  Download PDF
</Button>
</Row>
            <Title
              level={2}
              style={{
                textAlign:
                  "center",
                marginBottom:
                  0,
              }}
            >
              Vehicle Job Card
            </Title>
          
            <div
              style={{
                textAlign:
                  "center",
                color: "#888",
                marginBottom: 20,
              }}
            >
              Job Card #
              {jobCard.job_card_id}
            </div>
        <Descriptions
          bordered
          column={2}
        >

          <Descriptions.Item
            label="Job Card No"
          >
            {
              jobCard.job_card_id
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Vehicle"
          >
            {
              vehicle?.rc_number
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Driver"
          >
            {
              driver?.driver_name
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Status"
          >
            <Tag
              color={
                getStatusColor(
                  jobCard.job_status
                )
              }
            >
              {jobCard.job_status}
            </Tag>
          </Descriptions.Item>

          <Descriptions.Item
            label="Date Time In"
          >
            {jobCard.date_time_in
              ? dayjs(
                  jobCard.date_time_in
                ).format(
                  "DD-MMM-YYYY HH:mm"
                )
              : "-"
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Date Time Out"
          >
            {jobCard.date_time_in
              ? dayjs(
                  jobCard.date_time_out
                ).format(
                  "DD-MMM-YYYY HH:mm"
                )
              : "-"
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Zone / Area"
          >
            {
              jobCard.zone_area
            }
          </Descriptions.Item>
          <Descriptions.Item
            label="Complaint ID"
          >
            {jobCard.complaint_id}
          </Descriptions.Item>
                  
          <Descriptions.Item
            label="Inspection ID"
          >
            {jobCard.inspection_id}
          </Descriptions.Item>
          <Descriptions.Item
            label="Mileage / Hours"
          >
            {
              jobCard.mileage_hours
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Maintenance Type"
            span={2}
          >
            {
              jobCard.maintenance_type
            }
          </Descriptions.Item>

        </Descriptions>

      </Card>

      <Card>

        <Title level={4}>
          Technicians
        </Title>

        <Descriptions
          bordered
          column={2}
        >

          <Descriptions.Item
            label="Technician 1"
          >
            {
              technician1?.full_name
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Technician 2"
          >
            {
              technician2?.full_name
            }
          </Descriptions.Item>

        </Descriptions>

      </Card>

      <Card>

        <Title level={4}>
          Issue Details
        </Title>

        <Descriptions
          bordered
          column={1}
        >

          <Descriptions.Item
            label="Issue Reported"
          >
            {
              jobCard.issue_reported
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Problems Found & Action Taken"
          >
            {
              jobCard.problem_found_action_taken
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Requisition Slip Number"
          >
            {
              jobCard.requisition_slip_number
            }
          </Descriptions.Item>

        </Descriptions>

      </Card>

      <Card>

        <Title level={4}>
          Parts Used
        </Title>
        <Table
          rowKey="id"
          columns={
            partColumns
          }
          dataSource={
            parts
          }
          pagination={false}
        />

      </Card>
<Card>

  <Title level={4}>
    Cost Summary
  </Title>

  <Descriptions bordered>

    <Descriptions.Item
      label="Total Parts Cost"
    >
      ₹
      {
        parts
          .reduce(
            (
              total,
              item
            ) =>
              total +
              (
                (item.quantity || 0)
                *
                (item.unit_price || 0)
              ),
            0
          )
          .toFixed(2)
      }
    </Descriptions.Item>

  </Descriptions>

</Card>
<Card
  style={{
    borderTop:
      "4px solid #52c41a",
  }}
>

  <Title level={4}>
    Approval Information
  </Title>

  <Descriptions
    bordered
    column={3}
  >

    <Descriptions.Item
      label="Requested By"
    >
      <Space>
        {
          requestedBy?.full_name
          || "-"
        }
    
        {
          getApprovalTag(
            requestedBy
          )
        }
      </Space>
    </Descriptions.Item>
      
    <Descriptions.Item
      label="Verified By"
    >
      <Space>
        {
          verifiedBy?.full_name
          || "-"
        }
    
        {
          getApprovalTag(
            verifiedBy
          )
        }
      </Space>
    </Descriptions.Item>
    <Descriptions.Item
      label="Approved By"
    >
      <Space>
        {
          approvedBy?.full_name
          || "-"
        }

        {
          getApprovalTag(
            approvedBy
          )
        }
      </Space>
    </Descriptions.Item>

  </Descriptions>

</Card>
    </Space>
  );
};

export default JobCardDetail;
