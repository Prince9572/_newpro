interface Props {
  eyebrow?: string;
  title: React.ReactNode;
  subtitle?: string;
  light?: boolean;
}

export const SectionHeading = ({ eyebrow, title, subtitle, light }: Props) => (
  <div className={`text-center max-w-2xl mx-auto mb-12 reveal ${light ? "text-primary-foreground" : ""}`}>
    {eyebrow && (
      <div className={`inline-block text-xs font-semibold tracking-widest uppercase mb-3 px-3 py-1 rounded-full ${light ? "bg-white/10 text-accent" : "bg-accent/10 text-accent"}`}>
        {eyebrow}
      </div>
    )}
    <h2 className="font-display text-3xl md:text-5xl font-bold mb-4">{title}</h2>
    {subtitle && (
      <p className={`text-base md:text-lg ${light ? "text-primary-foreground/80" : "text-muted-foreground"}`}>
        {subtitle}
      </p>
    )}
  </div>
);
