// React component with Ant Design for a Storybook Hypertext Model
import React, { useState } from "react";
import { Layout, Menu, Typography, Card, Button } from "antd";

const { Sider, Content } = Layout;
const { Title, Paragraph, Link } = Typography;

const chapters = [
  {
    id: "chapter1",
    title: "Chapter 1: The Beginning",
    content: "In Chapter 1, we are introduced to the world of Eloria, a land filled with magic and mystery. The protagonist, Alaric, discovers a hidden map in his attic that hints at a long-lost treasure.",
    linkedChapters: ["chapter2", "chapter4"],
  },
  {
    id: "chapter2",
    title: "Chapter 2: The Conflict",
    content: "Alaric's journey begins, but he is soon confronted by a band of thieves who also want the treasure. A fierce battle ensues, leading to unexpected allies and foes.",
    linkedChapters: ["chapter1", "chapter3"],
  },
  {
    id: "chapter3",
    title: "Chapter 3: The Revelation",
    content: "In this chapter, Alaric discovers that the treasure is not gold but an ancient artifact capable of immense power. The revelation sets the stakes even higher.",
    linkedChapters: ["chapter2", "chapter5"],
  },
  {
    id: "chapter4",
    title: "Chapter 4: The Mentor",
    content: "Alaric meets an old wizard named Eldrin, who becomes his mentor. Eldrin reveals secrets about Alaric's lineage and his connection to the artifact.",
    linkedChapters: ["chapter1", "chapter5"],
  },
  {
    id: "chapter5",
    title: "Chapter 5: The Climax",
    content: "The final battle takes place at the ruins of an ancient castle. Alaric must make a choice that will shape the future of Eloria forever.",
    linkedChapters: ["chapter3", "chapter4"],
  },
];

const Storybook = () => {
  const [selectedChapter, setSelectedChapter] = useState(chapters[0]);
  const [history, setHistory] = useState([]);

  const handleMenuClick = (chapterId) => {
    const chapter = chapters.find((ch) => ch.id === chapterId);
    setHistory((prevHistory) => [...prevHistory, selectedChapter]);
    setSelectedChapter(chapter);
  };

  const handleBack = () => {
    if (history.length > 0) {
      const previousChapter = history[history.length - 1];
      setHistory((prevHistory) => prevHistory.slice(0, -1));
      setSelectedChapter(previousChapter);
    }
  };

  return (
    <Layout className="storybook-layout">
      <Sider className="storybook-sider" width={250}>
        <Menu
          mode="inline"
          defaultSelectedKeys={[chapters[0].id]}
          className="storybook-menu"
        >
          {chapters.map((chapter) => (
            <Menu.Item
              key={chapter.id}
              onClick={() => handleMenuClick(chapter.id)}
            >
              {chapter.title}
            </Menu.Item>
          ))}
        </Menu>
      </Sider>

      <Content className="storybook-content">
        <Card className="storybook-card">
          <Button onClick={handleBack} disabled={history.length === 0} className="back-button">
            Back
          </Button>
          <Title level={2}>{selectedChapter.title}</Title>
          <Paragraph>{selectedChapter.content}</Paragraph>

          <Title level={5}>Related Chapters</Title>
          {selectedChapter.linkedChapters.map((linkedId) => {
            const linkedChapter = chapters.find((ch) => ch.id === linkedId);
            return (
              <Paragraph key={linkedId}>
                <Link onClick={() => handleMenuClick(linkedId)}>
                  {linkedChapter.title}
                </Link>
              </Paragraph>
            );
          })}
        </Card>
      </Content>
    </Layout>
  );
};

export default Storybook;
