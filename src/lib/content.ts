import addu from "@/assets/chart/atoll-addu.svg?url";
import ari from "@/assets/chart/atoll-ari.svg?url";
import kaafu from "@/assets/chart/atoll-kaafu.svg?url";
import laamu from "@/assets/chart/atoll-laamu.svg?url";
import noonu from "@/assets/chart/atoll-noonu.svg?url";
import raa from "@/assets/chart/atoll-raa.svg?url";

export const SITE = {
  name: "Leewan",
  title: "Leewan, full-stack engineer in the Maldives",
  description:
    "I build software for a country of 1,192 islands. Full-stack engineer, backend first, with more than five years of building for the web and mobile.",
  jobTitle: "Full-stack engineer",
  employer: "Nine Sixteen",
} as const;

export const LINKS = {
  telegram: "https://t.me/toor09",
  github: "https://github.com/leewan-09",
  x: "https://x.com/leewan98",
  cv: "https://drive.google.com/drive/folders/1obdkkB3U2eztMoiUAIwrEaTkGgwxpnyu?usp=sharing",
  osm: "https://www.openstreetmap.org/copyright",
} as const;

export interface Project {
  name: string;
  summary: string;
  /** Decorative atoll crop. It doesn't show where the project is. */
  art: string;
  href?: string;
}

export const PROJECTS: Project[] = [
  {
    name: "Furaaqu",
    summary: "Speedboat ticket booking",
    art: noonu,
    href: "https://furaaqu.com",
  },
  {
    name: "Maahdhaa4",
    summary: "Public engagement platform",
    art: kaafu,
    href: "https://maahdhaa4.com",
  },
  {
    name: "Dhivehi Maps",
    summary: "World map app in Dhivehi",
    art: laamu,
  },
  {
    name: "Silver Oasis",
    summary: "Guest house website",
    art: ari,
    href: "https://silveroasismaldives.com",
  },
  {
    name: "Apex Logistics",
    summary: "Company website",
    art: raa,
    href: "https://apexlogistics.mv",
  },
  {
    name: "NineSixteen",
    summary: "Company website",
    art: addu,
    href: "https://ninesixteen.mv",
  },
];

export const ALSO_BUILT =
  "Also built: Furaaqu Naalu, Wellness Raagu, Silversmoke, Salesco, ILM Vidhaaraa, Dhivehi Calendar and Youtu.Bio.";

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
  { title: "Backend", list: "NestJS, Express, tRPC" },
  { title: "Data", list: "PostgreSQL, Prisma, MongoDB" },
  { title: "Frontend", list: "Next.js, Nuxt, Tailwind CSS" },
  { title: "Mobile and ops", list: "Flutter, Docker, GitHub Actions" },
];
