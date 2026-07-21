import {
  useEffect,
  useState,
} from "react";

import {
  Button,
  Card,
  Form,
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
} from "@ant-design/icons";

import SearchToolbar
  from "../components/SearchToolbar";

import tablePagination
  from "../utils/tablePagination";

import {
  getJobCardParts,
  createJobCardPart,
  updateJobCardPart,
  deactivateJobCardPart,
} from "../services/jobCardPartService";

import {
  getJobCards,
} from "../services/jobCardService";

import {
  getParts,
} from "../services/partService";

const { Title } =
  Typography;


const JobCardParts = () => {

const [jobCardParts,
    setJobCardParts] =
    useState([]);

  const [jobCards,
    setJobCards] =
    useState([]);

  const [parts,
    setParts] =
    useState([]);

  const [loading,
    setLoading] =
    useState(false);

  const [modalOpen,
    setModalOpen] =
    useState(false);

  const [editingPart,
    setEditingPart] =
    useState(null);

  const [searchText,
    setSearchText] =
    useState("");

  const [statusFilter,
    setStatusFilter] =
    useState("ALL");

  const [form] =
    Form.useForm();

const loadData = async () => {

  try {

    setLoading(true);

    const [
      jobCardPartData,
      jobCardData,
      partsData,
    ] = await Promise.all([
      getJobCardParts(),
      getJobCards(),
      getParts(),
    ]);

    setJobCardParts(
      jobCardPartData
    );

    setJobCards(
      jobCardData
    );

    setParts(
      partsData
    );

  } catch (error) {

    console.error(error);

    message.error(
      "Failed to load Job Card Parts"
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

      setEditingPart(
        null
      );

      form.resetFields();

      form.setFieldsValue({
        active_flag: true,
        quantity: 1,
        unit_price: 0,
      });

      setModalOpen(true);
    };

  const openEditModal =
    (record) => {

      setEditingPart(
        record
      );

      form.setFieldsValue({
        job_card_id:
          record.job_card_id,

        part_id:
          record.part_id,

        quantity:
          record.quantity,
        unit_price:
          record.unit_price,

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
          editingPart
        ) {

          await updateJobCardPart(
            editingPart.id,
            values
          );

          message.success(
            "Updated successfully"
          );

        } else {
console.log(values);
          await createJobCardPart(
            values
          );

          message.success(
            "Created successfully"
          );
        }

        setModalOpen(false);

        await loadData();

      } catch (error) {

        console.error(error);

        message.error(
          "Operation failed"
        );
      }
    };

  const handleDeactivate =
    async (id) => {

      try {

        await deactivateJobCardPart(
          id
        );

        message.success(
          "Deactivated"
        );

        await loadData();

      } catch (error) {

        message.error(
          "Deactivate failed"
        );
      }
    };

  const filteredParts =
    jobCardParts.filter(
      (record) => {

        const matchesSearch =

          String(
            record.job_card_id
          ).includes(
            searchText
          )

          ||

          String(
            record.part_id
          ).includes(
            searchText
          );

        const matchesStatus =
          statusFilter ===
          "ALL"

          ||

          (
            statusFilter ===
            "ACTIVE"
            &&
            record.active_flag
            === true
          )

          ||

          (
            statusFilter ===
            "INACTIVE"
            &&
            record.active_flag
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
        "ID",

      dataIndex:
        "id",
    },

    {
      title:
        "Job Card",

      dataIndex:
        "job_card_id",
    },

    {
      title:
        "Part",

      dataIndex:
        "part_id",
    },

    {
      title:
        "Quantity",

      dataIndex:
        "quantity",
    },
    {
      title: "Unit Price",
        
      dataIndex:
        "unit_price",
        
      render:
        (value) =>
          `₹ ${value ?? 0}`,
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
              title="Deactivate?"
              onConfirm={() =>
                handleDeactivate(
                  record.id
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
        Job Card Parts
      </Title>

      <SearchToolbar
        searchText={searchText}
        setSearchText={setSearchText}
        statusFilter={statusFilter}
        setStatusFilter={setStatusFilter}
        onRefresh={loadData}
        onAdd={openCreateModal}
        searchPlaceholder="Search Job Card Part"
        addLabel="Add Part"
      />

      <Card>

        <Table
          rowKey="id"
          loading={loading}
          columns={columns}
          dataSource={filteredParts}
          pagination={tablePagination}
          scroll={{
            x: 1200,
          }}
        />

      </Card>

      <Modal
        title={
          editingPart
            ? "Edit Part"
            : "Add Part"
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
            label="Job Card"
            name="job_card_id"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Select
              options={
                jobCards.map(
                  (jobCard) => ({
                    label:
                      `Job Card ${jobCard.job_card_id}`,
                    value:
                      jobCard.job_card_id,
                  })
                )
              }
            />
          </Form.Item>

          <Form.Item
            label="Part"
            name="part_id"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Select
              options={
                parts.map(
                  (part) => ({
                    label:
                      part.part_name,
                    value:
                      part.part_id,
                  })
                )
              }
            />
          </Form.Item>

          <Form.Item
            label="Quantity"
            name="quantity"
          >
            <InputNumber
              min={1}
              style={{
                width: "100%",
              }}
            />
          </Form.Item>
          <Form.Item
            label="Unit Price"
            name="unit_price"
            rules={[
              {
                required: true,
                message: "Unit Price is required",
              },
            ]}
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

export default JobCardParts;