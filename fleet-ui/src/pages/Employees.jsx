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
  Typography,
  message,
  Tag,
} from "antd";

import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  TeamOutlined,
  SearchOutlined,
} from "@ant-design/icons";

import {
  getEmployees,
  createEmployee,
  updateEmployee,
  deleteEmployee,
} from "../services/employeeService";

import SearchToolbar
from "../components/SearchToolbar";

import tablePagination
from "../utils/tablePagination";

const { Title } = Typography;

const employeeTypeOptions = [
  {
    label: "Technician",
    value: "TECHNICIAN",
  },
  {
    label: "Supervisor",
    value: "SUPERVISOR",
  },
  {
    label: "Store Incharge",
    value: "STORE_INCHARGE",
  },
  {
    label: "Manager",
    value: "MANAGER",
  },
  {
    label: "Helper",
    value: "HELPER",
  },
  {
    label: "Other",
    value: "OTHER",
  },
];

const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(false);

  const [modalOpen, setModalOpen] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState(null);
  const activeEmployees = employees.filter( employee => employee.active_flag );
  const [searchText, setSearchText] =  useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");


  const [form] = Form.useForm();

  const loadEmployees = async () => {
    try {
      setLoading(true);

      const data = await getEmployees();

      console.log("Employees API Data:", data);

      setEmployees(data);
    } catch (error) {
      console.error(error);
      message.error("Failed to load employees");
    } finally {
      setLoading(false);
    }
  };
  const filteredEmployees =
    employees.filter(
      (employee) =>
        (employee.full_name
          ?.toLowerCase()
          .includes(
            searchText.toLowerCase()
          ) ||

        employee.phone_number
          ?.toLowerCase()
          .includes(
            searchText.toLowerCase()
          ) ||

        employee.employee_type
          ?.toLowerCase()
          .includes(
            searchText.toLowerCase()
          ) ||

        String(
          employee.employee_id
        ).includes(searchText))
        &&
        (
          statusFilter === "ALL"
          ||
          (
            statusFilter === "ACTIVE"
            && employee.active_flag
          )
          ||
          (
            statusFilter === "INACTIVE"
            && !employee.active_flag
          )
        )
  );
  useEffect(() => {
    loadEmployees();
  }, []);

  const openCreateModal = () => {
    setEditingEmployee(null);
    form.resetFields();
    form.setFieldsValue({
    active_flag: true,
    });
    form.setFieldsValue({
      employee_type: "TECHNICIAN",
    });

    setModalOpen(true);
  };

  const openEditModal = (record) => {
    setEditingEmployee(record);

    form.setFieldsValue({
      employee_type: record.employee_type,
      full_name: record.full_name,
      phone_number: record.phone_number,
    
      active_flag:
        record.active_flag ?? true,
    });
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();

      if (editingEmployee) {
        const updatedEmployee = await updateEmployee(
          editingEmployee.employee_id,
          values
        );

        setEmployees((previousEmployees) =>
          previousEmployees.map((employee) =>
            employee.employee_id === editingEmployee.employee_id
              ? {
                  ...employee,
                  ...updatedEmployee,
                }
              : employee
          )
        );

        message.success("Employee updated successfully");
      } else {
        const newEmployee = await createEmployee(values);

        setEmployees((previousEmployees) => [
          newEmployee,
          ...previousEmployees,
        ]);

        message.success("Employee created successfully");
      }

      setModalOpen(false);
      setEditingEmployee(null);
      form.resetFields();

      await loadEmployees();
    } catch (error) {
      console.error(error);

      if (error?.response?.status === 409) {
        message.error("Employee already exists");
      } else if (error?.response?.status === 422) {
        message.error("Validation failed. Please check the form.");
      } else {
        message.error("Operation failed");
      }
    }
  };

  const handleDelete = async (employeeId) => {
    try {
      await deleteEmployee(employeeId);

      message.success("Employee deactivated successfully");

      await loadEmployees();
    } catch (error) {
      console.error(error);
      message.error("deactivate failed");
    }
  };

  const renderEmployeeType = (value) => {
    if (!value) {
      return "-";
    }

    const colorMap = {
      TECHNICIAN: "blue",
      SUPERVISOR: "purple",
      STORE_INCHARGE: "orange",
      MANAGER: "green",
      HELPER: "cyan",
      OTHER: "default",
    };

    return (
      <Tag color={colorMap[value] || "default"}>
        {value}
      </Tag>
    );
  };

  const columns = [
    {
      title: "Employee ID",
      dataIndex: "employee_id",
      key: "employee_id",
      width: 120,
    },
    {
      title: "Employee Type",
      dataIndex: "employee_type",
      key: "employee_type",
      render: renderEmployeeType,
    },
    {
      title: "Full Name",
      dataIndex: "full_name",
      key: "full_name",
      render: (value) => value ?? "-",
    },
    {
      title: "Phone Number",
      dataIndex: "phone_number",
      key: "phone_number",
      render: (value) => value ?? "-",
    },
    {
      title: "Last Updated",
      dataIndex: "modified_at",
      key: "modified_at",
      render: (value) => value ?? "-",
    },
    {
      title: "Updated By",
      dataIndex: "modified_by",
      key: "modified_by",
      render: (value) => value ?? "-",
    },
    {
      title: "Status",
      dataIndex: "active_flag",
      key: "active_flag",
      render: (value) => {
        return value
          ? <Tag color="green">Active</Tag>
          : <Tag color="red">Inactive</Tag>;
      },
    },
    {
      title: "Actions",
      key: "actions",
      width: 180,
      render: (_, record) => (
        <Space>
          <Button
            icon={<EditOutlined />}
            onClick={() => openEditModal(record)}
          >
            Edit
          </Button>

          <Popconfirm
            title="Dactivate employee?"
            description="Are you sure you want to deactive this employee?"
            okText="Yes"
            cancelText="No"
            onConfirm={() => handleDelete(record.employee_id)}
          >
            <Button
              danger
              icon={<DeleteOutlined />}
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
        <Title level={3}> <TeamOutlined /> Employees</Title>
      </div>
      <div
        style={{
          marginBottom: 2,
          fontWeight: "bold",
        }}
      >
        <SearchToolbar
          searchText={searchText}
          setSearchText={setSearchText}
          statusFilter={statusFilter}
          setStatusFilter={setStatusFilter}
          onRefresh={loadEmployees}
          onAdd={openCreateModal}
          searchPlaceholder="Search Employee"
          addLabel="Add Employee"
        />
        Total Employees:
        {" "}
        {filteredEmployees.length}
      </div>
      <Card>
        <Table
          rowKey="employee_id"
          loading={loading}
          columns={columns}
          dataSource={filteredEmployees}
          scroll={{ x: 1500 }}
          pagination={tablePagination}
        />
      </Card>

      <Modal
        title={
          editingEmployee
            ? "Edit Employee"
            : "Add Employee"
        }
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => {
          setModalOpen(false);
          setEditingEmployee(null);
          form.resetFields();
        }}
        okText={
          editingEmployee
            ? "Update"
            : "Create"
        }
      >
        <Form
          layout="vertical"
          form={form}
        >
          <Form.Item
            label="Employee Type"
            name="employee_type"
            rules={[
              {
                required: true,
                message: "Employee type is required",
              },
            ]}
          >
            <Select
              placeholder="Select employee type"
              options={employeeTypeOptions}
            />
          </Form.Item>

          <Form.Item
            label="Full Name"
            name="full_name"
            rules={[
              {
                required: true,
                message: "Full name is required",
              },
              {
                min: 2,
                message: "Full name must be at least 2 characters",
              },
            ]}
          >
            <Input placeholder="Example: John Doe" />
          </Form.Item>

          <Form.Item
            label="Phone Number"
            name="phone_number"
            rules={[
              {
                required: true,
                message: "Phone number is required",
              },
              {
                min: 10,
                message: "Phone number must be at least 10 digits",
              },
              {
                max: 15,
                message: "Phone number must not exceed 15 digits",
              },
            ]}
          >
            <Input placeholder="Example: 9999999999" />
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

export default Employees;