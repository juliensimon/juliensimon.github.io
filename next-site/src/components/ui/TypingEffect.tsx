'use client';

import { useEffect, useState } from 'react';

interface TypingEffectProps {
  texts: string[];
  speed?: number;
  deleteSpeed?: number;
  pauseMs?: number;
}

export default function TypingEffect({
  texts,
  speed = 50,
  deleteSpeed = 30,
  pauseMs = 2000,
}: TypingEffectProps) {
  const [displayed, setDisplayed] = useState('');
  const [textIndex, setTextIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const current = texts[textIndex];

    if (!deleting && charIndex < current.length) {
      const timer = setTimeout(() => {
        setDisplayed(current.slice(0, charIndex + 1));
        setCharIndex(charIndex + 1);
      }, speed);
      return () => clearTimeout(timer);
    }

    if (!deleting && charIndex === current.length) {
      const timer = setTimeout(() => setDeleting(true), pauseMs);
      return () => clearTimeout(timer);
    }

    if (deleting && charIndex > 0) {
      const timer = setTimeout(() => {
        setDisplayed(current.slice(0, charIndex - 1));
        setCharIndex(charIndex - 1);
      }, deleteSpeed);
      return () => clearTimeout(timer);
    }

    if (deleting && charIndex === 0) {
      setDeleting(false);
      setTextIndex((textIndex + 1) % texts.length);
    }
  }, [charIndex, deleting, textIndex, texts, speed, deleteSpeed, pauseMs]);

  return (
    <span>
      {displayed}
      <span className="typing-cursor" />
    </span>
  );
}
