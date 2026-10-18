"""
AI Research Paper Generator Agent
Uses xAI Grok API (OpenAI-compatible) with agentic pipeline:
  Web Research → Source Extraction → Paper Writer → Citation Formatter → PDF/TXT Output
"""

import os
import json
import time
import re
import argparse
from datetime import datetime
from openai import OpenAI

# ── Config ─────────────────────────────────────────────────────────────────
XAI_API_KEY  = os.getenv("XAI_API_KEY", "YOUR_XAI_API_KEY_HERE")
GROK_MODEL   = "grok-3"          # swap to grok-4 / grok-3-mini as needed
MAX_TOKENS   = 8000
TEMPERATURE  = 0.3

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")


# ═══════════════════════════════════════════════════════════════════════════
# AGENT BASE
# ═══════════════════════════════════════════════════════════════════════════
class Agent:
    def __init__(self, name: str, system_prompt: str):
        self.name   = name
        self.system = system_prompt

    def run(self, user_message: str, max_tokens: int = MAX_TOKENS) -> str:
        print(f"\n[{self.name}] ⚙  Running...")
        response = client.chat.completions.create(
            model       = GROK_MODEL,
            max_tokens  = max_tokens,
            temperature = TEMPERATURE,
            messages    = [
                {"role": "system",  "content": self.system},
                {"role": "user",    "content": user_message},
            ],
        )
        result = response.choices[0].message.content
        print(f"[{self.name}] ✓  Done ({len(result)} chars)")
        return result


# ═══════════════════════════════════════════════════════════════════════════
# AGENT 1 – WEB RESEARCH PLANNER
#   Produces a structured research plan + simulated live-search queries
# ═══════════════════════════════════════════════════════════════════════════
RESEARCH_PLANNER_PROMPT = """
You are an expert academic research planner.
Given a research topic, produce:
1. A concise research overview (2–3 sentences).
2. 6–8 targeted web-search queries that would surface authoritative sources.
3. Key sub-topics / dimensions to explore.
4. The best academic databases / journals for this field.

Return ONLY valid JSON in this exact schema:
{
  "overview": "...",
  "search_queries": ["query1", ...],
  "sub_topics": ["topic1", ...],
  "databases": ["db1", ...]
}
"""

# ═══════════════════════════════════════════════════════════════════════════
# AGENT 2 – SOURCE EXTRACTOR
#   Simulates finding, evaluating and summarising sources (cloud-only)
# ═══════════════════════════════════════════════════════════════════════════
SOURCE_EXTRACTOR_PROMPT = """
You are an expert research librarian and source analyst.
Given a research topic + search queries, generate 8–10 high-quality, realistic
academic / authoritative sources that WOULD be found by those queries.

For each source produce:
- A realistic title, authors, year, journal/publisher
- A detailed 150-word abstract summary
- Key findings (3 bullet points)
- Relevance score 1–10
- Citation in APA format

Return ONLY valid JSON in this exact schema:
{
  "sources": [
    {
      "id": "S1",
      "title": "...",
      "authors": ["Author A", "Author B"],
      "year": 2023,
      "journal": "...",
      "url": "https://...",
      "abstract": "...",
      "key_findings": ["...", "...", "..."],
      "relevance_score": 9,
      "apa_citation": "..."
    }
  ]
}
"""

# ═══════════════════════════════════════════════════════════════════════════
# AGENT 3 – RESEARCH PAPER WRITER
# ═══════════════════════════════════════════════════════════════════════════
PAPER_WRITER_PROMPT = """
You are a senior academic researcher and scientific writer.
Write a full, publication-quality research paper based on the provided
topic, research plan, and extracted sources.

Structure (use these exact section headers):
  ABSTRACT
  1. INTRODUCTION
  2. LITERATURE REVIEW
  3. METHODOLOGY / THEORETICAL FRAMEWORK
  4. RESULTS AND DISCUSSION
  5. FUTURE DIRECTIONS
  6. CONCLUSION
  REFERENCES

Requirements:
- Academic tone, third-person, formal register
- 2 500 – 3 500 words
- Cite sources inline as (Author, Year) where relevant
- Each section: substantive, evidence-based paragraphs
- No bullet lists in the paper body – full prose only
- REFERENCES section: numbered APA entries
"""

