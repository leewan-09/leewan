import projectsData from "@/data/projects.json";

export interface ProjectMeta {
  id: string;
  title: string;
  description: string;
  date: string;
  tags: string[];
  github?: string | null;
  demo?: string | null;
  featured: boolean;
  order_number: number;
}

export function getAllProjects(): ProjectMeta[] {
  return projectsData.projects.sort((a, b) => {
    // Featured projects first
    if (a.featured && !b.featured) return -1;
    if (!a.featured && b.featured) return 1;

    // Then by order_number
    return a.order_number - b.order_number;
  });
}
