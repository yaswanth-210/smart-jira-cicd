def classify_task(issue):
    summary = issue["fields"]["summary"].lower()

    if "bug" in summary:
        return "high"

    return "low"