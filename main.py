from core.orchestrator import ResearchPaperOrchestrator
from output.txt_writer import save_txt
from output.json_writer import save_json
from output.pdf_writer import save_pdf


def main():
    topic = input("Enter topic: ")

    orch = ResearchPaperOrchestrator()
    result = orch.generate(topic)

    save_txt(result, "paper.txt")
    save_json(result, "paper.json")
    save_pdf(result, "paper.pdf")

    print("Files generated successfully")


if __name__ == "__main__":
    main()