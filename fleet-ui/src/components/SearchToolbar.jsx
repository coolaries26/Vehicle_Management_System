import {
  Button,
  Input,
  Select,
  Space,
} from "antd";

import {
  PlusOutlined,
  ReloadOutlined,
  SearchOutlined,
} from "@ant-design/icons";

const SearchToolbar = ({
  searchText,
  setSearchText,
  statusFilter,
  setStatusFilter,
  onRefresh,
  onAdd,
  searchPlaceholder,
  addLabel,
}) => {

  return (
    <Space
      wrap
      style={{
        marginBottom: 6,
        width: "100%",
        justifyContent: "space-between",
      }}
    >
    <Space>
        <Input
          allowClear
          prefix={<SearchOutlined />}
          placeholder={searchPlaceholder}
          value={searchText}
          onChange={(e) =>
            setSearchText(
              e.target.value
            )
          }
          style={{
            width: 300,
          }}
        />

        <Select
          value={statusFilter}
          onChange={setStatusFilter}
          style={{
            width: 150,
          }}
          options={[
            {
              label: "All",
              value: "ALL",
            },
            {
              label: "Active",
              value: "ACTIVE",
            },
            {
              label: "Inactive",
              value: "INACTIVE",
            },
          ]}
        />

      </Space>

      <Space>

        <Button
          icon={<ReloadOutlined />}
          onClick={onRefresh}
        >
          Refresh
        </Button>

        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={onAdd}
        >
          {addLabel}
        </Button>

      </Space>

    </Space>
  );
};

export default SearchToolbar;