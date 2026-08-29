import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Profile",
  description: "Customize your VibeBox experience and preferences.",
};

export default function ProfileLayout({ children }: LayoutProps<"/profile">) {
  return children;
}
