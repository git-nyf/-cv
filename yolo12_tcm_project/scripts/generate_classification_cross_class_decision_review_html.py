from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path
from typing import Any
from urllib.parse import quote

from generate_classification_cross_class_decision_table import MANUAL_FIELDS, normalize_path
from path_utils import project_root, resolve_project_path


ROOT = project_root()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def split_semicolon(value: str) -> list[str]:
    return [normalize_path(item.strip()) for item in value.split(";") if item.strip()]


def display_path(value: str) -> str:
    return str(value).replace("\\", "/")


def load_decision_table(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    payload = read_json(path)
    return {
        str(item.get("group_id")): item
        for item in payload.get("decisions", [])
        if item.get("group_id")
    }


def load_decision_csv(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    decisions: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            group_id = str(row.get("group_id", "")).strip()
            if not group_id:
                continue
            item: dict[str, Any] = {}
            for key in MANUAL_FIELDS:
                value = str(row.get(key, "")).strip()
                item[key] = split_semicolon(value) if key == "remove_relative_paths" else value
            decisions[group_id] = item
    return decisions


def merge_manual_fields(group_id: str, table: dict[str, dict[str, Any]], csv_overrides: dict[str, dict[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {
        "decision_status": "pending",
        "chosen_class": "",
        "action": "",
        "remove_relative_paths": [],
        "move_to_class": "",
        "reviewer": "",
        "reviewed_at": "",
        "decision_note": "",
    }
    if group_id in table:
        for key in MANUAL_FIELDS:
            if key in table[group_id]:
                merged[key] = table[group_id][key]
    if group_id in csv_overrides:
        for key in MANUAL_FIELDS:
            if key in csv_overrides[group_id]:
                merged[key] = csv_overrides[group_id][key]
    if isinstance(merged.get("remove_relative_paths"), str):
        merged["remove_relative_paths"] = split_semicolon(merged["remove_relative_paths"])
    else:
        merged["remove_relative_paths"] = [normalize_path(str(item)) for item in merged.get("remove_relative_paths", [])]
    return merged


def rel_url(path: Path, html_path: Path) -> str:
    try:
        relative = path.resolve().relative_to(html_path.parent.resolve())
    except ValueError:
        relative = Path(*Path(path).resolve().parts)
        try:
            relative = Path(Path(path).resolve().relative_to(ROOT.resolve()))
        except ValueError:
            return ""
    return quote(relative.as_posix(), safe="/._-()")


def project_relative(path: Path) -> str:
    try:
        return normalize_path(str(path.resolve().relative_to(ROOT.resolve())))
    except ValueError:
        return normalize_path(str(path))


def option_tags(values: list[str], selected: str, include_empty: bool = True) -> str:
    items = [""] + values if include_empty else values
    tags = []
    for value in items:
        label = value or "-"
        selected_attr = " selected" if value == selected else ""
        tags.append(f'<option value="{html.escape(value, quote=True)}"{selected_attr}>{html.escape(label)}</option>')
    return "\n".join(tags)


def row_from_group(group: dict[str, Any], manual: dict[str, Any], index: int, output: Path) -> str:
    records = group.get("records", [])
    classes = [str(item) for item in group.get("classes", [])]
    remove_paths = set(manual.get("remove_relative_paths", []))
    images = []
    checkboxes = []
    for record in records:
        image_path = Path(str(record.get("path", "")))
        src = rel_url(image_path, output)
        relative_path = display_path(normalize_path(str(record.get("relative_path", ""))))
        checked = " checked" if relative_path in remove_paths else ""
        exists_class = "ok" if record.get("exists") and image_path.exists() else "missing"
        images.append(
            f"""
            <figure class="record {exists_class}">
              <div class="image-frame">
                <img src="{src}" alt="{html.escape(relative_path, quote=True)}" loading="lazy">
              </div>
              <figcaption>
                <strong>{html.escape(str(record.get("class_name", "")))}</strong>
                <code>{html.escape(relative_path)}</code>
                <span>{html.escape(str(record.get("split", "")))} · {html.escape(str(record.get("filename", "")))} · {record.get("bytes", 0)} bytes</span>
              </figcaption>
            </figure>
            """
        )
        checkboxes.append(
            f"""
            <label class="path-check">
              <input type="checkbox" data-remove-path value="{html.escape(relative_path, quote=True)}"{checked}>
              <span>{html.escape(relative_path)}</span>
            </label>
            """
        )

    classes_text = " / ".join(classes)
    fields_payload = {
        "group_id": group.get("group_id", ""),
        "decision_status": manual.get("decision_status", "pending"),
        "chosen_class": manual.get("chosen_class", ""),
        "action": manual.get("action", ""),
        "remove_relative_paths": ";".join(display_path(path) for path in manual.get("remove_relative_paths", [])),
        "move_to_class": manual.get("move_to_class", ""),
        "reviewer": manual.get("reviewer", ""),
        "reviewed_at": manual.get("reviewed_at", ""),
        "decision_note": manual.get("decision_note", ""),
    }
    fields_json = html.escape(json.dumps(fields_payload, ensure_ascii=False), quote=True)
    image_html = "\n".join(images)
    checkbox_html = "\n".join(checkboxes)
    return f"""
    <article class="group-card" data-group-id="{html.escape(str(group.get("group_id", "")), quote=True)}" data-classes="{html.escape(classes_text, quote=True)}" data-status="{html.escape(str(manual.get("decision_status", "pending")), quote=True)}">
      <header class="group-head">
        <div>
          <span class="index">#{index:02d}</span>
          <h2>{html.escape(str(group.get("group_id", "")))}</h2>
          <p>{html.escape(classes_text)} · {group.get("record_count", len(records))} records · SHA {html.escape(str(group.get("sha256_short", "")))}</p>
        </div>
        <div class="status-pill">{html.escape(str(manual.get("decision_status", "pending")))}</div>
      </header>
      <section class="image-grid">
        {image_html}
      </section>
      <section class="decision-grid" data-fields="{fields_json}">
        <label>decision_status
          <select data-field="decision_status">
            {option_tags(["pending", "decided", "needs_expert_review", "defer"], str(manual.get("decision_status", "pending")), include_empty=False)}
          </select>
        </label>
        <label>chosen_class
          <select data-field="chosen_class">
            {option_tags(classes, str(manual.get("chosen_class", "")))}
          </select>
        </label>
        <label>action
          <select data-field="action">
            {option_tags(["keep_chosen_class_remove_others", "move_all_to_chosen_class", "keep_all_as_is", "remove_all_uncertain", "needs_expert_review"], str(manual.get("action", "")))}
          </select>
        </label>
        <label>move_to_class
          <select data-field="move_to_class">
            {option_tags(classes, str(manual.get("move_to_class", "")))}
          </select>
        </label>
        <label>reviewer
          <input data-field="reviewer" value="{html.escape(str(manual.get("reviewer", "")), quote=True)}">
        </label>
        <label>reviewed_at
          <input data-field="reviewed_at" placeholder="YYYY-MM-DD" value="{html.escape(str(manual.get("reviewed_at", "")), quote=True)}">
        </label>
        <label class="wide">remove_relative_paths
          <div class="path-list">{checkbox_html}</div>
        </label>
        <label class="wide">decision_note
          <textarea data-field="decision_note" rows="3">{html.escape(str(manual.get("decision_note", "")))}</textarea>
        </label>
      </section>
      <footer class="group-actions">
        <button type="button" data-copy-row>Copy TSV row</button>
        <button type="button" data-copy-remove>Copy remove paths</button>
        <code class="copy-state">ready</code>
      </footer>
    </article>
    """


def build_html(review_package: Path, decision_table: Path | None, decision_csv: Path | None, output: Path) -> str:
    package = read_json(review_package)
    table = load_decision_table(decision_table)
    csv_overrides = load_decision_csv(decision_csv)
    groups = package.get("groups", [])
    summary = package.get("summary", {})
    rows = [
        row_from_group(group, merge_manual_fields(str(group.get("group_id")), table, csv_overrides), index, output)
        for index, group in enumerate(groups, start=1)
    ]
    generated = {
        "groups": len(groups),
        "records": sum(len(group.get("records", [])) for group in groups),
        "review_package": project_relative(review_package),
        "decision_table": project_relative(decision_table) if decision_table else "",
        "decision_csv": project_relative(decision_csv) if decision_csv else "",
        "source_status": summary.get("status", ""),
    }
    rows_html = "\n".join(rows)
    meta_json = html.escape(json.dumps(generated, ensure_ascii=False), quote=True)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>跨类别标签冲突人工决策复核页</title>
  <style>
    :root {{
      --bg: #f6f4ee;
      --ink: #1d2520;
      --muted: #68736c;
      --line: #d7d0c2;
      --panel: #fffdf8;
      --accent: #2f6f73;
      --accent-2: #8a4d2f;
      --warn: #a23e31;
      --ok: #4d7a45;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: "Microsoft YaHei", "Segoe UI", sans-serif; }}
    header.page {{ position: sticky; top: 0; z-index: 5; background: rgba(246,244,238,.96); border-bottom: 1px solid var(--line); padding: 18px 24px; }}
    h1 {{ margin: 0 0 8px; font-size: 24px; letter-spacing: 0; }}
    .summary {{ display: flex; flex-wrap: wrap; gap: 10px; color: var(--muted); font-size: 13px; }}
    .toolbar {{ margin-top: 14px; display: grid; grid-template-columns: minmax(180px, 1fr) 180px 180px; gap: 10px; max-width: 940px; }}
    input, select, textarea, button {{ font: inherit; border: 1px solid var(--line); border-radius: 6px; background: #fff; color: var(--ink); }}
    .toolbar input, .toolbar select {{ padding: 9px 10px; }}
    main {{ padding: 22px 24px 56px; display: grid; gap: 18px; }}
    .group-card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; overflow: hidden; box-shadow: 0 10px 24px rgba(33, 28, 20, .06); }}
    .group-head {{ display: flex; justify-content: space-between; gap: 16px; padding: 16px 18px; border-bottom: 1px solid var(--line); }}
    .group-head h2 {{ margin: 0; font-size: 18px; }}
    .group-head p {{ margin: 6px 0 0; color: var(--muted); font-size: 13px; }}
    .index {{ color: var(--accent-2); font-weight: 700; font-size: 13px; }}
    .status-pill {{ align-self: start; padding: 6px 9px; border-radius: 999px; background: #e6efe8; color: var(--ok); font-size: 12px; white-space: nowrap; }}
    .image-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; padding: 16px 18px; }}
    .record {{ margin: 0; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fbfaf4; }}
    .image-frame {{ aspect-ratio: 1 / .82; display: grid; place-items: center; background: #ece6d8; }}
    .image-frame img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
    figcaption {{ display: grid; gap: 5px; padding: 10px; font-size: 12px; color: var(--muted); }}
    figcaption strong {{ color: var(--ink); font-size: 14px; }}
    code {{ font-family: "Cascadia Mono", Consolas, monospace; font-size: 12px; white-space: normal; word-break: break-all; }}
    .decision-grid {{ padding: 0 18px 16px; display: grid; grid-template-columns: repeat(3, minmax(180px, 1fr)); gap: 12px; }}
    label {{ display: grid; gap: 6px; font-size: 12px; color: var(--muted); }}
    label > input, label > select, label > textarea {{ width: 100%; padding: 8px 9px; }}
    .wide {{ grid-column: 1 / -1; }}
    .path-list {{ display: grid; gap: 6px; border: 1px solid var(--line); border-radius: 6px; background: #fff; padding: 8px; }}
    .path-check {{ display: flex; align-items: flex-start; gap: 8px; font-size: 12px; }}
    .group-actions {{ display: flex; gap: 10px; align-items: center; padding: 12px 18px 16px; border-top: 1px solid var(--line); }}
    button {{ padding: 8px 11px; cursor: pointer; background: var(--accent); color: #fff; border-color: var(--accent); }}
    button:hover {{ filter: brightness(.96); }}
    .copy-state {{ color: var(--muted); }}
    .hidden {{ display: none; }}
    @media (max-width: 760px) {{
      header.page {{ position: static; padding: 14px; }}
      main {{ padding: 14px; }}
      .toolbar, .decision-grid {{ grid-template-columns: 1fr; }}
      .group-head {{ display: grid; }}
    }}
  </style>
</head>
<body data-meta="{meta_json}">
  <header class="page">
    <h1>跨类别标签冲突人工决策复核页</h1>
    <div class="summary">
      <span>{generated["groups"]} 组冲突</span>
      <span>{generated["records"]} 条记录</span>
      <span>来源: {html.escape(generated["review_package"])}</span>
      <span>只辅助人工填写，不自动修改 CSV 或数据集</span>
    </div>
    <div class="toolbar">
      <input id="search" placeholder="搜索 group、类别、路径">
      <select id="statusFilter">
        <option value="">全部状态</option>
        <option value="pending">pending</option>
        <option value="decided">decided</option>
        <option value="needs_expert_review">needs_expert_review</option>
        <option value="defer">defer</option>
      </select>
      <select id="classFilter">
        <option value="">全部类别组合</option>
      </select>
    </div>
  </header>
  <main id="groups">
    {rows_html}
  </main>
  <script>
    const cards = Array.from(document.querySelectorAll('.group-card'));
    const search = document.querySelector('#search');
    const statusFilter = document.querySelector('#statusFilter');
    const classFilter = document.querySelector('#classFilter');
    const classes = [...new Set(cards.map(card => card.dataset.classes).filter(Boolean))].sort();
    for (const item of classes) {{
      const option = document.createElement('option');
      option.value = item;
      option.textContent = item;
      classFilter.appendChild(option);
    }}
    function removePaths(card) {{
      return Array.from(card.querySelectorAll('[data-remove-path]:checked')).map(item => item.value).join(';');
    }}
    function fieldValue(card, field) {{
      const input = card.querySelector(`[data-field="${{field}}"]`);
      return input ? input.value.trim() : '';
    }}
    function tsvRow(card) {{
      return [
        card.dataset.groupId,
        fieldValue(card, 'decision_status'),
        fieldValue(card, 'chosen_class'),
        fieldValue(card, 'action'),
        removePaths(card),
        fieldValue(card, 'move_to_class'),
        fieldValue(card, 'reviewer'),
        fieldValue(card, 'reviewed_at'),
        fieldValue(card, 'decision_note')
      ].join('\\t');
    }}
    async function copyText(text, state) {{
      try {{
        await navigator.clipboard.writeText(text);
        state.textContent = 'copied';
      }} catch (err) {{
        state.textContent = text;
      }}
    }}
    function applyFilters() {{
      const needle = search.value.trim().toLowerCase();
      const status = statusFilter.value;
      const klass = classFilter.value;
      for (const card of cards) {{
        const text = card.textContent.toLowerCase();
        const visible = (!needle || text.includes(needle)) && (!status || card.dataset.status === status) && (!klass || card.dataset.classes === klass);
        card.classList.toggle('hidden', !visible);
      }}
    }}
    document.addEventListener('click', event => {{
      const card = event.target.closest('.group-card');
      if (!card) return;
      const state = card.querySelector('.copy-state');
      if (event.target.matches('[data-copy-row]')) copyText(tsvRow(card), state);
      if (event.target.matches('[data-copy-remove]')) copyText(removePaths(card), state);
    }});
    document.addEventListener('input', event => {{
      if (event.target.matches('select[data-field="decision_status"]')) {{
        const card = event.target.closest('.group-card');
        card.dataset.status = event.target.value;
        card.querySelector('.status-pill').textContent = event.target.value;
      }}
      applyFilters();
    }});
    search.addEventListener('input', applyFilters);
    statusFilter.addEventListener('change', applyFilters);
    classFilter.addEventListener('change', applyFilters);
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a static HTML page for manual cross-class decision review.")
    parser.add_argument("--review-package", default="reports/classification_cross_class_review_package.json")
    parser.add_argument("--decision-table", default="reports/classification_cross_class_decision_table.json")
    parser.add_argument("--decision-csv", default="reports/classification_cross_class_decision_table.csv")
    parser.add_argument("--output", default="reports/classification_cross_class_decision_review.html")
    args = parser.parse_args()

    review_package = resolve_project_path(args.review_package)
    decision_table = resolve_project_path(args.decision_table) if args.decision_table else None
    decision_csv = resolve_project_path(args.decision_csv) if args.decision_csv else None
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_html(review_package, decision_table, decision_csv, output), encoding="utf-8")
    print(json.dumps({"output": str(output), "bytes": output.stat().st_size}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
