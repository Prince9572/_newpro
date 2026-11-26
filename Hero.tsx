import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowRight, Plane, Sparkles } from "lucide-react";
import { toast } from "sonner";
import heroImg from "@/assets/hero-aviation.jpg";

export const Hero = () => {
  const navigate = useNavigate();
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden gradient-hero pt-20">
      {/* Background image */}
      <div className="absolute inset-0">
        <img
          src={heroImg}
          alt="Professional cabin crew at sunrise airport"
          width={1920}
          height={1080}
          className="w-full h-full object-cover opacity-40"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-primary/90 via-primary/60 to-transparent" />
      </div>

      {/* Floating decorations */}
      <div className="absolute top-24 left-10 w-32 h-32 rounded-full bg-secondary/30 blur-3xl animate-float-slow" />
      <div className="absolute bottom-20 right-10 w-48 h-48 rounded-full bg-accent/20 blur-3xl animate-float" />
      <Plane className="hidden md:block absolute top-1/3 right-[10%] w-10 h-10 text-white/40 -rotate-45 animate-drift" />

      <div className="container relative z-10 grid md:grid-cols-2 gap-10 items-center py-16">
        <div className="text-primary-foreground animate-fade-in-up">
          <div className="inline-flex items-center gap-2 glass-dark px-4 py-2 rounded-full text-sm mb-6">
            <Sparkles className="w-4 h-4 text-accent" />
            India's Premium Aviation Training Institute
          </div>
          <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold leading-tight mb-6">
            Fly High with{" "}
            <span className="gradient-text">Professional Training</span>
          </h1>
          <p className="text-base md:text-lg text-primary-foreground/85 mb-8 max-w-xl">
            Launch your career in aviation, hospitality, and global travel with
            industry-certified courses, expert trainers, and 100% placement
            assistance.
          </p>
          <div className="flex flex-wrap gap-4">
            <Button
              size="lg"
              onClick={() => navigate("/enroll")}
              className="btn-shine bg-accent text-accent-foreground hover:bg-accent/90 shadow-[var(--shadow-gold)] text-base px-8 h-12"
            >
              Enroll Now <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() =>
                toast.info("Login coming soon — submit an enquiry!")
              }
              className="glass border-white/40 text-primary-foreground hover:bg-white/20 hover:text-primary-foreground text-base px-8 h-12"
            >
              Login
            </Button>
          </div>

          <div className="mt-12 grid grid-cols-3 gap-6 max-w-md">
            {[{ n: "95%", l: "Job Assistance" }].map((s) => (
              <div key={s.l} className="text-center">
                <div className="font-display text-2xl md:text-3xl font-bold text-accent">
                  {s.n}
                </div>
                <div className="text-xs md:text-sm text-primary-foreground/75">
                  {s.l}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right glass card */}
        <div className="hidden md:block animate-scale-in">
          <div className="glass rounded-3xl p-2 shadow-[var(--shadow-elegant)]">
            <img
              src={heroImg}
              alt="Cabin crew training"
              width={800}
              height={800}
              className="w-full h-[480px] object-cover rounded-2xl"
            />
          </div>
        </div>
      </div>
    </section>
  );
};
