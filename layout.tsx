import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Discover",
  description: "Explore entertainment by mood and genre with AI-powered recommendations.",
};

export default function DiscoverLayout({ children }: LayoutProps<"/discover">) {
  return children;
}
