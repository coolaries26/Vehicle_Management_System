import { useEffect, useState } from "react";
import {
  Button,
  Card,
  Form,
  Input,
  InputNumber,
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
  getVehicles,
  createVehicle,
  updateVehicle,
  deleteVehicle,
} from "../services/vehicleService";

import SearchToolbar from "../components/SearchToolbar";

import tablePagination from "../utils/tablePagination";
const { Title } = Typography;

const Vehicles = () => {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(false);

  const [modalOpen, setModalOpen] = useState(false);
  const [editingVehicle, setEditingVehicle] = useState(null);
  const [searchText, setSearchText] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");


  const [form] = Form.useForm();

  const loadVehicles = async () => {
    try {
      setLoading(true);

      const data = await getVehicles();

      console.log("Loaded vehicles:", data);

      setVehicles(data);
    } catch (error) {
      console.error(error);
      message.error("Failed to load vehicles");
    } finally {
      setLoading(false);
    }
  };

  const filteredVehicles = vehicles.filter(
    (vehicle) =>
      (vehicle.rc_number
        ?.toLowerCase()
        .includes(
          searchText.toLowerCase()
        ) ||
      
      vehicle.engine_no
        ?.toLowerCase()
        .includes(
          searchText.toLowerCase()
        ) ||
      
      vehicle.chassis_no
        ?.toLowerCase()
        .includes(
          searchText.toLowerCase()
        ) ||
      
      String(
        vehicle.vehicle_id
      ).includes(searchText))
        &&
      (
        statusFilter === "ALL"
        ||
        (
          statusFilter === "ACTIVE"
          && vehicle.active_flag
        )
        ||
        (
          statusFilter === "INACTIVE"
          && !vehicle.active_flag
        )
      )

  );

  useEffect(() => {
    loadVehicles();
  }, []);


  const openCreateModal = () => {
    setEditingVehicle(null);
    form.resetFields();
    form.setFieldsValue({
        active_flag: true,
    });
    setModalOpen(true);
  };

  const openEditModal = (record) => {
    setEditingVehicle(record);

    form.setFieldsValue({
      rc_number: record.rc_number,
      vehicle_type_id: record.vehicle_type_id,
      fuel_type_id: record.fuel_type_id,
      vehicle_status_id: record.vehicle_status_id,
        
      purchase_date: record.purchase_date,
      rc_expiry_date: record.rc_expiry_date,
        
      engine_no: record.engine_no,
      chassis_no: record.chassis_no,
      gps_id: record.gps_id,
        
      fuel_capacity: record.fuel_capacity ?? true,
    
      active_flag:
        record.active_flag ?? true,
    });
    
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();

      if (editingVehicle) {
        const updatedVehicle = await updateVehicle(
          editingVehicle.vehicle_id,
          values
        );

        setVehicles((previousVehicles) =>
          previousVehicles.map((vehicle) =>
            vehicle.vehicle_id === editingVehicle.vehicle_id
              ? {
                  ...vehicle,
                  ...updatedVehicle,
                }
              : vehicle
          )
        );

        message.success("Vehicle updated successfully");
      } else {
        const newVehicle = await createVehicle(values);

        setVehicles((previousVehicles) => [
          newVehicle,
          ...previousVehicles,
        ]);

        message.success("Vehicle created successfully");
      }

      setModalOpen(false);
      setEditingVehicle(null);
      form.resetFields();

      await loadVehicles();
    } catch (error) {
      console.error(error);

      if (error?.response?.status === 409) {
        message.error("Vehicle already exists");
      } else if (error?.response?.status === 422) {
        message.error("Validation failed. Please check the form.");
      } else {
        message.error("Operation failed");
      }
    }
  };
  const handleDelete = async (vehicleId) => {
    try {
      await deleteVehicle(vehicleId);

      message.success("Vehicle deactivated successfully");

      await loadVehicles();
    } catch (error) {
      console.error(error);
      message.error("Deactivation failed");
    }
  };

  const columns = [
    {
      title: "Vehicle ID",
      dataIndex: "vehicle_id",
      key: "vehicle_id",
      width: 120,
    },
    {
      title: "RC Number",
      dataIndex: "rc_number",
      key: "rc_number",
    },
    {
      title: "Engine No",
      dataIndex: "engine_no",
      key: "engine_no",
    },
    {
      title: "Chassis No",
      dataIndex: "chassis_no",
      key: "chassis_no",
    },
    {
      title: "Fuel Capacity",
      dataIndex: "fuel_capacity",
      key: "fuel_capacity",
      render: (value) => value ?? "-",
    },
    {
      title: "Vehicle Type",
      dataIndex: "vehicle_type_id",
      key: "vehicle_type_id",
      render: (value) => value ?? "-",
    },
    {
      title: "Fuel Type",
      dataIndex: "fuel_type_id",
      key: "fuel_type_id",
      render: (value) => value ?? "-",
    },
    {
      title: "Status",
      dataIndex: "vehicle_status_id",
      key: "vehicle_status_id",
      render: (value) => value ?? "-",
    },
    {
      title: "GPS ID",
      dataIndex: "gps_id",
      key: "gps_id",
      render: (value) => value ?? "-",
    },
    {
      title: "Purchase Date",
      dataIndex: "purchase_date",
      key: "purchase_date",
      render: (value) => value ?? "-",
    },
    {
      title: "RC Expiry",
      dataIndex: "rc_expiry_date",
      key: "rc_expiry_date",
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
            title="Deactivate vehicle?"
            description="Are you sure you want to deactivate this vehicle?"
            okText="Yes"
            cancelText="No"
            onConfirm={() => handleDelete(record.vehicle_id)}
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
        <Title level={3}>Vehicles</Title>
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
            onRefresh={loadVehicles}
            onAdd={openCreateModal}
            searchPlaceholder="Search Vehicle"
            addLabel="Add Vehicle"
          />
        Total Vehicles:
        {" "}
        {filteredVehicles.length}
      </div>

      <Card>
        <Table
          rowKey="vehicle_id"
          loading={loading}
          columns={columns}
          dataSource={filteredVehicles}
          scroll={{ x: 1500 }}
          size="middle"
          variant
          pagination={tablePagination}
        />
      </Card>

      <Modal
        title={
          editingVehicle
            ? "Edit Vehicle"
            : "Add Vehicle"
        }
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => setModalOpen(false)}
        okText={
          editingVehicle
            ? "Update"
            : "Create"
        }
      >
        <Form
          layout="vertical"
          form={form}
        >
          <Form.Item
            label="RC Number"
            name="rc_number"
            rules={[
              {
                required: true,
                message: "RC Number is required",
              },
              {
                min: 5,
                message: "RC Number must be at least 5 characters",
              },
            ]}
          >
            <Input placeholder="Example: TS09AB1234" />
          </Form.Item>

          <Form.Item
            label="Vehicle Type ID"
            name="vehicle_type_id"
          >
            <InputNumber
              style={{ width: "100%" }}
              placeholder="Vehicle Type ID"
            />
          </Form.Item>

          <Form.Item
            label="Fuel Type ID"
            name="fuel_type_id"
          >
            <InputNumber
              style={{ width: "100%" }}
              placeholder="Fuel Type ID"
            />
          </Form.Item>

          <Form.Item
            label="Fuel Capacity"
            name="fuel_capacity"
          >
            <InputNumber
              style={{ width: "100%" }}
              min={0}
              placeholder="Fuel capacity"
            />
          </Form.Item>

          <Form.Item
            label="Vehicle Status ID"
            name="vehicle_status_id"
          >
            <InputNumber
              style={{ width: "100%" }}
              placeholder="Vehicle Status ID"
            />
          </Form.Item>

          <Form.Item
            label="Purchase Date"
            name="purchase_date"
          >
            <Input type="date" />
          </Form.Item>

          <Form.Item
            label="RC Expiry Date"
            name="rc_expiry_date"
          >
            <Input type="date" />
          </Form.Item>

          <Form.Item
            label="Engine Number"
            name="engine_no"
          >
            <Input placeholder="Engine number" />
          </Form.Item>

          <Form.Item
            label="Chassis Number"
            name="chassis_no"
          >
            <Input placeholder="Chassis number" />
          </Form.Item>

          <Form.Item
            label="GPS ID"
            name="gps_id"
          >
            <Input placeholder="GPS Device ID" />
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

export default Vehicles;
