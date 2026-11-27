import { Check } from "lucide-react";
import { SectionHeading } from "./SectionHeading";
import bg from "@/assets/highlights-bg.jpg";

const stats = [{ n: "95%", l: "Job Assistance" }];

const points = [
  "Live mock interviews with airline HR",
  "Personality grooming labs & wardrobe coaching",
  "Resume building and LinkedIn optimization",
  "Cabin emergency & first-aid simulations",
];

export const Highlights = () => (
  <section id="highlights" className="relative py-20 md:py-28 overflow-hidden">
    <div className="absolute inset-0">
      <img
        src={bg}
        alt="Aircraft taking off at sunset"
        loading="lazy"
        width={1920}
        height={1080}
        className="w-full h-full object-cover"
      />
      <div className="absolute inset-0 bg-gradient-to-br from-primary/95 via-primary/85 to-primary/70" />
    </div>

    <div className="container relative z-10">
      <SectionHeading
        light
        eyebrow="Special Highlights"
        title={
          <>
            What Makes Skyspeak <span className="gradient-text">Different</span>
          </>
        }
        subtitle="A full-spectrum training experience designed around real airline expectations."
      />

      <div className="grid lg:grid-cols-4 gap-4 mb-12">
        {stats.map((s, i) => (
          <div
            key={s.l}
            className="reveal glass-dark rounded-2xl p-6 text-center"
            style={{ transitionDelay: `${i * 80}ms` }}
          >
            <div className="font-display text-4xl md:text-5xl font-bold gradient-text mb-1">
              {s.n}
            </div>
            <div className="text-sm text-primary-foreground/80">{s.l}</div>
          </div>
        ))}
      </div>

      <div className="reveal glass rounded-3xl p-8 md:p-10">
        <div className="grid sm:grid-cols-2 gap-4">
          {points.map((p) => (
            <div key={p} className="flex items-start gap-3">
              <span className="mt-0.5 w-6 h-6 rounded-full bg-gradient-to-br from-accent to-amber-500 flex items-center justify-center shrink-0">
                <Check className="w-4 h-4 text-accent-foreground" />
              </span>
              <span className="text-foreground font-medium">{p}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </section>
);
