from flask import Flask, jsonify
from jira_service import get_issues
from priority_engine import classify_task

app = Flask(__name__)

@app.route("/debug")
def debug():
    return jsonify(get_issues())

@app.route("/tasks")
def tasks():
    data = get_issues()

    # Find the list of issues regardless of Jira response shape
    issues = data.get("issues") or data.get("values") or data.get("results") or []

    result = []
    for issue in issues:
        fields = issue.get("fields", {})
        summary = (
            fields.get("summary")
            or issue.get("summary")
            or issue.get("name")
            or "No Title"
        )

        result.append({
            "id": issue.get("key") or issue.get("id") or "N/A",
            "title": summary,
            "workflow": "high" if "bug" in summary.lower() else "low"
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)