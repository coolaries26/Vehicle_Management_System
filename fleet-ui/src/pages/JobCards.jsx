import {
  useEffect,
  useState,
} from "react";

import {
  Button,
  Card,
  Form,
  Input,
  InputNumber,
  Modal,
  Popconfirm,
  Space,
  Switch,
  Table,
  Tag,
  Typography,
  message,
  Select,
} from "antd";

import {
  DeleteOutlined,
  EditOutlined,
} from "@ant-design/icons";

import SearchToolbar from "../components/SearchToolbar";

import tablePagination from "../utils/tablePagination";

import {
  getJobCards,
  createJobCard,
  updateJobCard,
  deactivateJobCard,
} from "../services/jobCardService";

import {
  getVehicles,
} from "../services/vehicleService";

import {
  getComplaints,
} from "../services/complaintService";

import {
  getInspections,
} from "../services/inspectionService";

const { Title } = Typography;

const JobCards = () => {

  const [jobCards, setJobCards] =
    useState([]);

  const [vehicles, setVehicles] =
    useState([]);

  const [complaints, setComplaints] =
    useState([]);

  const [inspections, setInspections] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [modalOpen, setModalOpen] =
    useState(false);

  const [editingJobCard,
    setEditingJobCard] =
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
          jobCardsData,
          vehiclesData,
          complaintsData,
          inspectionsData,
        ] = await Promise.all([
          getJobCards(),
          getVehicles(),
          getComplaints(),
          getInspections(),
        ]);

        setJobCards(
          jobCardsData
        );

        setVehicles(
          vehiclesData
        );

        setComplaints(
          complaintsData
        );

        setInspections(
          inspectionsData
        );

      } catch (error) {

        console.error(error);

        message.error(
          "Failed to load job cards"
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

      setEditingJobCard(
        null
      );

      form.resetFields();

      form.setFieldsValue({
        active_flag: true,
      });

      setModalOpen(true);
    };

  const openEditModal =
    (record) => {

      setEditingJobCard(
        record
      );

      form.setFieldsValue({
        vehicle_id:
          record.vehicle_id,

        complaint_id:
          record.complaint_id,

        inspection_id:
          record.inspection_id,

        description:
          record.description,

        labour_charges:
          record.labour_charges,

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
          editingJobCard
        ) {

          await updateJobCard(
            editingJobCard.job_card_id,
            values
          );

          message.success(
            "Job card updated successfully"
          );

        } else {

          await createJobCard(
            values
          );

          message.success(
            "Job card created successfully"
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
      jobCardId
    ) => {

      try {

        await deactivateJobCard(
          jobCardId
        );

        message.success(
          "Job card deactivated"
        );

        await loadData();

      } catch (error) {

        console.error(error);

        message.error(
          "Deactivate failed"
        );
      }
    };

  const filteredJobCards =
    jobCards.filter(
      (jobCard) => {

        const matchesSearch =

          (
            jobCard.description
              ?.toLowerCase()
              .includes(
                searchText
                  .toLowerCase()
              )

            ||

            String(
              jobCard.job_card_id
            ).includes(
              searchText
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

            jobCard.active_flag
            === true
          )

          ||

          (
            statusFilter ===
            "INACTIVE"

            &&

            jobCard.active_flag
            === false
          );

        return (
          matchesSearch
          &&
          matchesStatus
        );
      }
    );

  const vehicleMap =
    Object.fromEntries(
      vehicles.map(
        (vehicle) => [
          vehicle.vehicle_id,
          vehicle.rc_number,
        ]
      )
    );

  const columns = [

    {
      title:
        "Job Card ID",

      dataIndex:
        "job_card_id",
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
        "Complaint",

      dataIndex:
        "complaint_id",
    },

    {
      title:
        "Inspection",

      dataIndex:
        "inspection_id",
    },

    {
      title:
        "Description",

      dataIndex:
        "description",
    },

    {
      title:
        "Labour Charges",

      dataIndex:
        "labour_charges",
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
              title="Deactivate Job Card?"
              onConfirm={() =>
                handleDeactivate(
                  record.job_card_id
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
        Job Cards
      </Title>

      <SearchToolbar
        searchText={searchText}
        setSearchText={setSearchText}
        statusFilter={statusFilter}
        setStatusFilter={
          setStatusFilter
        }
        onRefresh={loadData}
        onAdd={openCreateModal}
        searchPlaceholder="Search Job Card"
        addLabel="Add Job Card"
      />

      <div
        style={{
          marginBottom: 2,
          fontWeight: "bold",
        }}
      >
        Total Job Cards:{" "}
        {
          filteredJobCards.length
        }
      </div>

      <Card>

        <Table
          rowKey="job_card_id"
          loading={loading}
          columns={columns}
          dataSource={
            filteredJobCards
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
          editingJobCard
            ? "Edit Job Card"
            : "Add Job Card"
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
            label="Inspection"
            name="inspection_id"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Select
              options={
                inspections.map(
                  (inspection) => ({
                    label:
                      `Inspection ${inspection.inspection_id}`,
                    value:
                      inspection.inspection_id,
                  })
                )
              }
            />
          </Form.Item>

          <Form.Item
            label="Description"
            name="description"
          >
            <Input.TextArea
              rows={4}
            />
          </Form.Item>

          <Form.Item
            label="Labour Charges"
            name="labour_charges"
          >
            <InputNumber
              min={0}
              style={{
                width: "100%",
              }}
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

export default JobCards;