import React, { useState } from 'react';
import "../styles/Dashboard.css"
import { 
  HomeOutlined, 
  UserOutlined, 
  SettingOutlined, 
  DotChartOutlined, 
  MessageOutlined, 
  FileTextOutlined, 
  QuestionCircleOutlined 
} from '@ant-design/icons';
import Assignment01 from './Assignment01';
import Assignment02 from './Assignment02';
import Assignment03 from './Assignment03';
import Assignment04 from './Assignment04';
import Assignment07 from './Assignment07';
import Assignment04_2 from './Assignment04_2';

const Dashboard = () => {
  const [activeItem, setActiveItem] = useState(null);

  const sidebarItems = [
    { icon: <HomeOutlined />, label: 'Indexer', content: <Assignment01/> },
    { icon: <UserOutlined />, label: 'Ranking', content: <Assignment02/> },
    { icon: <SettingOutlined />, label: 'Strcutured Models', content: <Assignment03/> },
    { icon: <DotChartOutlined />, label: 'Structure Guided', content: <Assignment04/>},
    { icon: <MessageOutlined />, label: 'Hypertext Model', content: <Assignment04_2/> },
    { icon: <FileTextOutlined />, label: 'SET Theoretic', content: <Assignment01/>},
    { icon: <QuestionCircleOutlined />, label: 'Neural Ranking', content: 'Help & Support' },
    { icon: <QuestionCircleOutlined />, label: 'Probabilistic Models', content: <Assignment07/> },
    // { icon: <QuestionCircleOutlined />, label: 'Belief Network', content: 'Help & Support' }
  ];

  return (
    <div className="dashboard-container">
      <div className="sidebar">
        <h2 style={{color: "white", textAlign: "center"}}>Information Retrieval</h2>
        {sidebarItems.map((item) => (
          <div 
            key={item.label}
            onClick={() => setActiveItem(item)}
            className={`sidebar-item ${activeItem === item ? 'active' : ''}`}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span className="sidebar-label">{item.label}</span>
          </div>
        ))}
      </div>

      <div className="right-panel">
        {activeItem ? (
          <div className="panel-content">
            <h2>{activeItem.label}</h2>
            <p>{activeItem.content}</p>
          </div>
        ) : (
          <div className="panel-placeholder">
            Select an option from the sidebar
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;