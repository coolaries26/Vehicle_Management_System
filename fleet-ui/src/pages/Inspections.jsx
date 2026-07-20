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
  PlusOutlined,
  ReloadOutlined,
  SearchOutlined,
} from "@ant-design/icons";

import {
  getInspections,
  createInspection,
  updateInspection,
  deactivateInspection,
} from "../services/inspectionService";

import {  getComplaints,} from "../services/complaintService";

import {  getEmployees,} from "../services/employeeService";

import SearchToolbar from "../components/SearchToolbar";

import tablePagination from "../utils/tablePagination";
const { Title } = Typography;

const Inspections = () => {

  const [inspections, setInspections] =
    useState([]);

  const [complaints, setComplaints] =
    useState([]);

  const [employees, setEmployees] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [modalOpen, setModalOpen] =
    useState(false);

  const [editingInspection,
    setEditingInspection] =
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
          inspectionsData,
          complaintsData,
          employeesData,
        ] = await Promise.all([
          getInspections(),
          getComplaints(),
          getEmployees(),
        ]);

        setInspections(
          inspectionsData
        );

        setComplaints(
          complaintsData
        );

        setEmployees(
          employeesData
        );

      } catch (error) {

        console.error(error);

        message.error(
          "Failed to load inspections"
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

      setEditingInspection(
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

      setEditingInspection(
        record
      );

      form.setFieldsValue({
        complaint_id:
          record.complaint_id,

        technician_id:
          record.technician_id,

        observed_issue:
          record.observed_issue,

        operator_notes:
          record.operator_notes,

        status:
          record.status,

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
          editingInspection
        ) {

          await updateInspection(
            editingInspection.inspection_id,
            values
          );

          message.success(
            "Inspection updated successfully"
          );

        } else {

          await createInspection(
            values
          );

          message.success(
            "Inspection created successfully"
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
      inspectionId
    ) => {

      try {

        await deactivateInspection(
          inspectionId
        );

        message.success(
          "Inspection deactivated"
        );

        await loadData();

      } catch (error) {

        console.error(error);

        message.error(
          "Deactivate failed"
        );
      }
    };

  const filteredInspections =
    inspections.filter(
      (inspection) => {

        const matchesSearch = (

          inspection.observed_issue
            ?.toLowerCase()
            .includes(
              searchText
                .toLowerCase()
            )

          ||

          inspection.operator_notes
            ?.toLowerCase()
            .includes(
              searchText
                .toLowerCase()
            )

          ||

          inspection.status
            ?.toLowerCase()
            .includes(
              searchText
                .toLowerCase()
            )

          ||

          String(
            inspection.inspection_id
          ).includes(searchText)

        );

        const matchesStatus =

          statusFilter === "ALL"

          ||

          (
            statusFilter ===
            "ACTIVE"

            &&

            inspection.active_flag
            === true
          )

          ||

          (
            statusFilter ===
            "INACTIVE"

            &&

            inspection.active_flag
            === false
          );

        return (
          matchesSearch
          &&
          matchesStatus
        );
      }
    );

  const complaintMap =
    Object.fromEntries(
      complaints.map(
        (complaint) => [
          complaint.complaint_id,
          complaint.complaint_id,
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

  const columns = [

    {
      title:
        "Inspection ID",

      dataIndex:
        "inspection_id",
    },

    {
      title:
        "Complaint",

      render:
        (_, record) =>

          complaintMap[
            record.complaint_id
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
        "Observed Issue",

      dataIndex:
        "observed_issue",
    },

    {
      title:
        "Operator Notes",

      dataIndex:
        "operator_notes",
    },

    {
      title:
        "Status",

      dataIndex:
        "status",
    },

    {
      title:
        "Active",

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
                "Deactivate Inspection?"
              onConfirm={() =>
                handleDeactivate(
                  record.inspection_id
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
      <div className="action-bar">
        <Title level={3}>Inspections</Title>
      </div>
      <div
        style={{
          marginBottom: 12,
          fontWeight: "bold",
        }}
      >
        <SearchToolbar
          searchText={searchText}
          setSearchText={setSearchText}
          statusFilter={statusFilter}
          setStatusFilter={setStatusFilter}
          onRefresh={loadData}
          onAdd={openCreateModal}
          searchPlaceholder="Search Inspection"
          addLabel="Add Inspection"
        />
        Total Inspections:
        {" "}
        {
          filteredInspections.length
        }
      </div>

      <Card>

        <Table
          rowKey="inspection_id"
          loading={loading}
          columns={columns}
          dataSource={
            filteredInspections
          }
          scroll={{
            x: 1500,
          }}
          pagination={tablePagination}
        />

      </Card>

      <Modal
        title={
          editingInspection
            ? "Edit Inspection"
            : "Add Inspection"
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
            label="Complaint"
            name="complaint_id"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Select
              options={
                complaints.map(
                  (complaint) => ({
                    label:
                      `Complaint ${complaint.complaint_id}`,
                    value:
                      complaint.complaint_id,
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
            label="Observed Issue"
            name="observed_issue"
          >
            <Input.TextArea
              rows={4}
            />
          </Form.Item>

          <Form.Item
            label="Operator Notes"
            name="operator_notes"
          >
            <Input.TextArea
              rows={3}
            />
          </Form.Item>

          <Form.Item
            label="Status"
            name="status"
          >
            <Select
              options={[
                {
                  label: "OPEN",
                  value: "OPEN",
                },
                {
                  label: "IN_PROGRESS",
                  value: "IN_PROGRESS",
                },
                {
                  label: "COMPLETED",
                  value: "COMPLETED",
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

export default Inspections;