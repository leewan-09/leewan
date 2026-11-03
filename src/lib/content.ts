import barfume from "@/assets/chart/card-barfume.svg?url";
import basvaaru from "@/assets/chart/card-basvaaru.svg?url";
import furaaqu from "@/assets/chart/card-furaaqu.svg?url";
import pdf from "@/assets/chart/card-pdf.svg?url";
import taxflow from "@/assets/chart/card-taxflow.svg?url";
import yoosuf from "@/assets/chart/card-yoosuf.svg?url";

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
  /** Key of this card's chart and labels in cards.json. */
  chart: "furaaqu" | "barfume" | "yoosuf" | "taxflow" | "basvaaru" | "pdf";
  /** A real chart of where the project works. */
  art: string;
  artAlt: string;
  href?: string;
  /** Where the card's link goes, as shown on the card. */
  destination?: string;
}

/** Each card opens something a visitor can actually see. Other work goes in ALSO_BUILT. */
export const PROJECTS: Project[] = [
  {
    name: "Furaaqu",
    summary: "Booking for a speedboat line up north",
    chart: "furaaqu",
    art: furaaqu,
    artAlt: "Chart of Furaaqu's line of 15 stops, from Malé north to Shaviyani",
    href: "https://furaaqu.com",
    destination: "furaaqu.com",
  },
  {
    name: "Barfume",
    summary: "Fragrance store in Malé",
    chart: "barfume",
    art: barfume,
    artAlt: "Chart of Malé and Hulhumalé, with every mapped building lit",
    href: "https://barfumemv.com",
    destination: "barfumemv.com",
  },
  {
    name: "Yoosuf Speed",
    summary: "Booking for a speedboat line to Baa",
    chart: "yoosuf",
    art: yoosuf,
    artAlt: "Chart of Yoosuf Speed's line from Malé to four islands in Baa",
    href: "https://yoosufspeed.com",
    destination: "yoosufspeed.com",
  },
  {
    name: "TaxFlow",
    summary: "Invoice photos into tax statements",
    chart: "taxflow",
    art: taxflow,
    artAlt: "Chart of the whole country, with a line from every atoll to Malé",
    href: "https://taxflow.run",
    destination: "taxflow.run",
  },
  {
    name: "Basvaaru",
    summary: "Platform behind a Dhivehi learning app",
    chart: "basvaaru",
    art: basvaaru,
    artAlt: "Chart of the whole country, with its settled islands lit",
    href: "https://play.google.com/store/apps/details?id=com.thestudypoint.basvaaru",
    destination: "Google Play",
  },
  {
    name: "PDF service",
    summary: "100,000+ tickets, invoices and résumés",
    chart: "pdf",
    art: pdf,
    artAlt:
      "Chart of the Furaaqu and Yoosuf Speed lines, both leaving from Malé",
    href: "https://github.com/leewan-09/html-to-pdf",
    destination: "GitHub",
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
