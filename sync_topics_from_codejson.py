import json
import os
import re
import sys
import urllib.request


CODE_JSON_PATH = "code.json"
API_VERSION = "2026-03-10"


def normalize_topic(tag: str) -> str:
    topic = tag.strip().lower()
    topic = re.sub(r"[\s_]+", "-", topic)
    topic = re.sub(r"[^a-z0-9-]", "", topic)
    topic = re.sub(r"-+", "-", topic)
    topic = topic.strip("-")
    return topic


def read_code_json_tags(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    tags = data.get("tags", [])

    if not isinstance(tags, list):
        raise ValueError("code.json 'tags' field must be a list.")

    normalized_tags = []

    for tag in tags:
        if not isinstance(tag, str):
            continue

        normalized = normalize_topic(tag)

        if normalized:
            normalized_tags.append(normalized)

    return sorted(set(normalized_tags))


def update_repo_topics(repository: str, token: str, topics: list[str]) -> None:
    url = f"https://api.github.com/repos/{repository}/topics"

    payload = json.dumps({"names": topics}).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        method="PUT",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": API_VERSION,
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(request) as response:
        if response.status not in (200, 201):
            raise RuntimeError(f"GitHub API returned status {response.status}")


def main() -> None:
    repository = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN_FOR_TOPICS")

    if not repository:
        print("Missing GITHUB_REPOSITORY environment variable.", file=sys.stderr)
        sys.exit(1)

    if not token:
        print("Missing GITHUB_TOKEN_FOR_TOPICS environment variable.", file=sys.stderr)
        sys.exit(1)

    topics = read_code_json_tags(CODE_JSON_PATH)

    print(f"Syncing {len(topics)} topics from code.json:")
    print(", ".join(topics))

    update_repo_topics(repository, token, topics)

    print("Repository topics synced successfully.")


if __name__ == "__main__":
    main()
