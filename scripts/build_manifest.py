#!/usr/bin/env python3
# ============================================================
# manifest 생성기 v2
#
# 문서(.md)를 훑어 목록과 프로젝트 집계를 만든다.
#   manifest.json : 프로그램이 읽는 목록 (커밋됨)
#   manifest.js   : 페이지가 읽는 목록 (커밋됨)
#
# 사용법: 저장소 루트에서  python3 scripts/build_manifest.py
# ============================================================
import json
import os
import re
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_SECTIONS = [
    ("projects",     "프로젝트",   "프로젝트 단위로 정리한 경험"),
    ("reports",      "주간 보고",  "코드와 git 기록 기반 진행 보고"),
    ("experiences",  "경험 정리",  "프로젝트 단위로 정리한 경험"),
    ("experiments",  "실험 기록",  "실험 조건, 결과, 해석"),
    ("applications", "지원 자료",  "자소서, 경력기술서 재료"),
    ("notes",        "기술 노트",  "트러블슈팅과 정리"),
    ("guides",       "작성 지침",  "보고서 작성 규칙과 템플릿"),
]

FM_RE = re.compile(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
DATE_RE = re.compile(r"(20\d{2})[-_.]?(0[1-9]|1[0-2])[-_.]?(0[1-9]|[12]\d|3[01])")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.*)$")


def load_site():
    path = os.path.join(ROOT, "site.json")
    site = {
        "title": os.path.basename(ROOT),
        "subtitle": "",
        "visibility": "private",
        "sections": [s[0] for s in DEFAULT_SECTIONS],
    }
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8-sig") as f:
                site.update(json.load(f))
        except (OSError, ValueError) as e:
            print(f"[!] site.json 을 읽지 못했습니다: {e}", file=sys.stderr)
    keys = site.get("sections") or [s[0] for s in DEFAULT_SECTIONS]
    known = {k: (l, d) for k, l, d in DEFAULT_SECTIONS}
    site["_sections"] = [(k, known.get(k, (k, ""))[0], known.get(k, (k, ""))[1]) for k in keys]
    return site


SITE = load_site()
SECTIONS = SITE["_sections"]


def parse_frontmatter(text, rel):
    """의존성 없는 최소 YAML 파서. 지원하지 않는 문법은 경고를 남긴다."""
    m = FM_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    lines = m.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\r")
        i += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            print(f"    [!] 중첩 YAML 은 지원하지 않습니다, 건너뜀: {rel} :: {line.strip()}",
                  file=sys.stderr)
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val in (">", "|", ">-", "|-"):
            block = []
            while i < len(lines) and lines[i].startswith((" ", "\t")):
                block.append(lines[i].strip())
                i += 1
            meta[key] = " ".join(block)
            continue
        if not val:
            items = []
            while i < len(lines) and LIST_ITEM_RE.match(lines[i]):
                items.append(LIST_ITEM_RE.match(lines[i]).group(1).strip().strip('"').strip("'"))
                i += 1
            meta[key] = items if items else ""
            continue
        val = val.strip('"').strip("'")
        if val.startswith("[") and val.endswith("]"):
            meta[key] = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
        else:
            meta[key] = val
    return meta, text[m.end():]


def as_list(v):
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    if isinstance(v, str) and v.strip():
        return [t.strip() for t in v.split(",") if t.strip()]
    return []


def first_heading(body):
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip()
    return ""


def summarize(body, limit=140):
    out = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "|", "```", "---", ">")):
            continue
        out.append(s)
        if len(" ".join(out)) > limit:
            break
    text = re.sub(r"[*_`\[\]<>]", "", " ".join(out))
    text = re.sub(r"\s+", " ", text).strip()
    return (text[:limit] + "…") if len(text) > limit else text


