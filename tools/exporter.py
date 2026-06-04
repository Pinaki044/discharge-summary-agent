
def export_summary(summary, filename="outputs/summary.txt"):

    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(summary.model_dump()))

    return filename