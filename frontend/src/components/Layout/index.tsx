import React from 'react';
import { Layout as AntLayout, Menu } from 'antd';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { DashboardOutlined, BookOutlined } from '@ant-design/icons';

const { Header, Content, Footer } = AntLayout;

const Layout: React.FC = () => {
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: <Link to="/">Dashboard</Link>,
    },
    {
      key: '/blog',
      icon: <BookOutlined />,
      label: <Link to="/blog">Blog</Link>,
    },
  ];

  return (
    <AntLayout className="app">
      <Header>
        <div className="logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
        />
      </Header>
      <Content className="content">
        <Outlet />
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        Study Flow ©{new Date().getFullYear()}
      </Footer>
    </AntLayout>
  );
};

export default Layout; 