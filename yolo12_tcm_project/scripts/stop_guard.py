from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_REQUIRED_PHRASE = "我绝对确定所有任务都已经完成且所有目标都已经达成"


def collect_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        texts: list[str] = []
        for key, item in value.items():
            texts.extend(collect_strings(key))
            texts.extend(collect_strings(item))
        return texts
    if isinstance(value, list):
        texts: list[str] = []
        for item in value:
            texts.extend(collect_strings(item))
        return texts
    return [str(value)]


def read_transcript(path: str | None, max_chars: int) -> str:
    if not path:
        return ""
    target = Path(path)
    if not target.exists() or not target.is_file():
        return ""
    try:
        text = target.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return text[-max_chars:]


def content_to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(filter(None, (content_to_text(item) for item in value)))
    if isinstance(value, dict):
        if isinstance(value.get("text"), str):
            return value["text"]
        if isinstance(value.get("content"), (str, list, dict)):
            return content_to_text(value["content"])
        if isinstance(value.get("message"), dict):
            return content_to_text(value["message"])
    return ""


def role_of(value: dict[str, Any]) -> str:
    if isinstance(value.get("role"), str):
        return value["role"]
    message = value.get("message")
    if isinstance(message, dict) and isinstance(message.get("role"), str):
        return message["role"]
    if value.get("type") == "assistant":
        return "assistant"
    return ""


def assistant_text(value: dict[str, Any]) -> str:
    message = value.get("message")
    if isinstance(message, dict):
        text = content_to_text(message.get("content"))
        if text:
            return text
    return content_to_text(value.get("content"))


def find_last_assistant_text(value: Any) -> str:
    if isinstance(value, list):
        for item in reversed(value):
            text = find_last_assistant_text(item)
            if text:
                return text
        return ""
    if isinstance(value, dict):
        if role_of(value) == "assistant":
            return assistant_text(value)
        for key in ("messages", "transcript", "conversation", "items"):
            text = find_last_assistant_text(value.get(key))
            if text:
                return text
    return ""


def read_last_assistant_from_transcript(path: str | None, max_chars: int) -> str:
    text = read_transcript(path, max_chars)
    if not text.strip():
        return ""

    last = ""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            item = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        candidate = find_last_assistant_text(item)
        if candidate:
            last = candidate
    if last:
        return last

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return ""
    return find_last_assistant_text(payload)


def decode_stdin(raw: bytes) -> str:
    if raw.count(b"\x00") > max(2, len(raw) // 8):
        for encoding in ("utf-16", "utf-16-le", "utf-16-be"):
            try:
                return raw.decode(encoding)
            except UnicodeDecodeError:
                continue
    for encoding in ("utf-8-sig", "gb18030", "mbcs"):
        try:
            return raw.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode(errors="replace")


def load_payload(raw: str) -> tuple[Any | None, list[str]]:
    if not raw.strip():
        return None, []
    try:
        payload = json.loads(raw)
        return payload, collect_strings(payload)
    except json.JSONDecodeError:
        return None, [raw]


def main() -> int:
    parser = argparse.ArgumentParser(description="Stop hook guard: block stopping until the required completion phrase appears.")
    parser.add_argument("--required-phrase", default=DEFAULT_REQUIRED_PHRASE)
    parser.add_argument("--max-transcript-chars", type=int, default=250_000)
    parser.add_argument("--text", default="", help="Optional explicit text to inspect.")
    args = parser.parse_args()

    raw = decode_stdin(sys.stdin.buffer.read())
    payload, _texts = load_payload(raw)
    texts: list[str] = []

    if args.text:
        texts.append(args.text)

    if isinstance(payload, dict):
        payload_assistant = find_last_assistant_text(payload)
        if payload_assistant:
            texts.append(payload_assistant)
        transcript_path = payload.get("transcript_path") or payload.get("transcriptPath")
        transcript_assistant = read_last_assistant_from_transcript(transcript_path, args.max_transcript_chars)
        if transcript_assistant:
            texts.append(transcript_assistant)
    elif raw.strip():
        texts.append(raw)

    corpus = "\n".join(texts)
    if args.required_phrase in corpus:
        print(json.dumps({"decision": "allow", "reason": "required completion phrase found"}, ensure_ascii=False))
        return 0

    message = (
        "StopHook blocked: 未检测到允许停止的完成短语。"
        f"必须在确实完成全部目标后输出：{args.required_phrase}"
    )
    print(message, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
