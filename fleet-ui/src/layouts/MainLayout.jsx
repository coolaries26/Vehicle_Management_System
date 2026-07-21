import { Layout, Menu, Typography } from "antd";
import {
  DashboardOutlined,
  CarOutlined,
  UserOutlined,
  TeamOutlined,
  ToolOutlined,
  FileTextOutlined,
  AuditOutlined,
} from "@ant-design/icons";
import { Link, Outlet, useLocation } from "react-router-dom";

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

const MainLayout = () => {
  const location = useLocation();

  const menuItems = [
    {
      key: "/",
      icon: <DashboardOutlined />,
      label: <Link to="/">Dashboard</Link>,
    },
    {
      key: "/vehicles",
      icon: <CarOutlined />,
      label: <Link to="/vehicles">Vehicles</Link>,
    },
    {
      key: "/drivers",
      icon: <UserOutlined />,
      label: <Link to="/drivers">Drivers</Link>,
    },
    {
      key: "/employees",
      icon: <TeamOutlined />,
      label: <Link to="/employees">Employees</Link>,
    },
    {
      key: "/complaints",
      icon: <FileTextOutlined />,
      label: <Link to="/complaints">Complaints</Link>,
    },
    {
      key: "/maintenance",
      icon: <ToolOutlined />,
      label: <Link to="/maintenance">Maintenance</Link>,
    },
    {
      key: "/inspections",
      icon: <ToolOutlined />,
      label: (<Link to="/inspections">Inspections</Link>),
    },
    {
      key: "/parts",
      icon: <ToolOutlined />,
      label: (<Link to="/parts">Parts</Link>),
    },
    {
      key: "/jobcards",
      icon: <ToolOutlined />,
      label: (<Link to="/jobcards">Job Cards</Link>),
    },
    {
      key: "/jobcard-parts",
      icon: <ToolOutlined />,
      label: (<Link to="/jobcardparts">Job Card Parts</Link>),
    },
    {
      key: "/checklists",
      icon: <ToolOutlined />,
      label: (<Link to="/checklists">Checklists</Link>),
    },
    {
      key: "/audit-logs",
      icon: <AuditOutlined />,
      label: (<Link to="/audit-logs">Audit Logs</Link>),
    },
  ];

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider width={240}>
        <div
          style={{
            color: "#ffffff",
            padding: "18px",
            fontSize: "20px",
            fontWeight: "bold",
          }}
        >
          FMS MVP
        </div>

        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
        />
      </Sider>

      <Layout>
        <Header
          style={{
            background: "#ffffff",
            borderBottom: "1px solid #eee",
            padding: "0 24px",
          }}
        >
          <Title level={4} style={{ marginTop: 14 }}>
            Fleet Management System
          </Title>
        </Header>

        <Content style={{ padding: 24 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;