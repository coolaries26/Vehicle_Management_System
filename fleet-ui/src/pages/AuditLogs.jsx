import {
  useEffect,
  useState,
} from "react";

import {
  Card,
  Table,
  Tag,
  Typography,
  Input,
  Space,
} from "antd";

import SearchToolbar
  from "../components/SearchToolbar";

import tablePagination
  from "../utils/tablePagination";

import {
  getAuditLogs,
} from "../services/auditService";

const { Title } =
  Typography;

const AuditLogs = () => {

  const [auditLogs,
    setAuditLogs] =
    useState([]);

  const [loading,
    setLoading] =
    useState(false);

  const [searchText,
    setSearchText] =
    useState("");

  const [statusFilter,
    setStatusFilter] =
    useState("ALL");

  const loadAuditLogs =
    async () => {

      try {

        setLoading(true);

        const data =
          await getAuditLogs();

        setAuditLogs(data);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);
      }
    };

  useEffect(() => {
    loadAuditLogs();
  }, []);

  const filteredLogs =
    auditLogs.filter(
      (log) => {

        return (

          log.table_name
            ?.toLowerCase()
            .includes(
              searchText.toLowerCase()
            )

          ||

          log.operation
            ?.toLowerCase()
            .includes(
              searchText.toLowerCase()
            )

          ||

          log.record_id
            ?.toLowerCase()
            .includes(
              searchText.toLowerCase()
            )
        );
      }
    );

  const columns = [

    {
      title:
        "Audit ID",

      dataIndex:
        "audit_id",
    },

    {
      title:
        "Schema",

      dataIndex:
        "schema_name",
    },

    {
      title:
        "Table",

      dataIndex:
        "table_name",
    },

    {
      title:
        "Record ID",

      dataIndex:
        "record_id",
    },

    {
      title:
        "Operation",

      render:
        (_, record) => {

          const colorMap = {
            INSERT:
              "green",

            UPDATE:
              "blue",

            DELETE:
              "red",
          };

          return (
            <Tag
              color={
                colorMap[
                  record.operation
                ]
              }
            >
              {
                record.operation
              }
            </Tag>
          );
        },
    },

    {
      title:
        "Changed At",

      dataIndex:
        "changed_at",
    },

    {
      title:
        "Old Data",

      render:
        (_, record) => (

          <pre
            style={{
              maxWidth: 300,
              overflow: "auto",
            }}
          >
            {
              JSON.stringify(
                record.old_data,
                null,
                2
              )
            }
          </pre>
        ),
    },

    {
      title:
        "New Data",

      render:
        (_, record) => (

          <pre
            style={{
              maxWidth: 300,
              overflow: "auto",
            }}
          >
            {
              JSON.stringify(
                record.new_data,
                null,
                2
              )
            }
          </pre>
        ),
    },

  ];

  return (
    <>
      <Title level={3}>
        Audit Logs
      </Title>

      <Space
        style={{
          marginBottom: 16,
        }}
      >
        <Input
          allowClear
          placeholder=
            "Search Audit Logs"
          value={
            searchText
          }
          onChange={(e) =>
            setSearchText(
              e.target.value
            )
          }
          style={{
            width: 300,
          }}
        />
      </Space>

      <Card>

        <Table
          rowKey="audit_id"
          loading={loading}
          columns={columns}
          dataSource={
            filteredLogs
          }
          pagination={
            tablePagination
          }
          scroll={{
            x: 2500,
            y: 700,
          }}
        />

      </Card>
    </>
  );
};

export default AuditLogs;