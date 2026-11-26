import { useNavigate } from "react-router-dom";
import { ArrowUpRight } from "lucide-react";
import { SectionHeading } from "./SectionHeading";
import airhostess from "@/assets/course-airhostess.jpg";
import groundstaff from "@/assets/course-groundstaff.jpg";
import personality from "@/assets/course-personality.jpg";
import english from "@/assets/course-english.jpg";
import interview from "@/assets/course-interview.jpg";
import travel from "@/assets/course-travel.jpg";

const courses = [
  {
    title: "Air Hostess Training",
    img: airhostess,
    blurb: "Cabin crew grooming, in-flight service, safety.",
  },
  {
    title: "Ground Staff Training",
    img: groundstaff,
    blurb: "Airport operations, ramp handling, customer service & ticketing.",
  },
  {
    title: "Personality Development",
    img: personality,
    blurb: "Body language, etiquette, confidence & professional grooming.",
  },
  {
    title: "Spoken English Classes",
    img: english,
    blurb: "Fluency, accent neutralization, public speaking & pronunciation.",
  },
  {
    title: "Interview Preparation",
    img: interview,
    blurb: "Mock interviews, GD practice, resume building & HR rounds.",
  },
  {
    title: "Tour & Travel Management",
    img: travel,
    blurb: "Itinerary design, IATA basics & global travel operations.",
  },
];

export const Courses = () => {
  const navigate = useNavigate();
  return (
    <section id="courses" className="py-20 md:py-28 gradient-section">
      <div className="container">
        <SectionHeading
          eyebrow="Our Courses"
          title={
            <>
              Programs Designed to{" "}
              <span className="gradient-text">Take You Higher</span>
            </>
          }
          subtitle="Industry-aligned curriculum, hands-on practice, and certified trainers."
        />
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((c, i) => (
            <article
              key={c.title}
              className="reveal group relative rounded-3xl overflow-hidden bg-card shadow-[var(--shadow-glass)] hover:shadow-[var(--shadow-elegant)] transition-all duration-500 hover:-translate-y-2"
              style={{ transitionDelay: `${i * 60}ms` }}
            >
              <div className="aspect-[4/3] overflow-hidden">
                <img
                  src={c.img}
                  alt={c.title}
                  loading="lazy"
                  width={768}
                  height={768}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                />
              </div>
              <div className="p-6">
                <h3 className="font-display text-xl font-bold text-primary mb-2">
                  {c.title}
                </h3>
                <p className="text-sm text-muted-foreground mb-4">{c.blurb}</p>
                <button
                  onClick={() => navigate("/enroll")}
                  className="inline-flex items-center gap-1 text-sm font-semibold text-secondary hover:text-accent transition-colors"
                >
                  Enroll <ArrowUpRight className="w-4 h-4" />
                </button>
              </div>
              <div className="absolute top-4 right-4 glass px-3 py-1 rounded-full text-xs font-semibold text-primary">
                Certified
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
};
