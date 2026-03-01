import React, { useState } from 'react';
import ChatBot from '../components/ChatBot';
import TextSelection from '../components/ChatBot/TextSelection';

interface Props {
  children: React.ReactNode;
}

export default function Root({ children }: Props) {
  const [selectedText, setSelectedText] = useState<string | undefined>();

  // Derive chapter/module from current URL path
  const getPageContext = () => {
    if (typeof window === 'undefined') return { chapter: undefined, module: undefined };

    const path = window.location.pathname;
    const moduleMatch = path.match(/module-(\d)/);
    const module = moduleMatch ? parseInt(moduleMatch[1], 10) : undefined;

    // Use path segment as chapter identifier
    const segments = path.split('/').filter(Boolean);
    const chapter = segments.length > 0 ? segments.join('/') : undefined;

    return { chapter, module };
  };

  const { chapter, module } = getPageContext();

  return (
    <>
      {children}
      <TextSelection onTextSelected={(text) => setSelectedText(text)} />
      <ChatBot
        currentChapter={chapter}
        currentModule={module}
        selectedText={selectedText}
        onClearSelection={() => setSelectedText(undefined)}
      />
    </>
  );
}
