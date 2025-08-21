import Image from "next/image";
import Link from "next/link";
import { EXTERNAL_LINKS, SITE_CONFIG } from "@/lib/constants";

interface SocialLink {
  href: string;
  label: string;
  icon: string;
  alt: string;
}

const socialLinks: SocialLink[] = [
  {
    href: EXTERNAL_LINKS.github,
    label: "GitHub",
    icon: "/img/github.svg",
    alt: "GitHub",
  },
  {
    href: EXTERNAL_LINKS.twitter,
    label: "X (Twitter)",
    icon: "/img/x.svg",
    alt: "X",
  },
  {
    href: EXTERNAL_LINKS.telegram,
    label: "Telegram",
    icon: "/img/tg.svg",
    alt: "Telegram",
  },
];

export default function Navbar() {
  return (
    <nav
      className="m-auto h-14 w-full max-w-screen-xl px-6"
      aria-label="Main navigation"
    >
      <div className="flex h-full items-center justify-between">
        <Link
          href="/"
          className="group flex cursor-pointer font-mono text-xl font-semibold tracking-wider"
          aria-label={`Home - ${SITE_CONFIG.name}`}
        >
          <span className="flex flex-col">
            <span className="group-hover:text-primary transition-all ease-in-out">
              LEE
            </span>
            <span className="bg-primary h-[2px] transition-all ease-in-out group-hover:bg-white" />
          </span>
          <span className="flex flex-col">
            <span className="text-primary transition-all ease-in-out group-hover:text-white">
              WAN
            </span>
            <span className="group-hover:bg-primary h-[2px] bg-white transition-all ease-in-out" />
          </span>
        </Link>

        <ul className="flex items-center gap-4" role="list">
          {socialLinks.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={link.label}
                className="block opacity-70 transition-opacity hover:opacity-100 focus:opacity-100"
              >
                <Image
                  src={link.icon}
                  alt={link.alt}
                  width={24}
                  height={24}
                  className="brightness-0 invert"
                  priority
                />
              </a>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}
