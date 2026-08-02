#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path
from urllib import error, request


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def build_request_url(base_url: str, api_path: str) -> str:
    base = base_url.rstrip("/")
    path = api_path.strip()

    if base.endswith("/v1") and path.startswith("/v1/"):
        path = path[len("/v1"):]

    return base + path


def parse_streamed_response(body: str) -> dict:
    content_parts: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("data:"):
            continue
        data = stripped[5:].strip()
        if data == "[DONE]":
            continue
        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            continue

        choice = payload.get("choices", [{}])[0]
        delta = choice.get("delta", {})
        if isinstance(delta.get("content"), str):
            content_parts.append(delta["content"])

    if not content_parts:
        return {}

    return {
        "choices": [
            {
                "message": {
                    "content": "".join(content_parts)
                }
            }
        ]
    }


def call_gateway(prompt: str, base_url: str, api_key: str, model: str, api_path: str) -> dict:
    url = build_request_url(base_url, api_path)
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
    }
    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = request.Request(
        url,
        data=data,
        headers=headers,
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as response:
            body = response.read().decode("utf-8", errors="replace")
            if body.lstrip().startswith("data:"):
                parsed = parse_streamed_response(body)
                if parsed:
                    return parsed
            return json.loads(body)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gateway returned HTTP {exc.code}: {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Unable to reach gateway: {exc}") from exc


def main() -> int:
    load_dotenv(Path(".env"))

    parser = argparse.ArgumentParser(description="Test a connection to an OmniRoute-compatible LLM gateway.")
    parser.add_argument("--prompt", default="Say hello from OmniRoute in one short sentence.")
    parser.add_argument("--model", default=os.getenv("OMNIROUTE_MODEL", "gpt-4o-mini"))
    parser.add_argument("--base-url", default=os.getenv("OMNIROUTE_BASE_URL"))
    parser.add_argument("--api-key", default=os.getenv("OMNIROUTE_API_KEY", ""))
    parser.add_argument("--api-path", default=os.getenv("OMNIROUTE_API_PATH", "/chat/completions"))
    args = parser.parse_args()

    try:
        base_url = get_env("OMNIROUTE_BASE_URL", args.base_url)
        api_key = args.api_key or os.getenv("OMNIROUTE_API_KEY", "")
    except ValueError as exc:
        print(f"Setup error: {exc}", file=sys.stderr)
        print("Copy .env.example to .env and fill in the gateway values.", file=sys.stderr)
        return 1

    try:
        response = call_gateway(
            prompt=args.prompt,
            base_url=base_url,
            api_key=api_key,
            model=args.model,
            api_path=args.api_path,
        )
    except RuntimeError as exc:
        print(f"Connection error: {exc}", file=sys.stderr)
        return 1

    message = response.get("choices", [{}])[0].get("message", {}).get("content")
    print(message or json.dumps(response, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
