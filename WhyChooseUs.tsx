import { Briefcase, Sparkles, PlayCircle, GraduationCap } from "lucide-react";
import { SectionHeading } from "./SectionHeading";

const features = [
  { icon: Briefcase, title: "100% Job Assistance", desc: "Dedicated placement cell with airline & travel partners." },
  { icon: Sparkles, title: "Grooming Sessions", desc: "Personalized grooming, posture and style coaching." },
  { icon: PlayCircle, title: "Free Demo Class", desc: "Try before you enroll — book a no-obligation demo." },
  { icon: GraduationCap, title: "Experienced Trainers", desc: "Industry veterans with 10+ years of cabin & ground experience." },
];

export const WhyChooseUs = () => (
  <section id="why" className="py-20 md:py-28 bg-background">
    <div className="container">
      <SectionHeading
        eyebrow="Why Choose Us"
        title={<>Built for Your <span className="gradient-text">Career Take-off</span></>}
        subtitle="Everything you need to land your dream job in aviation and hospitality."
      />
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((f, i) => (
          <div
            key={f.title}
            className="reveal group p-7 rounded-3xl bg-card border border-border hover:border-accent transition-all duration-500 hover:-translate-y-2 hover:shadow-[var(--shadow-elegant)]"
            style={{ transitionDelay: `${i * 80}ms` }}
          >
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-secondary to-primary-glow flex items-center justify-center mb-5 group-hover:scale-110 transition-transform">
              <f.icon className="w-7 h-7 text-primary-foreground" />
            </div>
            <h3 className="font-display text-lg font-bold text-primary mb-2">{f.title}</h3>
            <p className="text-sm text-muted-foreground">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  </section>
);
