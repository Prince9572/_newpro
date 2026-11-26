import { Phone, Mail, MapPin, Send } from "lucide-react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { SectionHeading } from "./SectionHeading";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { contactSchema, type ContactValues } from "@/lib/schemas";

export const Contact = () => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ContactValues>({ resolver: zodResolver(contactSchema) });

  const onSubmit = async (data: ContactValues) => {
    await new Promise((r) => setTimeout(r, 600));
    toast.success(
      `Thanks ${data.name.split(" ")[0]}! We'll get back to you soon.`,
    );
    reset();
  };

  return (
    <section id="contact" className="py-20 md:py-28 gradient-section">
      <div className="container">
        <SectionHeading
          eyebrow="Get in Touch"
          title={
            <>
              Let's Plan Your <span className="gradient-text">Take-Off</span>
            </>
          }
          subtitle="Visit our campus, call us, or drop a message — we usually respond within an hour."
        />

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Info */}
          <div className="reveal space-y-4">
            {[
              {
                icon: Phone,
                title: "Phone",
                lines: [
                  "+91 95255 60025",
                  "+91 87098 90856",
                  "+91 96933 70775",
                ],
              },
              {
                icon: Mail,
                title: "Email",
                lines: [
                  "skyspeak550@gmail.com",
                  "admissions@skyspeakacademy.com",
                ],
              },
              {
                icon: MapPin,
                title: "Address",
                lines: [
                  "1E ,Niket Anand Complex - 1st Floor",
                  "Jagdeo Path Opposite Panna Lal",
                  "Pillar No.10",
                  "Patna-800014",
                ],
              },
            ].map((item) => (
              <div
                key={item.title}
                className="glass rounded-2xl p-6 flex gap-4 items-start hover:shadow-[var(--shadow-elegant)] transition-shadow"
              >
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-secondary to-primary-glow flex items-center justify-center shrink-0">
                  <item.icon className="w-5 h-5 text-primary-foreground" />
                </div>
                <div>
                  <h3 className="font-display text-lg font-bold text-primary mb-1">
                    {item.title}
                  </h3>
                  {item.lines.map((l) => (
                    <p key={l} className="text-sm text-muted-foreground">
                      {l}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Form */}
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="reveal glass rounded-3xl p-8 space-y-4"
          >
            <h3 className="font-display text-2xl font-bold text-primary mb-2">
              Send us a message
            </h3>

            <div>
              <Label htmlFor="c-name">Full Name</Label>
              <Input
                id="c-name"
                {...register("name")}
                placeholder="Your name"
                className="mt-1.5"
              />
              {errors.name && (
                <p className="text-xs text-destructive mt-1">
                  {errors.name.message}
                </p>
              )}
            </div>
            <div>
              <Label htmlFor="c-email">Email</Label>
              <Input
                id="c-email"
                type="email"
                {...register("email")}
                placeholder="you@email.com"
                className="mt-1.5"
              />
              {errors.email && (
                <p className="text-xs text-destructive mt-1">
                  {errors.email.message}
                </p>
              )}
            </div>
            <div>
              <Label htmlFor="c-msg">Message</Label>
              <Textarea
                id="c-msg"
                rows={4}
                {...register("message")}
                placeholder="How can we help?"
                className="mt-1.5"
              />
              {errors.message && (
                <p className="text-xs text-destructive mt-1">
                  {errors.message.message}
                </p>
              )}
            </div>

            <Button
              type="submit"
              disabled={isSubmitting}
              className="btn-shine w-full bg-accent text-accent-foreground hover:bg-accent/90 shadow-[var(--shadow-gold)] h-12"
            >
              {isSubmitting ? (
                "Sending..."
              ) : (
                <>
                  Send Message <Send className="ml-2 w-4 h-4" />
                </>
              )}
            </Button>
          </form>
        </div>
      </div>
    </section>
  );
};
