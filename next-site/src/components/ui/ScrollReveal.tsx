'use client';

import { useEffect, useRef, type ReactNode } from 'react';

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
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          el.classList.add('revealed');
          observer.unobserve(el);
        }
      },
      { rootMargin: margin, threshold: 0 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [margin]);

  const Tag = as;

  return (
    <Tag
      ref={ref as never}
      data-reveal={direction}
      style={delay ? { transitionDelay: `${delay}s` } : undefined}
      className={className}
      {...rest}
    >
      {children}
    </Tag>
  );
}
