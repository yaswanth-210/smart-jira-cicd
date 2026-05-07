def classify_priority(title):

    title = title.lower()

    if "critical" in title or "failure" in title or "urgent" in title:
        return "high"

    elif "feature" in title or "improvement" in title:
        return "medium"

    else:
        return "low"