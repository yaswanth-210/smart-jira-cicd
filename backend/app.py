from flask import Flask, jsonify
from jira_service import get_issues
from github_service import trigger_workflow

app = Flask(__name__)

# Priority Classification Function
def classify_priority(title):

    title = title.lower()

    if "critical" in title or "failure" in title or "urgent" in title:
        return "high"

    elif "feature" in title or "improvement" in title:
        return "medium"

    else:
        return "low"


@app.route("/tasks")
def tasks():

    data = get_issues()

    issues = data.get("issues") or data.get("values") or []

    result = []

    for issue in issues:

        summary = issue.get("fields", {}).get("summary", "No Title")

        # Get Priority
        workflow = classify_priority(summary)

        # Select Workflow File
        if workflow == "high":
            workflow_file = "high-priority.yml"

        elif workflow == "medium":
            workflow_file = "medium-priority.yml"

        else:
            workflow_file = "low-priority.yml"

        # Trigger GitHub Workflow
        trigger_workflow(workflow_file)

        result.append({
            "id": issue.get("key", issue.get("id", "N/A")),
            "title": summary,
            "workflow": workflow
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)