import {  useEffect,  useState,} from "react";
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
  Tag,
  Typography,
  message,
} from "antd";

import {
  DeleteOutlined,
  EditOutlined,
  PlusOutlined,
  ReloadOutlined,
  TeamOutlined,
  SearchOutlined,
} from "@ant-design/icons";

import {
  createDriver,
  deactivateDriver,
  getDrivers,
  updateDriver,
} from "../services/driverService";

import SearchToolbar from "../components/SearchToolbar";

import tablePagination from "../utils/tablePagination";
const { Title } = Typography;

const Drivers = () => {

  const [drivers,     setDrivers] =  useState([]);
  const [loading,     setLoading] =  useState(false);

  const [modalOpen, setModalOpen] =  useState(false);
  const [editingDriver, setEditingDriver] =   useState(null);

  const [searchText,   setSearchText] =    useState("");
  const [statusFilter,  setStatusFilter] =   useState("ALL");

  const [form] =    Form.useForm();

  const loadDrivers =
    async () => {
      try {
        setLoading(true);
        const data = await getDrivers();
        console.log("Loaded drivers:", data);
        setDrivers(data);

      } catch (error) {
        console.error(error);
        message.error( "Failed to load drivers");
      } finally {
        setLoading(false);
      }
    };

  useEffect(() => {
    loadDrivers();
  }, []);

  const openCreateModal =
    () => {

      setEditingDriver(
        null
      );

      form.resetFields();

      form.setFieldsValue({
        active_flag: true,
      });

      setModalOpen(
        true
      );
    };

  const openEditModal =
    (record) => {

      setEditingDriver(
        record
      );

      form.setFieldsValue({
        driver_name:
          record.driver_name,

        mobile_number:
          record.mobile_number,

        dl_number:
          record.dl_number,

        dl_expiry_date:
          record.dl_expiry_date,

        permanent_address:
          record.permanent_address,

        active_flag:
          record.active_flag,
      });

      setModalOpen(
        true
      );
    };

  const handleSubmit =
    async () => {

      try {

        const values =
          await form.validateFields();

        if (
          editingDriver
        ) {

          await updateDriver(
            editingDriver.driver_id,
            values
          );

          message.success(
            "Driver updated successfully"
          );

        } else {

          await createDriver(
            values
          );

          message.success(
            "Driver created successfully"
          );
        }

        setModalOpen(
          false
        );

        form.resetFields();

        await loadDrivers();

      } catch (error) {

        console.error(
          error
        );

        if (
          error?.response
            ?.status ===
          409
        ) {

          message.error(
            "Duplicate DL Number"
          );

        } else {

          message.error(
            "Operation failed"
          );
        }
      }
    };

  const filteredDrivers =
    drivers.filter(
      (driver) => {

        const matchesSearch = (

          driver.driver_name
            ?.toLowerCase()
            .includes(
              searchText
                .toLowerCase()
            )

          ||

          driver.mobile_number
            ?.toLowerCase()
            .includes(
              searchText
                .toLowerCase()
            )

          ||

          driver.dl_number
            ?.toLowerCase()
            .includes(
              searchText
                .toLowerCase()
            )
        );

        const matchesStatus =
          statusFilter ===
          "ALL"

          ||

          (
            statusFilter ===
            "ACTIVE"

            &&

            driver.active_flag
            === true
          )

          ||

          (
            statusFilter ===
            "INACTIVE"

            &&

            driver.active_flag
            === false
          );

        return (
          matchesSearch
          &&
          matchesStatus
        );
      }
    );

  const handleDeactivate =
    async (
      driverId
    ) => {
      try {
        await deactivateDriver(
          driverId
        );
        message.success(
          "Driver deactivated"
        );

        await loadDrivers();

      } catch (error) {

        console.error(
          error
        );

        message.error(
          "Deactivate failed"
        );
      }
    };

  const columns = [

    {
      title:
        "Driver ID",
      dataIndex:
        "driver_id",
    },

    {
      title:
        "Driver Name",
      dataIndex:
        "driver_name",
    },

    {
      title:
        "Mobile",
      dataIndex:
        "mobile_number",
    },

    {
      title:
        "DL Number",
      dataIndex:
        "dl_number",
    },

    {
      title:
        "DL Expiry",

      dataIndex:
        "dl_expiry_date",

      render:
        (value) =>
          value ?? "-",
    },

    {
      title: "Status",
      dataIndex: "active_flag",

      render:
        (value) =>

          value === true

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
              title="Deactivate Driver?"
              onConfirm={() =>
                handleDeactivate(
                  record.driver_id
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
        <Title level={3}>Drivers</Title>
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
          onRefresh={loadDrivers}
          onAdd={openCreateModal}
          searchPlaceholder="Search Driver"
          addLabel="Add Driver"
        />
        Total Drivers:
        {""}
        {
          filteredDrivers.length
        }
      </div>

      <Card>

        <Table
          rowKey="driver_id"
          columns={columns}
          loading={loading}
          dataSource={ filteredDrivers }
          scroll={{ x: 1500 }}
          pagination={tablePagination}
        />

      </Card>

      <Modal
        title={
          editingDriver
            ?
            "Edit Driver"
            :
            "Add Driver"
        }

        open={modalOpen}

        onOk={
          handleSubmit
        }

        onCancel={() =>
          setModalOpen(
            false
          )
        }
      >

        <Form
          form={form}
          layout="vertical"
        >

          <Form.Item
            label=
              "Driver Name"
            name=
              "driver_name"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label=
              "Mobile Number"
            name=
              "mobile_number"
          >
            <Input />
          </Form.Item>

          <Form.Item
            label=
              "DL Number"
            name=
              "dl_number"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label=
              "DL Expiry Date"
            name=
              "dl_expiry_date"
          >
            <Input
              type="date"
            />
          </Form.Item>

          <Form.Item
            label=
              "Permanent Address"
            name=
              "permanent_address"
          >
            <Input.TextArea
              rows={3}
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

export default Drivers;