def valid_date(s):
    try:
        return datetime.strptime(str(s)[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def guess_date(meta, path, body, rel):
    d = valid_date(meta.get("date"))
    if d:
        return d
    for src in (os.path.basename(path), body[:400]):
        m = DATE_RE.search(src)
        if m:
            d = valid_date("-".join(m.groups()))
            if d:
                return d
    return datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")


def read_text(path, rel):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        print(f"    [!] UTF-8 이 아니라 건너뜁니다: {rel}", file=sys.stderr)
        return None
    except OSError as e:
        print(f"    [!] 읽기 실패, 건너뜁니다: {rel} ({e})", file=sys.stderr)
        return None


def collect():
    entries = []
    for folder, label, _d in SECTIONS:
        base = os.path.join(ROOT, folder)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if not d.startswith((".", "_"))]
            for name in sorted(filenames):
                if not name.endswith(".md") or name.startswith("_"):
                    continue
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
                raw = read_text(full, rel)
                if raw is None:
                    continue
                meta, body = parse_frontmatter(raw, rel)
                group = os.path.relpath(dirpath, base).replace(os.sep, "/")
                entries.append({
                    "title": str(meta.get("title") or first_heading(body) or name[:-3])[:120],
                    "path": rel,
                    "category": folder,
                    "category_label": label,
                    "group": "" if group == "." else group,
                    "date": guess_date(meta, full, body, rel),
                    "project": str(meta.get("project") or "").strip(),
                    # 소속·시기 (예: "학부 졸업 프로젝트", "현장실습 · 제조 자동화 기업", "재직 · 로봇 SW 기업")
                    "org": str(meta.get("org") or "").strip(),
                    "role": str(meta.get("role") or "").strip(),
                    "period": str(meta.get("period") or "").strip(),
                    "stage": str(meta.get("stage") or "").strip(),
                    "headline": str(meta.get("headline") or "").strip(),
                    "tags": as_list(meta.get("tags")),
                    "stack": as_list(meta.get("stack")),
                    "summary": str(meta.get("summary") or "").strip() or summarize(body),
                })
    entries.sort(key=lambda e: (e["date"], e["title"]), reverse=True)
    return entries


def build_projects(entries):
    """project 값으로 문서를 묶는다. projects/ 안의 문서가 그 프로젝트의 본체가 된다."""
    buckets = {}
    for e in entries:
        key = e["project"] or (e["title"] if e["category"] == "projects" else "")
        if not key:
            continue
        b = buckets.setdefault(key, {
            "name": key, "org": "", "period": "", "role": "", "stage": "",
            "headline": "", "summary": "", "stack": [], "tags": [],
            "main": None, "docs": [], "dates": [],
        })
        b["dates"].append(e["date"])
        if e["org"] and not b["org"]:
            b["org"] = e["org"]
        for f in ("stack", "tags"):
            for v in e[f]:
                if v not in b[f]:
                    b[f].append(v)
        if e["category"] == "projects" and b["main"] is None:
            b["main"] = e["path"]
            for f in ("org", "period", "role", "stage", "headline", "summary"):
                if e[f]:
                    b[f] = e[f]
        else:
            b["docs"].append({
                "title": e["title"], "path": e["path"],
                "date": e["date"], "category_label": e["category_label"],
            })

    out = []
    for b in buckets.values():
        b["docs"].sort(key=lambda d: d["date"], reverse=True)
        ds = sorted(b["dates"])
        if not b["period"] and ds:
            a, z = ds[0][:7].replace("-", "."), ds[-1][:7].replace("-", ".")
            b["period"] = a if a == z else f"{a} ~ {z}"
        b["last_activity"] = ds[-1] if ds else ""
        b["doc_count"] = len(b["docs"]) + (1 if b["main"] else 0)
        del b["dates"]
        out.append(b)
    out.sort(key=lambda p: p["last_activity"], reverse=True)
    return out


def main():
    entries = collect()
    projects = build_projects(entries)
    site_out = {
        "title": SITE.get("title", ""),
        "subtitle": SITE.get("subtitle", ""),
        "visibility": SITE.get("visibility", "private"),
        # 최종 업데이트 = 가장 최근 문서의 date. 생성 시각 대신 문서 날짜를 쓰므로
        # PC 두 대가 같은 문서 집합에서 같은 값을 만들어 충돌하지 않는다.
        "updated": entries[0]["date"] if entries else "",
    }
    # 랜딩 히어로 (site.json 의 hero: tagline, metrics[], contact{}). 없으면 페이지도 그리지 않는다.
    if isinstance(SITE.get("hero"), dict):
        site_out["hero"] = SITE["hero"]
    manifest = {
        "site": site_out,
        "sections": [{"key": k, "label": l, "description": d} for k, l, d in SECTIONS],
        "count": len(entries),
        "projects": projects,
        "entries": entries,
    }
    # generated_at 은 넣지 않는다. 매번 바뀌면 PC 두 대 사이에서 계속 충돌한다.
    # newline="\n": 윈도우에서 CRLF 로 써지면 git 이 매번 정규화 경고를 낸다.
    with open(os.path.join(ROOT, "manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    with open(os.path.join(ROOT, "manifest.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("// 자동 생성 파일. scripts/build_manifest.py 로 갱신하세요.\n")
        f.write("window.ARCHIVE_MANIFEST = ")
        json.dump(manifest, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write(";\n")

    nj = os.path.join(ROOT, ".nojekyll")
    if SITE.get("visibility") == "public" and not os.path.exists(nj):
        open(nj, "w").close()
        print("[+] .nojekyll 생성 (없으면 GitHub Pages 에서 .md 를 못 읽습니다)")

    print(f"[+] manifest 갱신: 문서 {len(entries)}건, 프로젝트 {len(projects)}건")
    for p in projects:
        print(f"    - {p['name']} ({p['period']}) 문서 {p['doc_count']}건")
    return 0


if __name__ == "__main__":
    sys.exit(main())
