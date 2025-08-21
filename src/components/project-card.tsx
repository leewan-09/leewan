import Image from "next/image";
import { type ProjectMeta } from "@/lib/projects";

interface ProjectCardProps {
  project: ProjectMeta;
}

export default function ProjectCard({ project }: ProjectCardProps) {
  return (
    <article
      className="group hover:border-primary/30 relative overflow-hidden rounded-lg border border-zinc-800/50 bg-zinc-900/50 p-6 transition-all duration-300 hover:bg-zinc-900/70"
      role="article"
      aria-labelledby={`project-${project.id}`}
    >
      <h3
        id={`project-${project.id}`}
        className="group-hover:text-primary mb-3 text-xl font-semibold text-zinc-100 transition-colors"
      >
        {project.title}
      </h3>

      <p className="mb-4 line-clamp-3 text-sm leading-relaxed text-zinc-400">
        {project.description}
      </p>

      <div className="mb-4 flex flex-wrap gap-2">
        {project.tags.slice(0, 4).map((tag) => (
          <span
            key={tag}
            className="group-hover:bg-primary/10 group-hover:text-primary rounded-full bg-zinc-800/70 px-3 py-1 font-mono text-xs text-zinc-300 ring-1 ring-zinc-700/50 transition-colors"
          >
            {tag}
          </span>
        ))}
        {project.tags.length > 4 && (
          <span className="rounded-full bg-zinc-800/70 px-3 py-1 text-xs text-zinc-400 ring-1 ring-zinc-700/50">
            +{project.tags.length - 4}
          </span>
        )}
      </div>

      <div className="flex gap-3">
        {project.github && (
          <a
            href={project.github}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:bg-primary/10 hover:text-primary hover:ring-primary/30 flex items-center gap-2 rounded-md bg-zinc-800/50 px-3 py-2 font-mono text-xs text-zinc-400 ring-1 ring-zinc-700/50 transition-all"
            aria-label={`View ${project.title} source code on GitHub`}
          >
            <Image
              src="/images/github.svg"
              alt=""
              width={14}
              height={14}
              className="opacity-70 brightness-0 invert transition-opacity group-hover:opacity-100"
            />
            Code
          </a>
        )}
        {project.demo && (
          <a
            href={project.demo}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:bg-primary/10 hover:text-primary hover:ring-primary/30 flex items-center gap-2 rounded-md bg-zinc-800/50 px-3 py-2 font-mono text-xs text-zinc-400 ring-1 ring-zinc-700/50 transition-all"
            aria-label={`View ${project.title} live demo`}
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="opacity-70 transition-opacity group-hover:opacity-100"
              aria-hidden="true"
            >
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
            Demo
          </a>
        )}
      </div>
    </article>
  );
}
