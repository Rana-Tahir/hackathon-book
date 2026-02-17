import React, { useState, useEffect, useCallback } from 'react';

interface TextSelectionProps {
  onTextSelected: (text: string) => void;
}

export default function TextSelection({ onTextSelected }: TextSelectionProps) {
  const [tooltip, setTooltip] = useState<{
    visible: boolean;
    x: number;
    y: number;
    text: string;
  }>({ visible: false, x: 0, y: 0, text: '' });

  const handleMouseUp = useCallback(() => {
    const selection = window.getSelection();
    const text = selection?.toString().trim();

    if (!text || text.length < 10) {
      setTooltip((prev) => ({ ...prev, visible: false }));
      return;
    }

    const range = selection?.getRangeAt(0);
    if (!range) return;

    const rect = range.getBoundingClientRect();
    setTooltip({
      visible: true,
      x: rect.left + rect.width / 2,
      y: rect.top - 8 + window.scrollY,
      text,
    });
  }, []);

  const handleClick = useCallback(() => {
    // Small delay to avoid clearing tooltip on the button click itself
    setTimeout(() => {
      const selection = window.getSelection();
      if (!selection?.toString().trim()) {
        setTooltip((prev) => ({ ...prev, visible: false }));
      }
    }, 200);
  }, []);

  useEffect(() => {
    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('click', handleClick);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('click', handleClick);
    };
  }, [handleMouseUp, handleClick]);

  const handleAsk = () => {
    onTextSelected(tooltip.text);
    setTooltip({ visible: false, x: 0, y: 0, text: '' });
    window.getSelection()?.removeAllRanges();
  };

  if (!tooltip.visible) return null;

  return (
    <button
      onClick={handleAsk}
      style={{
        position: 'absolute',
        left: tooltip.x,
        top: tooltip.y,
        transform: 'translate(-50%, -100%)',
        background: 'var(--ifm-color-primary)',
        color: '#fff',
        border: 'none',
        borderRadius: '6px',
        padding: '6px 12px',
        fontSize: '13px',
        fontWeight: 600,
        cursor: 'pointer',
        boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
        zIndex: 1200,
        whiteSpace: 'nowrap',
      }}
    >
      Ask about this
    </button>
  );
}
