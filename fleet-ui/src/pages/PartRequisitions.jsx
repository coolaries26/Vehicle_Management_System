import {
  useEffect,
  useState,
} from "react";

import {
  Button,
  Card,
  Form,
  Input,
  Modal,
  Popconfirm,
  Select,
  Space,
  Switch,
  Table,
  Tag,
  Typography,
  message,
} from "antd";

import {
  DeleteOutlined,
  EditOutlined,
} from "@ant-design/icons";

import {
  Link,
} from "react-router-dom";

import SearchToolbar from "../components/SearchToolbar";

import tablePagination from "../utils/tablePagination";

import {
  getPartRequisitions,
  createPartRequisition,
  updatePartRequisition,
  deactivatePartRequisition,
} from "../services/partRequisitionService";

import {
  getVehicles,
} from "../services/vehicleService";

import {
  getJobCards,
} from "../services/jobCardService";

import {
  getEmployees,
} from "../services/employeeService";

const { Title } = Typography;

const PartRequisitions = () => {

  const [loading,
    setLoading] =
    useState(false);

  const [requisitions,
    setRequisitions] =
    useState([]);

  const [vehicles,
    setVehicles] =
    useState([]);

  const [jobCards,
    setJobCards] =
    useState([]);

  const [employees,
    setEmployees] =
    useState([]);

  const [searchText,
    setSearchText] =
    useState("");

  const [statusFilter,
    setStatusFilter] =
    useState("ALL");

  const [modalOpen,
    setModalOpen] =
    useState(false);

  const [editingRecord,
    setEditingRecord] =
    useState(null);

  const [form] =
    Form.useForm();

  const loadData =
    async () => {

      try {

        setLoading(true);

        const [
          requisitionData,
          vehicleData,
          jobCardData,
          employeeData,
        ] = await Promise.all([
          getPartRequisitions(),
          getVehicles(),
          getJobCards(),
          getEmployees(),
        ]);

        setRequisitions(
          requisitionData
        );

        setVehicles(
          vehicleData
        );

        setJobCards(
          jobCardData
        );

        setEmployees(
          employeeData
        );

      } catch (error) {

        console.error(
          error
        );

        message.error(
          "Failed to load requisitions"
        );

      } finally {

        setLoading(false);
      }
    };

  useEffect(() => {

    loadData();

  }, []);

  const openCreateModal =
    () => {

      setEditingRecord(
        null
      );

      form.resetFields();

      form.setFieldsValue({
        active_flag: true,
        status: "OPEN",
      });

      setModalOpen(true);
    };

  const openEditModal =
    (record) => {

      setEditingRecord(
        record
      );

      form.setFieldsValue(
        record
      );

      setModalOpen(true);
    };

  const handleSubmit =
    async () => {

      try {

        const values =
          await form.validateFields();

        if (
          editingRecord
        ) {

          await updatePartRequisition(
            editingRecord.requisition_id,
            values
          );

        } else {

          await createPartRequisition(
            values
          );
        }

        message.success(
          "Requisition saved successfully"
        );

        setModalOpen(false);

        await loadData();

      } catch (error) {

        console.error(
          error
        );

        message.error(
          "Operation failed"
        );
      }
    };

  const handleDeactivate =
    async (
      requisitionId
    ) => {

      try {

        await deactivatePartRequisition(
          requisitionId
        );

        message.success(
          "Requisition deactivated"
        );

        await loadData();

      } catch (error) {

        message.error(
          "Operation failed"
        );
      }
    };

  const vehicleMap =
    Object.fromEntries(
      vehicles.map(
        vehicle => [
          vehicle.vehicle_id,
          vehicle.rc_number,
        ]
      )
    );

  const employeeMap =
    Object.fromEntries(
      employees.map(
        employee => [
          employee.employee_id,
          employee.full_name,
        ]
      )
    );

  const filteredData =
    requisitions.filter(
      item => {

        const matchesSearch =
          item.requisition_number
            ?.toLowerCase()
            .includes(
              searchText.toLowerCase()
            );

        const matchesStatus =
          statusFilter ===
            "ALL" ||
          (
            statusFilter ===
              "ACTIVE" &&
            item.active_flag
          ) ||
          (
            statusFilter ===
              "INACTIVE" &&
            !item.active_flag
          );

        return (
          matchesSearch &&
          matchesStatus
        );
      }
    );

  const columns = [

    {
      title:
        "Req No",

      dataIndex:
        "requisition_number",
    },

    {
      title:
        "Vehicle",

      render:
        (_, record) =>
          vehicleMap[
            record.vehicle_id
          ] ?? "-",
    },

    {
      title:
        "Job Card",

      dataIndex:
        "job_card_id",
    },

    {
      title:
        "Technician",

      render:
        (_, record) =>
          employeeMap[
            record.technician_id
          ] ?? "-",
    },

    {
      title:
        "Status",

      dataIndex:
        "status",

      render:
        status => (
          <Tag color="blue">
            {status}
          </Tag>
        ),
    },

    {
      title:
        "Actions",

      render:
        (_, record) => (

          <Space>

            <Link
              to={`/requisitions/${record.requisition_id}`}
            >
              <Button>
                View
              </Button>
            </Link>

            <Button
              icon={
                <EditOutlined />
              }
              onClick={() =>
                openEditModal(
                  record
                )
              }
            >
              Edit
            </Button>

            <Popconfirm
              title="Deactivate Requisition?"
              onConfirm={() =>
                handleDeactivate(
                  record.requisition_id
                )
              }
            >
              <Button
                danger
                icon={
                  <DeleteOutlined />
                }
              >
                Deactivate
              </Button>
            </Popconfirm>

          </Space>
        ),
    },

  ];

  return (
    <>

      <Title level={3}>
        Part Requisitions
      </Title>

      <SearchToolbar
        searchText={
          searchText
        }
        setSearchText={
          setSearchText
        }
        statusFilter={
          statusFilter
        }
        setStatusFilter={
          setStatusFilter
        }
        onRefresh={
          loadData
        }
        onAdd={
          openCreateModal
        }
        searchPlaceholder="Search Requisition"
        addLabel="Add Requisition"
      />

      <Card>

        <Table
          rowKey="requisition_id"
          loading={loading}
          columns={columns}
          dataSource={
            filteredData
          }
          pagination={
            tablePagination
          }
        />

      </Card>

      <Modal
        title={
          editingRecord
            ? "Edit Requisition"
            : "Add Requisition"
        }
        open={
          modalOpen
        }
        onOk={
          handleSubmit
        }
        onCancel={() => {
          setModalOpen(
            false
          );
        }}
      >

        <Form
          form={form}
          layout="vertical"
        >

          <Form.Item
            label="Vehicle"
            name="vehicle_id"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Select
              options={
                vehicles.map(
                  vehicle => ({
                    label:
                      vehicle.rc_number,
                    value:
                      vehicle.vehicle_id,
                  })
                )
              }
            />
          </Form.Item>

          <Form.Item
            label="Job Card"
            name="job_card_id"
          >
            <Select
              options={
                jobCards.map(
                  card => ({
                    label:
                      `Job Card ${card.job_card_id}`,
                    value:
                      card.job_card_id,
                  })
                )
              }
            />
          </Form.Item>

          <Form.Item
            label="Technician"
            name="technician_id"
          >
            <Select
              options={
                employees.map(
                  emp => ({
                    label:
                      emp.full_name,
                    value:
                      emp.employee_id,
                  })
                )
              }
            />
          </Form.Item>

          <Form.Item
            label="Status"
            name="status"
          >
            <Select
              options={[
                {
                  label:
                    "OPEN",
                  value:
                    "OPEN",
                },
                {
                  label:
                    "APPROVED",
                  value:
                    "APPROVED",
                },
                {
                  label:
                    "ISSUED",
                  value:
                    "ISSUED",
                },
                {
                  label:
                    "CLOSED",
                  value:
                    "CLOSED",
                },
              ]}
            />
          </Form.Item>

          <Form.Item
            label="Remarks"
            name="remarks"
          >
            <Input.TextArea
              rows={4}
            />
          </Form.Item>

          <Form.Item
            label="Active"
            name="active_flag"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

        </Form>

      </Modal>

    </>
  );
};

export default PartRequisitions;