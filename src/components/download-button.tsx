import { cn } from "@/lib/utils";

interface DownloadButtonProps {
  href: string;
  children: React.ReactNode;
  className?: string;
}

export default function DownloadButton({
  href,
  children,
  className,
}: DownloadButtonProps) {
  return (
    <a
      href={href}
      target="_blank"
      className={cn(
        `bg-primary/10 text-primary ring-primary/30 hover:bg-primary/20 hover:ring-primary/50 focus:ring-primary/50 inline-flex items-center gap-2 rounded-md px-4 py-2 font-mono text-sm ring-1 transition-all focus:ring-2 focus:outline-none`,
        className,
      )}
      aria-label="Download CV PDF"
    >
      <svg
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="7 10 12 15 17 10" />
        <line x1="12" y1="15" x2="12" y2="3" />
      </svg>
      {children}
    </a>
  );
}
