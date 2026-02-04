interface SocialButtonProps {
  name: string;
  href: string;
}

export default function SocialButton({ name, href }: SocialButtonProps) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium
        bg-primary/10 text-primary hover:bg-primary/20
        transition-all duration-200 hover:scale-[1.03]"
    >
      {name}
    </a>
  );
}
