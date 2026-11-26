import { Plane, Facebook, Instagram, Linkedin, Youtube } from "lucide-react";
import { Link } from "react-router-dom";

export const Footer = () => (
  <footer className="bg-primary text-primary-foreground py-12">
    <div className="container grid md:grid-cols-3 gap-8">
      <div>
        {/* <Link to="/" className="flex items-center gap-2 mb-4">
          <span className="p-2 rounded-xl bg-accent text-accent-foreground">
            <Plane className="w-5 h-5 -rotate-45" />
          </span>
          <span className="font-display text-xl font-bold">
            Skyspeak <span className="gradient-text">Academy</span>
          </span>
        </Link> */}
        <Link to="/" className="flex items-center gap-2 mb-4">
          <img
            src="/logo.jpg"
            alt="Skyspeak Logo"
            className="w-10 h-10 object-contain"
          />
          <span className="font-display text-xl font-bold">
            Skyspeak <span className="gradient-text">Academy</span>
          </span>
        </Link>
        <p className="text-sm text-primary-foreground/70 max-w-xs">
          ✨ Transform Your Future in Aviation ✈️ Industry-Ready Training | 100%
          Job Assistance
        </p>
      </div>

      <div>
        <h4 className="font-display font-bold mb-3">Quick Links</h4>
        <ul className="space-y-2 text-sm text-primary-foreground/80">
          <li>
            <a href="#courses" className="hover:text-accent transition-colors">
              Courses
            </a>
          </li>
          <li>
            <a href="#why" className="hover:text-accent transition-colors">
              Why Choose Us
            </a>
          </li>
          <li>
            <a
              href="#highlights"
              className="hover:text-accent transition-colors"
            >
              Highlights
            </a>
          </li>
          <li>
            <a href="#contact" className="hover:text-accent transition-colors">
              Contact
            </a>
          </li>
        </ul>
      </div>

      <div>
        <h4 className="font-display font-bold mb-3">Follow Us</h4>
        <div className="flex gap-3">
          {[Facebook, Instagram, Linkedin, Youtube].map((I, i) => (
            <a
              key={i}
              href="#"
              aria-label="Social link"
              className="w-10 h-10 rounded-full glass-dark flex items-center justify-center hover:bg-accent hover:text-accent-foreground transition-colors"
            >
              <I className="w-4 h-4" />
            </a>
          ))}
        </div>
        <p className="text-xs text-primary-foreground/60 mt-6">
          © {new Date().getFullYear()} Skyspeak Academy. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
);
