from flask import Flask, jsonify
from jira_service import get_issues
from github_service import trigger_workflow

app = Flask(__name__)

@app.route("/tasks")
def tasks():
    data = get_issues()
    issues = data.get("issues") or data.get("values") or []

    result = []

    for issue in issues:
        summary = issue.get("fields", {}).get("summary", "No Title")
        workflow = "high" if "bug" in summary.lower() else "low"

        workflow_file = "high-priority.yml" if workflow == "high" else "low-priority.yml"
        trigger_workflow(workflow_file)

        result.append({
            "id": issue.get("key", issue.get("id", "N/A")),
            "title": summary,
            "workflow": workflow
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)