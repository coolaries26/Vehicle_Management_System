import { useEffect, useState } from "react";

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

import SearchToolbar from "../components/SearchToolbar";

import tablePagination from "../utils/tablePagination";

import {
  getChecklists,
  createChecklist,
  updateChecklist,
  deactivateChecklist,
} from "../services/checklistService";

import {
  getVehicles,
} from "../services/vehicleService";

import {
  getEmployees,
} from "../services/employeeService";

const { Title } = Typography;

const Checklists = () => {

  const [checklists, setChecklists] =
    useState([]);

  const [vehicles, setVehicles] =
    useState([]);

  const [employees, setEmployees] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [modalOpen, setModalOpen] =
    useState(false);

  const [editingChecklist,
    setEditingChecklist] =
    useState(null);

  const [searchText,
    setSearchText] =
    useState("");

  const [statusFilter,
    setStatusFilter] =
    useState("ALL");

  const [form] =
    Form.useForm();

  const loadData =
    async () => {

      try {

        setLoading(true);

        const [
          checklistData,
          vehicleData,
          employeeData,
        ] = await Promise.all([
          getChecklists(),
          getVehicles(),
          getEmployees(),
        ]);

        setChecklists(
          checklistData
        );

        setVehicles(
          vehicleData
        );

        setEmployees(
          employeeData
        );

      } catch (error) {

        console.error(error);

        message.error(
          "Failed to load checklists"
        );

      } finally {

        setLoading(false);
      }
    };

  useEffect(() => {
    loadData();
  }, []);

  const vehicleMap =
    Object.fromEntries(
      vehicles.map(
        (vehicle) => [
          vehicle.vehicle_id,
          vehicle.rc_number,
        ]
      )
    );

  const technicianMap =
    Object.fromEntries(
      employees.map(
        (employee) => [
          employee.employee_id,
          employee.full_name,
        ]
      )
    );

  const openCreateModal =
    () => {

      setEditingChecklist(
        null
      );

      form.resetFields();

      form.setFieldsValue({
        issue_found: false,
        active_flag: true,
        final_status: "PASS",
      });

      setModalOpen(true);
    };

  const openEditModal =
    (record) => {

      setEditingChecklist(
        record
      );

      form.setFieldsValue({
        vehicle_id:
          record.vehicle_id,

        technician_id:
          record.technician_id,

        observation:
          record.observation,

        issue_found:
          record.issue_found,

        issue_description:
          record.issue_description,

        maintenance_action:
          record.maintenance_action,

        final_status:
          record.final_status,

        active_flag:
          record.active_flag,
      });

      setModalOpen(true);
    };

  const handleSubmit =
    async () => {

      try {

        const values =
          await form.validateFields();

        if (
          editingChecklist
        ) {

          await updateChecklist(
            editingChecklist.checklist_id,
            values
          );

          message.success(
            "Checklist updated successfully"
          );

        } else {

          await createChecklist(
            values
          );

          message.success(
            "Checklist created successfully"
          );
        }

        setModalOpen(false);

        form.resetFields();

        await loadData();

      } catch (error) {

        console.error(error);

        message.error(
          "Operation failed"
        );
      }
    };

  const handleDeactivate =
    async (
      checklistId
    ) => {

      try {

        await deactivateChecklist(
          checklistId
        );

        message.success(
          "Checklist deactivated"
        );

        await loadData();

      } catch (error) {

        console.error(error);

        message.error(
          "Deactivate failed"
        );
      }
    };

  const filteredChecklists =
    checklists.filter(
      (checklist) => {

        const matchesSearch = (

          checklist.observation
            ?.toLowerCase()
            .includes(
              searchText.toLowerCase()
            )

          ||

          checklist.issue_description
            ?.toLowerCase()
            .includes(
              searchText.toLowerCase()
            )

          ||

          checklist.final_status
            ?.toLowerCase()
            .includes(
              searchText.toLowerCase()
            )

          ||

          String(
            checklist.checklist_id
          ).includes(searchText)

        );

        const matchesStatus =

          statusFilter ===
          "ALL"

          ||

          (
            statusFilter ===
            "ACTIVE"

            &&

            checklist.active_flag
            === true
          )

          ||

          (
            statusFilter ===
            "INACTIVE"

            &&

            checklist.active_flag
            === false
          );

        return (
          matchesSearch
          &&
          matchesStatus
        );
      }
    );

  const columns = [

    {
      title:
        "Checklist ID",

      dataIndex:
        "checklist_id",
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
        "Technician",

      render:
        (_, record) =>
          technicianMap[
            record.technician_id
          ] ?? "-",
    },

    {
      title:
        "Issue Found",

      render:
        (_, record) =>

          record.issue_found

            ? (
              <Tag color="red">
                Yes
              </Tag>
            )

            : (
              <Tag color="green">
                No
              </Tag>
            ),
    },

    {
      title:
        "Final Status",

      dataIndex:
        "final_status",
    },

    {
      title:
        "Status",

      render:
        (_, record) =>

          record.active_flag

            ? (
              <Tag color="green">
                Active
              </Tag>
            )

            : (
              <Tag color="red">
                Inactive
              </Tag>
            ),
    },

    {
      title:
        "Actions",

      render:
        (_, record) => (

          <Space>

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
              title=
                "Deactivate Checklist?"
              onConfirm={() =>
                handleDeactivate(
                  record.checklist_id
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
        Preventive Maintenance Checklists
      </Title>

      <SearchToolbar
        searchText={searchText}
        setSearchText={setSearchText}
        statusFilter={statusFilter}
        setStatusFilter={setStatusFilter}
        onRefresh={loadData}
        onAdd={openCreateModal}
        searchPlaceholder="Search Checklist"
        addLabel="Add Checklist"
      />

      <div
        style={{
          marginBottom: 12,
          fontWeight: "bold",
        }}
      >
        Total Checklists:{" "}
        {
          filteredChecklists.length
        }
      </div>

      <Card>

        <Table
          rowKey="checklist_id"
          loading={loading}
          columns={columns}
          dataSource={
            filteredChecklists
          }
          pagination={
            tablePagination
          }
          scroll={{
            x: 1500,
          }}
        />

      </Card>

      <Modal
        title={
          editingChecklist
            ? "Edit Checklist"
            : "Add Checklist"
        }
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => {
          setModalOpen(false);
          form.resetFields();
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
                message:
                  "Vehicle is required",
              },
            ]}
          >
            <Select
              options={
                vehicles.map(
                  (vehicle) => ({
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
            label="Technician"
            name="technician_id"
            rules={[
              {
                required: true,
                message:
                  "Technician is required",
              },
            ]}
          >
            <Select
              options={
                employees.map(
                  (employee) => ({
                    label:
                      employee.full_name,
                    value:
                      employee.employee_id,
                  })
                )
              }
            />
          </Form.Item>

          <Form.Item
            label="Observation"
            name="observation"
          >
            <Input.TextArea
              rows={3}
            />
          </Form.Item>

          <Form.Item
            label="Issue Found"
            name="issue_found"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            label="Issue Description"
            name="issue_description"
          >
            <Input.TextArea
              rows={3}
            />
          </Form.Item>

          <Form.Item
            label="Maintenance Action"
            name="maintenance_action"
          >
            <Input.TextArea
              rows={3}
            />
          </Form.Item>

          <Form.Item
            label="Final Status"
            name="final_status"
          >
            <Select
              options={[
                {
                  label: "PASS",
                  value: "PASS",
                },
                {
                  label: "FAIL",
                  value: "FAIL",
                },
                {
                  label:
                    "REQUIRES_ATTENTION",
                  value:
                    "REQUIRES_ATTENTION",
                },
              ]}
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

export default Checklists;