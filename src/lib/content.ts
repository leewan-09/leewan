import addu from "@/assets/chart/atoll-addu.svg?url";
import ari from "@/assets/chart/atoll-ari.svg?url";
import kaafu from "@/assets/chart/atoll-kaafu.svg?url";
import laamu from "@/assets/chart/atoll-laamu.svg?url";
import noonu from "@/assets/chart/atoll-noonu.svg?url";
import raa from "@/assets/chart/atoll-raa.svg?url";

export const SITE = {
  name: "Leewan",
  fullName: "Ahmed Leevan",
  title: "Leewan, full-stack engineer in the Maldives",
  description:
    "I build software for a country of 1,192 islands. Senior full-stack engineer in Malé, backend first, with six years of building for the web and mobile.",
  jobTitle: "Senior full-stack engineer",
  company: "Kreating",
} as const;

export const LINKS = {
  telegram: "https://t.me/toor09",
  github: "https://github.com/leewan-09",
  x: "https://x.com/leewan98",
  kreating: "https://kreating.co",
  cv: "/Ahmed-Leevan-CV.pdf",
  osm: "https://www.openstreetmap.org/copyright",
} as const;

export interface Project {
  name: string;
  summary: string;
  /** Decorative atoll crop. It doesn't show where the project is. */
  art: string;
  href?: string;
}

/** Each card opens something a visitor can actually see. Other work goes in ALSO_BUILT. */
export const PROJECTS: Project[] = [
  {
    name: "Furaaqu",
    summary: "Speedboat ticketing for daily routes",
    art: noonu,
    href: "https://furaaqu.com",
  },
  {
    name: "Barfume",
    summary: "Fragrance store and catalogue",
    art: kaafu,
    href: "https://barfumemv.com",
  },
  {
    name: "Yoosuf Speed",
    summary: "Speedboat booking platform",
    art: raa,
    href: "https://yoosufspeed.com",
  },
  {
    name: "TaxFlow",
    summary: "Invoice photos into tax statements",
    art: ari,
    href: "https://taxflow.run",
  },
  {
    name: "Basvaaru",
    summary: "Platform behind a Dhivehi learning app",
    art: laamu,
    href: "https://play.google.com/store/apps/details?id=com.thestudypoint.basvaaru",
  },
  {
    name: "PDF service",
    summary: "Rust HTML-to-PDF service",
    art: addu,
    href: "https://github.com/leewan-09/html-to-pdf",
  },
];

export const ALSO_BUILT =
  "Also built: Hukit, Kreating HQ, Naalu, Dhivehi Maps, Dhivehi Calendar, Wellness Raagu and a ride-hailing API.";

export const PRINCIPLES = [
  {
    title: "Data model first",
    line: "The schema decides what the product can become.",
  },
  {
    title: "Let the database say no",
    line: "Rules live where no feature can forget them.",
  },
  {
    title: "Built to keep running",
    line: "Launch is the start. The real test comes after.",
  },
];

export const TOOLS = [
  { title: "Backend", list: "NestJS, tRPC, Hono" },
  { title: "Data", list: "PostgreSQL, Prisma, Drizzle, Redis" },
  { title: "Frontend", list: "Next.js, TanStack Start, Tailwind CSS" },
  { title: "Mobile and ops", list: "Expo, Flutter, Docker, GitHub Actions" },
];
