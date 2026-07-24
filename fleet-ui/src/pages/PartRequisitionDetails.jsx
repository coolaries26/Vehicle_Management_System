import { useEffect, useState } from "react";

import {
  Button,
  Card,
  Descriptions,
  Row,
  Space,
  Spin,
  Table,
  Typography,
  message,
} from "antd";

import {
  useNavigate,
  useParams,
} from "react-router-dom";
import {  getPartRequisitions,} from "../services/partRequisitionService";
import {  getPartRequisitionDetails,} from "../services/partRequisitionDetailService";
import {  getVehicles,} from "../services/vehicleService";
import {  getEmployees,} from "../services/employeeService";
import {  getParts,} from "../services/partService";
import {  API_BASE_URL,} from "../utils/config";

const { Title } =
  Typography;

const PartRequisitionDetails =
  () => {
    const {
      requisitionId,
    } = useParams();
    const navigate =
      useNavigate();
    const [loading,
      setLoading] =
      useState(true);
    const [requisition,
      setRequisition] =
      useState(null);
    const [details,
      setDetails] =
      useState([]);
    const [vehicles,
      setVehicles] =
      useState([]);
    const [employees,
      setEmployees] =
      useState([]);
    const [parts,
      setParts] =
      useState([]);
    const loadData = async () => {
        try {
          setLoading(
            true
          );
          const [
            requisitionData,
            detailData,
            vehicleData,
            employeeData,
            partData,
          ] =
            await Promise.all([
              getPartRequisitions(),
              getPartRequisitionDetails(),
              getVehicles(),
              getEmployees(),
              getParts(),
            ]);
          const current =
            requisitionData.find(
              item =>
                String(
                  item.requisition_id
                ) ===
                String(
                  requisitionId
                )
            );
          setRequisition(
            current
          );
          setDetails(
            detailData.filter(
              item =>
                String(
                  item.requisition_id
                ) ===
                String(
                  requisitionId
                )
            )
          );
          setVehicles(
            vehicleData
          );
          setEmployees(
            employeeData
          );
          setParts(
            partData
          );
        } catch (
          error
        ) {
          console.error(
            error
          );
          message.error(
            "Failed to load requisition"
          );
        } finally {
          setLoading(
            false
          );
        }
      };

    useEffect(() => {  loadData();}, [requisitionId]);
    if (loading) {
      return (
        <div
          style={{
            textAlign:
              "center",
            marginTop:
              100,
          }}
        >
          <Spin
            size="large"
          />
        </div>
      );
    }
    if (
      !requisition
    ) {
      return (
        <Card>
          Requisition
          not found
        </Card>
      );
    }
    const vehicle =
      vehicles.find(
        v =>
          v.vehicle_id ===
          requisition.vehicle_id
      );
    const technician =
      employees.find(
        e =>
          e.employee_id ===
          requisition.technician_id
      );
    const partMap =
      Object.fromEntries(
        parts.map(
          part => [
            part.part_id,
            part.part_name,
          ]
        )
      );
    const columns = [
      {
        title:
          "Part",
        render:
          (
            _,
            record
          ) =>
            partMap[
              record.part_id
            ] ?? "-",
      },
      {
        title:
          "Qty Required",

        dataIndex:
          "quantity_required",
      },
      {
        title:
          "Qty Returned",

        dataIndex:
          "quantity_returned",
      },
      {
        title:
          "Required Serial No",

        dataIndex:
          "required_serial_number",
      },
      {
        title:
          "Returned Serial No",

        dataIndex:
          "returned_serial_number",
      },
      {
        title:
          "Remarks",

        dataIndex:
          "remarks",
      },
    ];
    return (

      <Space
        direction="vertical"
        size="large"
        style={{
          width:
            "100%",
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
                  "/requisitions"
                )
              }
            >
              Back To Requisitions
            </Button>
            <Button
              type="primary"
              onClick={() =>
                window.open(
                  `${API_BASE_URL}/requisitions_print/${requisition.requisition_id}/pdf`,
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
            }}
          >
            Part Requisition
          </Title>
          <Descriptions
            bordered
            column={2}
          >
            <Descriptions.Item
              label="Requisition No"
            >
              {
                requisition.requisition_number
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Status"
            >
              {
                requisition.status
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Vehicle"
            >
              {
                vehicle
                  ?.rc_number
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Job Card"
            >
              {
                requisition.job_card_id
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Technician"
            >
              {
                technician
                  ?.full_name
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Date"
            >
              {
                requisition.requisition_date
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Remarks"
              span={2}
            >
              {
                requisition.remarks
              }
            </Descriptions.Item>
          </Descriptions>
        </Card>
        <Card>
          <Title
            level={4}
          >
            Requested Parts
          </Title>
          <Table
            rowKey={
              "requisition_detail_id"
            }
            columns={
              columns
            }
            dataSource={
              details
            }
            pagination={
              false
            }
          />
        </Card>
      </Space>
    );
  };

export default
  PartRequisitionDetails;