from tools.pdf_reader import extract_text_from_pdf

from tools.section_parser import split_into_sections

from agents.agent_loop import run_agent

from tools.summary_formatter import format_discharge_summary

from tools.exporter import export_summary


pdf_path = "data/patient.pdf"

pages = extract_text_from_pdf(pdf_path)

combined_text = "\n".join(pages)

sections = split_into_sections(combined_text)

summary, trace = run_agent(sections)


# Export summary AFTER it has been created
file_path = export_summary(summary)

print(f"\nSaved to: {file_path}")


print("\nAGENT TRACE:\n")

for step in trace:

    print(step)


print("\nFINAL SUMMARY:\n")

formatted_summary = format_discharge_summary(summary)

print(formatted_summary)