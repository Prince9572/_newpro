import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { Sparkles } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { enquirySchema, type EnquiryValues } from "@/lib/schemas";

export const EnquiryModal = () => {
  const [open, setOpen] = useState(false);
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<EnquiryValues>({ resolver: zodResolver(enquirySchema) });

  useEffect(() => {
    if (sessionStorage.getItem("skyspeak_enq_seen")) return;
    const t = setTimeout(() => {
      setOpen(true);
      sessionStorage.setItem("skyspeak_enq_seen", "1");
    }, 4000);
    return () => clearTimeout(t);
  }, []);

  const onSubmit = async (data: EnquiryValues) => {
    await new Promise((r) => setTimeout(r, 500));
    toast.success(`Thanks ${data.name.split(" ")[0]}! Our team will call you shortly.`);
    reset();
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="sm:max-w-md p-0 overflow-hidden border-0 bg-transparent shadow-none">
        <div className="glass rounded-3xl p-6 md:p-8">
          <DialogHeader className="text-left">
            <div className="inline-flex items-center gap-2 text-accent text-xs font-semibold uppercase tracking-widest mb-2">
              <Sparkles className="w-4 h-4" /> Quick Enquiry
            </div>
            <DialogTitle className="font-display text-2xl text-primary">
              Get a free <span className="gradient-text">demo class</span>
            </DialogTitle>
            <DialogDescription>
              Drop your details — we'll call within 30 minutes.
            </DialogDescription>
          </DialogHeader>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-3 mt-4">
            <div>
              <Label htmlFor="e-name">Name</Label>
              <Input id="e-name" {...register("name")} placeholder="Full name" className="mt-1.5 bg-white/70" />
              {errors.name && <p className="text-xs text-destructive mt-1">{errors.name.message}</p>}
            </div>
            <div>
              <Label htmlFor="e-email">Email</Label>
              <Input id="e-email" type="email" {...register("email")} placeholder="you@email.com" className="mt-1.5 bg-white/70" />
              {errors.email && <p className="text-xs text-destructive mt-1">{errors.email.message}</p>}
            </div>
            <div>
              <Label htmlFor="e-phone">Phone</Label>
              <Input id="e-phone" {...register("phone")} placeholder="10-digit mobile" className="mt-1.5 bg-white/70" />
              {errors.phone && <p className="text-xs text-destructive mt-1">{errors.phone.message}</p>}
            </div>

            <Button
              type="submit"
              disabled={isSubmitting}
              className="btn-shine w-full bg-accent text-accent-foreground hover:bg-accent/90 shadow-[var(--shadow-gold)] h-11 mt-2"
            >
              {isSubmitting ? "Submitting..." : "Submit Enquiry"}
            </Button>
          </form>
        </div>
      </DialogContent>
    </Dialog>
  );
};
