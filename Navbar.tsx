import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Menu, X, Plane } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

const links = [
  { href: "#courses", label: "Courses" },
  { href: "#why", label: "Why Us" },
  { href: "#highlights", label: "Highlights" },
  { href: "#contact", label: "Contact" },
];

export const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
        scrolled ? "glass shadow-md" : "bg-transparent"
      }`}
    >
      <nav className="container flex items-center justify-between h-16 md:h-20">
        <Link to="/" className="flex items-center gap-2 group">
          <span
            className={`p-2 rounded-xl ${scrolled ? "bg-primary text-primary-foreground" : "glass-dark text-primary-foreground"}`}
          >
            {/* <Plane className="w-5 h-5 -rotate-45 transition-transform group-hover:rotate-0" /> */}
            <img
              src="/logo.jpg"
              alt="SkySpeak Academy"
              className="h-10 w-auto"
            />
          </span>
          <span
            className={`font-display text-xl md:text-2xl font-bold ${scrolled ? "text-primary" : "text-primary-foreground"}`}
          >
            Skyspeak <span className="gradient-text">Academy</span>
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-8">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className={`text-sm font-medium transition-colors hover:text-accent ${
                scrolled ? "text-foreground" : "text-primary-foreground"
              }`}
            >
              {l.label}
            </a>
          ))}
        </div>

        <div className="hidden md:flex items-center gap-3">
          <Button
            variant="ghost"
            onClick={() => toast.info("Login coming soon — please enquire!")}
            className={
              scrolled
                ? ""
                : "text-primary-foreground hover:bg-white/10 hover:text-primary-foreground"
            }
          >
            Login
          </Button>
          <Button
            onClick={() => navigate("/enroll")}
            className="btn-shine bg-accent text-accent-foreground hover:bg-accent/90 shadow-[var(--shadow-gold)]"
          >
            Enroll Now
          </Button>
        </div>

        <button
          onClick={() => setOpen(!open)}
          className={`md:hidden p-2 rounded-lg ${scrolled ? "text-foreground" : "text-primary-foreground"}`}
          aria-label="Toggle menu"
        >
          {open ? <X /> : <Menu />}
        </button>
      </nav>

      {open && (
        <div className="md:hidden glass border-t border-white/30 animate-fade-in-up">
          <div className="container py-4 flex flex-col gap-3">
            {links.map((l) => (
              <a
                key={l.href}
                href={l.href}
                onClick={() => setOpen(false)}
                className="py-2 text-foreground font-medium"
              >
                {l.label}
              </a>
            ))}
            <div className="flex gap-2 pt-2">
              <Button
                variant="outline"
                className="flex-1"
                onClick={() => {
                  toast.info("Login coming soon — please enquire!");
                  setOpen(false);
                }}
              >
                Login
              </Button>
              <Button
                className="flex-1 bg-accent text-accent-foreground hover:bg-accent/90"
                onClick={() => {
                  navigate("/enroll");
                  setOpen(false);
                }}
              >
                Enroll
              </Button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};
