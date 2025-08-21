import Image from "next/image";
import { EXTERNAL_LINKS, SITE_CONFIG } from "@/lib/constants";
import { getAllProjects } from "@/lib/projects";
import ProjectGrid from "@/components/project-grid";
import Link from "next/link";
import DownloadButton from "@/components/download-button";

export default function HomePage() {
  const projects = getAllProjects();

  return (
    <>
      <section
        id="me"
        className="flex min-h-[calc(100vh-56px)] flex-col justify-center pb-16"
        aria-label="Introduction"
      >
        <header className="flex flex-col md:w-3/4">
          <div
            className="mb-6 h-4 w-full rotate-180 bg-[url('/images/wavy-line.svg')] bg-no-repeat opacity-80"
            role="presentation"
            aria-hidden="true"
          />
          <p className="flex max-w-3xl items-end text-lg font-normal text-white/70">
            Hello
            <Image
              src="/images/wave.gif"
              alt="Waving hand"
              width={30}
              height={30}
              className="ml-1"
              priority
              unoptimized
            />
            ,
            <span className="ml-1">
              My name is{" "}
              <strong className="text-primary font-mono font-semibold">
                {SITE_CONFIG.name}
              </strong>
              .
            </span>
          </p>
        </header>

        <h1 className="relative my-3 max-w-3xl text-4xl font-bold tracking-tight text-zinc-100 sm:text-6xl">
          {SITE_CONFIG.title}.
          <span
            className="text-primary/20 absolute top-[-6px] left-1 -z-10 my-3 max-w-3xl text-4xl font-bold tracking-tight sm:text-6xl"
            aria-hidden="true"
          >
            {SITE_CONFIG.title}.
          </span>
        </h1>

        <article className="relative md:w-3/4">
          <p className="max-w-3xl text-base font-normal text-zinc-400">
            I&apos;m a{" "}
            <span className="text-primary font-mono">full-stack</span> engineer
            with a passion for{" "}
            <span className="text-primary font-mono">backend development</span>.
            Currently working as a{" "}
            <span className="text-primary font-mono">
              {SITE_CONFIG.currentRole}
            </span>
            {SITE_CONFIG.company && (
              <>
                {" "}
                at{" "}
                <span className="text-primary font-mono">
                  {SITE_CONFIG.company}
                </span>
              </>
            )}{" "}
            with{" "}
            <span className="text-primary font-mono">
              {SITE_CONFIG.experience}
            </span>{" "}
            of experience. Check out my
            <Link
              href="/#projects"
              className="text-primary font-mono hover:underline focus:underline"
            >
              {" "}
              projects below{" "}
            </Link>
            or{" "}
            <a
              href={EXTERNAL_LINKS.telegram}
              className="text-primary font-mono hover:underline focus:underline"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Contact me on Telegram"
            >
              contact
            </a>{" "}
            me.
          </p>

          <div className="mt-6 sm:hidden">
            <DownloadButton href={SITE_CONFIG.cvLink}>
              Download CV
            </DownloadButton>
          </div>

          <div
            className="absolute right-10 h-11 w-36 translate-y-full rotate-180 bg-[url('/images/cricle-cross.svg')] bg-no-repeat opacity-50"
            role="presentation"
            aria-hidden="true"
          />
        </article>

        <div
          className="mt-6 h-4 w-full bg-[url('/images/wavy-line.svg')] bg-no-repeat"
          role="presentation"
          aria-hidden="true"
        />
      </section>

      <section id="projects" className="py-16" aria-label="Projects">
        <div className="mb-8">
          <h2 className="text-3xl font-bold tracking-tight text-zinc-100 sm:text-4xl">
            Projects
          </h2>
          <p className="mt-2 text-zinc-400">
            A collection of projects I&apos;ve worked on and experiments
            I&apos;ve built.
          </p>
        </div>
        <ProjectGrid projects={projects} />
      </section>
    </>
  );
}
