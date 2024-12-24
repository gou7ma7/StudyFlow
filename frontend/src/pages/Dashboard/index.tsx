import React from 'react';
import { Calendar, Card } from 'antd';

const Dashboard: React.FC = () => {
  return (
    <div>
      <Card title="Study Calendar">
        <Calendar />
      </Card>
    </div>
  );
};

export default Dashboard; 