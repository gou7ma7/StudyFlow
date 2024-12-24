import React from 'react';
import { List, Card } from 'antd';

interface BlogPost {
  id: string;
  title: string;
  description: string;
}

const BlogList: React.FC = () => {
  return (
    <Card title="Blog Posts">
      <List<BlogPost>
        itemLayout="vertical"
        pagination={{
          pageSize: 10,
        }}
        dataSource={[]}
        renderItem={(item: BlogPost) => (
          <List.Item>
            <List.Item.Meta
              title={item.title}
              description={item.description}
            />
          </List.Item>
        )}
      />
    </Card>
  );
};

export default BlogList; 