import { type ProjectMeta } from "@/lib/projects";
import ProjectCard from "./project-card";

interface ProjectGridProps {
  projects: ProjectMeta[];
}

export default function ProjectGrid({ projects }: ProjectGridProps) {
  if (projects.length === 0) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <p className="text-zinc-400">No projects found.</p>
      </div>
    );
  }

  return (
    <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
      {projects.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  );
}