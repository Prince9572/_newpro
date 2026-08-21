import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Search",
  description: "Search and discover music, movies, series, and podcasts.",
};

export default function SearchLayout({ children }: LayoutProps<"/search">) {
  return children;
}
