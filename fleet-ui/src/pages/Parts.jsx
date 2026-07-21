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
  getParts,
  createPart,
  updatePart,
  deactivatePart,
} from "../services/partService";

const { Title } =
  Typography;

const Parts = () => {

  const [parts, setParts] =
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

  const loadParts =
    async () => {

      try {

        setLoading(true);

        const data =
          await getParts();

        setParts(data);

      } catch (error) {

        console.error(error);

        message.error(
          "Failed to load parts"
        );

      } finally {

        setLoading(false);
      }
    };

  useEffect(() => {
    loadParts();
  }, []);

  const openCreateModal =
    () => {

      setEditingPart(
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

      setEditingPart(
        record
      );

      form.setFieldsValue({
        part_code:
          record.part_code,

        part_name:
          record.part_name,

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

          await updatePart(
            editingPart.part_id,
            values
          );

          message.success(
            "Part updated successfully"
          );

        } else {

          await createPart(
            values
          );

          message.success(
            "Part created successfully"
          );
        }

        setModalOpen(false);

        form.resetFields();

        await loadParts();

      } catch (error) {

        console.error(error);

        message.error(
          "Operation failed"
        );
      }
    };

  const handleDeactivate =
    async (
      partId
    ) => {

      try {

        await deactivatePart(
          partId
        );

        message.success(
          "Part deactivated"
        );

        await loadParts();

      } catch (error) {

        console.error(error);

        message.error(
          "Deactivate failed"
        );
      }
    };

  const filteredParts =
    parts.filter(
      (part) => {

        const matchesSearch =

          (
            part.part_code
              ?.toLowerCase()
              .includes(
                searchText
                  .toLowerCase()
              )

            ||

            part.part_name
              ?.toLowerCase()
              .includes(
                searchText
                  .toLowerCase()
              )

            ||

            String(
              part.part_id
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

            part.active_flag
            === true
          )

          ||

          (
            statusFilter ===
            "INACTIVE"

            &&

            part.active_flag
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
        "Part ID",

      dataIndex:
        "part_id",
    },

    {
      title:
        "Part Code",

      dataIndex:
        "part_code",
    },

    {
      title:
        "Part Name",

      dataIndex:
        "part_name",
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
                "Deactivate Part?"
              onConfirm={() =>
                handleDeactivate(
                  record.part_id
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
        Part Master
      </Title>

      <SearchToolbar
        searchText={searchText}
        setSearchText={setSearchText}
        statusFilter={statusFilter}
        setStatusFilter={
          setStatusFilter
        }
        onRefresh={loadParts}
        onAdd={openCreateModal}
        searchPlaceholder="Search Part"
        addLabel="Add Part"
      />

      <div
        style={{
          marginBottom: 12,
          fontWeight: "bold",
        }}
      >
        Total Parts:
        {" "}
        {
          filteredParts.length
        }
      </div>

      <Card>

        <Table
          rowKey="part_id"
          loading={loading}
          columns={columns}
          dataSource={
            filteredParts
          }
          pagination={
            tablePagination
          }
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
            label="Part Code"
            name="part_code"
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Part Name"
            name="part_name"
            rules={[
              {
                required: true,
                message:
                  "Part Name is required",
              },
            ]}
          >
            <Input />
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

export default Parts;