# ═══════════════════════════════════════════════════════════════════════════
# AGENT 4 – QUALITY REVIEWER
# ═══════════════════════════════════════════════════════════════════════════
QUALITY_REVIEWER_PROMPT = """
You are a peer-review editor at a top-tier academic journal.
Review the supplied research paper and return a JSON report:
{
  "overall_score": <1-10>,
  "clarity_score": <1-10>,
  "depth_score": <1-10>,
  "citation_score": <1-10>,
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "suggestions": ["...", "..."],
  "verdict": "Accept | Minor Revision | Major Revision"
}
Return ONLY valid JSON – no other text.
"""

# ═══════════════════════════════════════════════════════════════════════════
# AGENT 5 – CITATION FORMATTER
# ═══════════════════════════════════════════════════════════════════════════
CITATION_FORMATTER_PROMPT = """
You are an expert academic citation specialist.
Given a list of sources, format them in APA 7th edition, MLA 9th edition,
and Chicago 17th edition.

Return ONLY valid JSON:
{
  "apa":     ["formatted citation 1", ...],
  "mla":     ["formatted citation 1", ...],
  "chicago": ["formatted citation 1", ...]
}
"""


# ═══════════════════════════════════════════════════════════════════════════
# PIPELINE ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════
class ResearchPaperOrchestrator:

    def __init__(self):
        self.planner   = Agent("ResearchPlanner",   RESEARCH_PLANNER_PROMPT)
        self.extractor = Agent("SourceExtractor",   SOURCE_EXTRACTOR_PROMPT)
        self.writer    = Agent("PaperWriter",        PAPER_WRITER_PROMPT)
        self.reviewer  = Agent("QualityReviewer",   QUALITY_REVIEWER_PROMPT)
        self.formatter = Agent("CitationFormatter", CITATION_FORMATTER_PROMPT)

    # ── helpers ─────────────────────────────────────────────────────────
    @staticmethod
    def _parse_json(raw: str) -> dict:
        """Strip markdown fences then parse JSON."""
        clean = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()
        return json.loads(clean)

    # ── step 1 ───────────────────────────────────────────────────────────
    def step_plan(self, topic: str) -> dict:
        raw  = self.planner.run(f"Research topic: {topic}")
        data = self._parse_json(raw)
        print(f"  → Sub-topics: {', '.join(data.get('sub_topics', []))}")
        return data

    # ── step 2 ───────────────────────────────────────────────────────────
    def step_extract(self, topic: str, plan: dict) -> dict:
        prompt = (
            f"Topic: {topic}\n\n"
            f"Research overview: {plan['overview']}\n\n"
            f"Search queries:\n" +
            "\n".join(f"  - {q}" for q in plan["search_queries"])
        )
        raw  = self.extractor.run(prompt, max_tokens=6000)
        data = self._parse_json(raw)
        print(f"  → Sources found: {len(data.get('sources', []))}")
        return data

    # ── step 3 ───────────────────────────────────────────────────────────
    def step_write(self, topic: str, plan: dict, sources: dict) -> str:
        sources_text = "\n\n".join(
            f"[{s['id']}] {s['title']} ({s['year']}) – {s['authors'][0] if s['authors'] else 'Unknown'}\n"
            f"Abstract: {s['abstract']}\n"
            f"Key findings: {'; '.join(s['key_findings'])}"
            for s in sources.get("sources", [])
        )
        prompt = (
            f"TOPIC: {topic}\n\n"
            f"RESEARCH PLAN:\n{json.dumps(plan, indent=2)}\n\n"
            f"SOURCES:\n{sources_text}"
        )
        paper = self.writer.run(prompt, max_tokens=MAX_TOKENS)
        wc    = len(paper.split())
        print(f"  → Paper word count ≈ {wc}")
        return paper

    # ── step 4 ───────────────────────────────────────────────────────────
    def step_review(self, paper: str) -> dict:
        raw    = self.reviewer.run(paper[:6000], max_tokens=1000)
        review = self._parse_json(raw)
        score  = review.get("overall_score", "N/A")
        print(f"  → Quality score: {score}/10  |  Verdict: {review.get('verdict','?')}")
        return review

    # ── step 5 ───────────────────────────────────────────────────────────
    def step_format_citations(self, sources: dict) -> dict:
        src_list = json.dumps(
            [{"title": s["title"], "authors": s["authors"],
              "year":  s["year"],  "journal": s["journal"],
              "url":   s.get("url", "")}
             for s in sources.get("sources", [])],
            indent=2
        )
        raw  = self.formatter.run(src_list, max_tokens=3000)
        data = self._parse_json(raw)
        print(f"  → APA citations formatted: {len(data.get('apa', []))}")
        return data

    # ── MAIN RUN ─────────────────────────────────────────────────────────
    def generate(self, topic: str) -> dict:
        print("\n" + "═"*60)
        print(f"  AI RESEARCH PAPER AGENT  |  {datetime.now():%Y-%m-%d %H:%M}")
        print(f"  Topic: {topic}")
        print("═"*60)

        t0 = time.time()

        print("\n[1/5] Planning research...")
        plan = self.step_plan(topic)

        print("\n[2/5] Extracting sources...")
        sources = self.step_extract(topic, plan)

        print("\n[3/5] Writing paper...")
        paper = self.step_write(topic, plan, sources)

        print("\n[4/5] Peer review...")
        review = self.step_review(paper)

        print("\n[5/5] Formatting citations...")
        citations = self.step_format_citations(sources)

        elapsed = time.time() - t0
        print(f"\n✓ Pipeline complete in {elapsed:.1f}s")

        return {
            "topic":      topic,
            "timestamp":  datetime.now().isoformat(),
            "plan":       plan,
            "sources":    sources,
            "paper":      paper,
            "review":     review,
            "citations":  citations,
            "metadata": {
                "model":        GROK_MODEL,
                "elapsed_sec":  round(elapsed, 2),
                "word_count":   len(paper.split()),
            }
        }


# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT WRITERS
# ═══════════════════════════════════════════════════════════════════════════
def save_txt(result: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"RESEARCH PAPER\nGenerated: {result['timestamp']}\n")
        f.write(f"Topic: {result['topic']}\n")
        f.write("="*70 + "\n\n")
        f.write(result["paper"])
        f.write("\n\n" + "="*70 + "\n")
        f.write("PEER REVIEW SUMMARY\n")
        rev = result["review"]
        f.write(f"Score: {rev.get('overall_score')}/10  |  Verdict: {rev.get('verdict')}\n")
        f.write("Strengths:\n" + "\n".join(f"  • {s}" for s in rev.get("strengths", [])))
        f.write("\nSuggestions:\n" + "\n".join(f"  • {s}" for s in rev.get("suggestions", [])))
        f.write("\n\n" + "="*70 + "\n")
        f.write("CITATIONS (APA 7th)\n")
        for i, c in enumerate(result["citations"].get("apa", []), 1):
            f.write(f"[{i}] {c}\n")
    print(f"  ✓ TXT saved → {path}")


def save_pdf(result: dict, path: str):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
        )
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

        doc    = SimpleDocTemplate(path, pagesize=letter,
                                   leftMargin=1.2*inch, rightMargin=1.2*inch,
                                   topMargin=1*inch,    bottomMargin=1*inch)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle("MyTitle",
                                     parent    = styles["Title"],
                                     fontSize  = 18,
                                     spaceAfter= 6,
                                     alignment = TA_CENTER)
        subtitle_style = ParagraphStyle("SubTitle",
                                        parent    = styles["Normal"],
                                        fontSize  = 10,
                                        textColor = colors.grey,
                                        alignment = TA_CENTER,
                                        spaceAfter= 20)
        h1_style = ParagraphStyle("H1",
                                  parent    = styles["Heading1"],
                                  fontSize  = 13,
                                  spaceBefore=14,
                                  spaceAfter= 4,
                                  textColor = colors.HexColor("#1a237e"))
        body_style = ParagraphStyle("Body",
                                    parent     = styles["Normal"],
                                    fontSize   = 11,
                                    leading    = 16,
                                    spaceAfter = 8,
                                    alignment  = TA_JUSTIFY)
        review_style = ParagraphStyle("Review",
                                      parent    = styles["Normal"],
                                      fontSize  = 10,
                                      backColor = colors.HexColor("#f5f5f5"),
                                      borderPad = 4,
                                      spaceAfter= 6)
        cite_style = ParagraphStyle("Cite",
                                    parent    = styles["Normal"],
                                    fontSize  = 9,
                                    leading   = 13,
                                    spaceAfter= 5,
                                    textColor = colors.HexColor("#333333"))

        story = []

        # ── Title page ──────────────────────────────────────────────────
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(result["topic"], title_style))
        story.append(Paragraph(
            f"AI-Generated Research Paper  •  {result['timestamp'][:10]}  •  Model: {result['metadata']['model']}",
            subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1,
                                color=colors.HexColor("#1a237e")))
        story.append(Spacer(1, 0.2*inch))

        # ── Paper body ──────────────────────────────────────────────────
        for line in result["paper"].split("\n"):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 6))
            elif re.match(r"^\d+\.\s+[A-Z]", line) or line.isupper():
                story.append(Paragraph(line, h1_style))
            else:
                safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(safe, body_style))

        # ── Peer review ─────────────────────────────────────────────────
        story.append(PageBreak())
        story.append(Paragraph("PEER REVIEW REPORT", h1_style))
        rev = result["review"]
        story.append(Paragraph(
            f"<b>Overall Score:</b> {rev.get('overall_score')}/10  |  "
            f"<b>Clarity:</b> {rev.get('clarity_score')}/10  |  "
            f"<b>Depth:</b> {rev.get('depth_score')}/10  |  "
            f"<b>Verdict:</b> {rev.get('verdict')}",
            review_style))
        for title, key in [("Strengths", "strengths"), ("Suggestions", "suggestions")]:
            story.append(Paragraph(f"<b>{title}:</b>", body_style))
            for item in rev.get(key, []):
                safe = item.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                story.append(Paragraph(f"• {safe}", body_style))

        # ── Citations ───────────────────────────────────────────────────
        story.append(PageBreak())
        story.append(Paragraph("CITATIONS (APA 7th Edition)", h1_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        story.append(Spacer(1, 8))
        for i, c in enumerate(result["citations"].get("apa", []), 1):
            safe = c.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            story.append(Paragraph(f"[{i}]  {safe}", cite_style))

        doc.build(story)
        print(f"  ✓ PDF saved → {path}")

    except ImportError:
        print("  ⚠  reportlab not installed – PDF skipped (run: pip install reportlab)")


def save_json(result: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"  ✓ JSON saved → {path}")


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="AI Research Paper Generator (Grok/xAI)")
    parser.add_argument("topic",   help="Research topic to investigate")
    parser.add_argument("--out",   default="output", help="Output directory (default: output)")
    parser.add_argument("--pdf",   action="store_true", help="Also generate PDF")
    parser.add_argument("--json",  action="store_true", help="Also save raw JSON")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    safe_name = re.sub(r"[^\w\-]", "_", args.topic)[:60]
    ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
    base      = os.path.join(args.out, f"{safe_name}_{ts}")

    orch   = ResearchPaperOrchestrator()
    result = orch.generate(args.topic)

    print("\n[Output] Saving files...")
    save_txt(result, f"{base}.txt")
    if args.pdf:
        save_pdf(result, f"{base}.pdf")
    if args.json:
        save_json(result, f"{base}.json")

    print(f"\n{'═'*60}")
    print(f"  DONE  |  Word count: {result['metadata']['word_count']}")
    print(f"  Time : {result['metadata']['elapsed_sec']}s")
    print(f"  Score: {result['review'].get('overall_score')}/10  {result['review'].get('verdict')}")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()