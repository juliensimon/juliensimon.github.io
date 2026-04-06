'use client';

import { useCallback, useEffect, useRef, type ReactNode } from 'react';

type Direction = 'up' | 'down' | 'left' | 'right' | 'scale';

interface ScrollRevealProps {
  children: ReactNode;
  direction?: Direction;
  delay?: number;
  margin?: string;
  className?: string;
  as?: 'div' | 'a';
  href?: string;
  target?: string;
  rel?: string;
}

export default function ScrollReveal({
  children,
  direction = 'up',
  delay = 0,
  margin = '0px',
  className = '',
  as = 'div',
  ...rest
}: ScrollRevealProps) {
  const elRef = useRef<HTMLElement | null>(null);
  const observerRef = useRef<IntersectionObserver | null>(null);

  // Mark <html> as JS-ready so CSS can safely hide [data-reveal] elements.
  // Without JS (crawlers), content stays visible (opacity: 1).
  useEffect(() => {
    document.documentElement.classList.add('js-reveal-ready');
  }, []);

  useEffect(() => {
    observerRef.current = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observerRef.current?.unobserve(entry.target);
        }
      },
      { rootMargin: margin, threshold: 0 }
    );
    if (elRef.current) observerRef.current.observe(elRef.current);
    return () => observerRef.current?.disconnect();
  }, [margin]);

  const refCallback = useCallback((node: HTMLElement | null) => {
    elRef.current = node;
    if (node && observerRef.current) observerRef.current.observe(node);
  }, []);

  const Tag = as;

  return (
    <Tag
      ref={refCallback}
      data-reveal={direction}
      style={delay ? { transitionDelay: `${delay}s` } : undefined}
      className={className}
      {...rest}
    >
      {children}
    </Tag>
  );
}
