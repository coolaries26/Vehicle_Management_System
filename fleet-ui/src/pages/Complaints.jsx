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
  getComplaints,
  createComplaint,
  updateComplaint,
  deactivateComplaint,
} from "../services/complaintService";

import {  getVehicles,} from "../services/vehicleService";

import {  getDrivers,} from "../services/driverService";

import SearchToolbar from "../components/SearchToolbar";

import tablePagination from "../utils/tablePagination";

const { Title } =
  Typography;

const Complaints = () => {

  const [complaints,
    setComplaints] =
    useState([]);

  const [vehicles,
    setVehicles] =
    useState([]);

  const [drivers,
    setDrivers] =
    useState([]);

  const [loading,
    setLoading] =
    useState(false);

  const [modalOpen,
    setModalOpen] =
    useState(false);

  const [editingComplaint,
    setEditingComplaint] =
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
          complaintsData,
          vehiclesData,
          driversData,
        ] = await Promise.all([
          getComplaints(),
          getVehicles(),
          getDrivers(),
        ]);

        setComplaints(
          complaintsData
        );

        setVehicles(
          vehiclesData
        );

        setDrivers(
          driversData
        );

      } catch (error) {

        console.error(
          error
        );

        message.error(
          "Failed to load complaints"
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

  const driverMap =
    Object.fromEntries(
      drivers.map(
        (driver) => [
          driver.driver_id,
          driver.driver_name,
        ]
      )
    );

  const openCreateModal =
    () => {

      setEditingComplaint(
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

      setEditingComplaint(
        record
      );

      form.setFieldsValue({

        vehicle_id:
          record.vehicle_id,

        driver_id:
          record.driver_id,

        issue_description:
          record.issue_description,

        driver_reason:
          record.driver_reason,

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
          editingComplaint
        ) {

          await updateComplaint(
            editingComplaint.complaint_id,
            values
          );

          message.success(
            "Complaint updated successfully"
          );

        } else {

          await createComplaint(
            values
          );

          message.success(
            "Complaint created successfully"
          );
        }

        setModalOpen(
          false
        );

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
      complaintId
    ) => {

      try {

        await deactivateComplaint(
          complaintId
        );

        message.success(
          "Complaint deactivated"
        );

        await loadData();

      } catch (error) {

        message.error(
          "Deactivate failed"
        );
      }
    };

  const filteredComplaints =
    complaints.filter(
      (complaint) => {

        const matchesSearch =
          (
            complaint.issue_description
              ?.toLowerCase()
              .includes(
                searchText
                  .toLowerCase()
              )

            ||

            complaint.driver_reason
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

            complaint.active_flag
            === true
          )

          ||

          (
            statusFilter ===
            "INACTIVE"

            &&

            complaint.active_flag
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
        "Complaint ID",

      dataIndex:
        "complaint_id",
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
        "Driver",

      render:
        (_, record) =>

          driverMap[
            record.driver_id
          ] ?? "-",
    },

    {
      title:
        "Issue",

      dataIndex:
        "issue_description",
    },

    {
      title:
        "Driver Reason",

      dataIndex:
        "driver_reason",
    },

    {
      title:
        "Status",

      render:
        (_, record) =>

          record.active_flag
            ?

            (
              <Tag color="green">
                Active
              </Tag>
            )

            :

            (
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
                "Deactivate Complaint?"
              onConfirm={() =>
                handleDeactivate(
                  record.complaint_id
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
        <Title level={3}>Complaints</Title>
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
          onRefresh={loadData}
          onAdd={openCreateModal}
          searchPlaceholder="Search Complaint"
          addLabel="Add Complaint"
        />
        Total Complaints:
        {""}
        {
          filteredComplaints.length
        }
      </div>

      <Card>

        <Table
          rowKey="complaint_id"
          columns={columns}
          dataSource={filteredComplaints}
          loading={loading}
          scroll={{
            x: 1500,
          }}
          pagination={tablePagination}
        />

      </Card>

      <Modal
        title={
          editingComplaint
            ?
            "Edit Complaint"
            :
            "Add Complaint"
        }
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() =>
          setModalOpen(false)
        }
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
            label="Driver"
            name="driver_id"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Select
              options={
                drivers.map(
                  (driver) => ({
                    label:
                      driver.driver_name,
                    value:
                      driver.driver_id,
                  })
                )
              }
            />
          </Form.Item>

          <Form.Item
            label="Issue Description"
            name="issue_description"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Input.TextArea rows={4} />
          </Form.Item>

          <Form.Item
            label="Driver Reason"
            name="driver_reason"
          >
            <Input.TextArea rows={3} />
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

export default Complaints;