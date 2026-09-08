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
# 본문의 "쉽게 말하면" 인용문. 카드에 미리보기로 쓴다. 문서마다 형식이 같다(guides/REPORT_GUIDE.md).
PLAIN_RE = re.compile(r"^>[ \t]*\*\*쉽게 말하면\*\*[ \t]*\r?\n((?:^>.*\r?\n?)*)", re.M)
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

    # org_order: 소속 표시 순서. 없으면 문서 날짜순으로 밀려서
    # 오늘 쓴 학부 문서가 재직 경력보다 위로 온다.
    order = site.get("org_order")
    if order is not None and not (isinstance(order, list)
                                  and all(isinstance(o, str) for o in order)):
        print("[!] site.json 의 org_order 는 문자열 배열이어야 합니다. 무시합니다.",
              file=sys.stderr)
        order = None
    site["org_order"] = order or []

    # credentials: 학력·자격·교육·수상. 프로젝트 카드로 만들면 목록이 과밀해진다.
    creds = site.get("credentials")
    if creds is not None:
        groups = creds.get("groups") if isinstance(creds, dict) else None
        ok = isinstance(groups, list) and all(
            isinstance(g, dict) and isinstance(g.get("label"), str)
            and isinstance(g.get("items"), list)
            and all(isinstance(i, dict) and i.get("name") for i in g["items"])
            for g in groups)
        if not ok:
            # 조용히 기본값으로 넘어가면 화면에서 통째로 사라진 것을 눈치채기 어렵다.
            print("[!] site.json 의 credentials 형식이 맞지 않습니다. "
                  "{groups: [{label, items: [{name, ...}]}]} 여야 합니다. 무시합니다.",
                  file=sys.stderr)
            creds = None
        else:
            n = sum(len(g["items"]) for g in groups)
            print("    credentials: %d개 묶음, 항목 %d건" % (len(groups), n))
    site["credentials"] = creds or {}

    # glossary: 문서에 나오는 용어를 이 분야 밖의 사람도 읽을 수 있게 푼 것.
    gl = site.get("glossary")
    if gl is not None:
        terms = gl.get("terms") if isinstance(gl, dict) else None
        if not (isinstance(terms, list)
                and all(isinstance(t, dict) and t.get("t") and t.get("d") for t in terms)):
            print("[!] site.json 의 glossary 형식이 맞지 않습니다. "
                  "{terms: [{t, e, d}]} 여야 합니다. 무시합니다.", file=sys.stderr)
            gl = None
        else:
            print("    glossary: 용어 %d개" % len(terms))
    site["glossary"] = gl or {}
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
        # 따옴표로 감싼 값은 문자열이다. 벗기기 전에 판단해야 "[ROS2]" 같은 제목이 목록이 되지 않는다 (C11).
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
            if val[0] == '"':
                try:
                    meta[key] = json.loads(val)          # JSON 호환 escape 지원
                except ValueError:
                    meta[key] = val[1:-1].replace('\\"', '"')
            else:
                meta[key] = val[1:-1].replace("''", "'")  # YAML 작은따옴표 escape
        elif val.startswith("[") and val.endswith("]"):
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
    # 파일 수정 시각은 PC 마다 다르다(clone 시각). 두 PC 가 다른 목록을 만들게 되므로 쓰지 않는다 (C15).
    print(f"    [!] date 가 없습니다. 프론트매터에 date: YYYY-MM-DD 를 적으세요: {rel}", file=sys.stderr)
    return ""


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
                    # track: 소속과 다른 축. 같은 회사 안에도 현업과 연구가 섞인다.
                    "track": str(meta.get("track") or "").strip(),
                    "role": str(meta.get("role") or "").strip(),
                    "period": str(meta.get("period") or "").strip(),
                    "stage": str(meta.get("stage") or "").strip(),
                    "headline": str(meta.get("headline") or "").strip(),
                    "tags": as_list(meta.get("tags")),
                    "stack": as_list(meta.get("stack")),
                    "summary": str(meta.get("summary") or "").strip() or summarize(body),
                    "plain": extract_plain(body),
                    # 이 사례와 이어지는 이론 심화 교재 장 번호. 예: chapters: [5, 17]
                    "chapters": [n for n in (to_int(x) for x in as_list(meta.get("chapters"))) if n],
                })
    entries.sort(key=lambda e: (e["date"], e["title"]), reverse=True)
    return entries


def to_int(v):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return 0


def extract_plain(body):
    """본문의 "쉽게 말하면" 인용문을 한 덩이 문장으로 돌려준다. 없으면 빈 문자열."""
    m = PLAIN_RE.search(body or "")
    if not m:
        return ""
    out = []
    for line in m.group(1).splitlines():
        line = line.lstrip(">").strip()
        if line:
            out.append(line)
    return " ".join(out)[:400]


def build_projects(entries):
    """project 값으로 문서를 묶는다. projects/ 안의 문서가 그 프로젝트의 본체가 된다.
    소속(org)이 다르면 이름이 같아도 다른 프로젝트다 (학부 'Robot' 과 회사 'Robot', C12)."""
    def name_of(e):
        return e["project"] or (e["title"] if e["category"] == "projects" else "")

    def new_bucket(name):
        return {
            "name": name, "org": "", "track": "", "period": "", "role": "", "stage": "",
            "headline": "", "summary": "", "plain": "", "chapters": [], "stack": [], "tags": [],
            "main": None, "docs": [], "dates": [],
        }

    def add(b, e):
        if e["date"]:                      # 날짜 없는 문서는 기간 계산에 넣지 않는다 (C15)
            b["dates"].append(e["date"])
        if e["org"] and not b["org"]:
            b["org"] = e["org"]
        if e["track"] and not b["track"]:
            b["track"] = e["track"]
        for f in ("stack", "tags"):
            for v in e[f]:
                if v not in b[f]:
                    b[f].append(v)
        if e["category"] == "projects" and b["main"] is None:
            b["main"] = e["path"]
            for f in ("org", "track", "period", "role", "stage", "headline", "summary", "plain", "chapters"):
                if e.get(f):
                    b[f] = e[f]
        else:
            b["docs"].append({
                "title": e["title"], "path": e["path"],
                "date": e["date"], "category_label": e["category_label"],
            })

    buckets = {}
    # 1차: org 가 있는 문서는 (org, 이름) 으로 묶는다.
    for e in entries:
        n = name_of(e)
        if n and e["org"]:
            add(buckets.setdefault((e["org"], n), new_bucket(n)), e)
    # 2차: org 가 없는 문서는 같은 이름의 프로젝트가 정확히 하나일 때만 거기에 붙인다.
    for e in entries:
        n = name_of(e)
        if not n or e["org"]:
            continue
        cands = [k for k in buckets if k[1] == n]
        if len(cands) == 1:
            key = cands[0]
        else:
            if len(cands) > 1:
                print(f"    [!] 같은 이름의 프로젝트가 소속별로 여러 개라 연결할 수 없습니다. org: 를 적으세요: {e['path']}",
                      file=sys.stderr)
            key = ("", n)
        add(buckets.setdefault(key, new_bucket(n)), e)

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

    # 1순위 소속 순서, 2순위 최근 활동. org_order 에 없는 소속은 뒤로 보낸다.
    order = SITE.get("org_order") or []
    rank = {name: i for i, name in enumerate(order)}
    unknown = sorted({b["org"] for b in out if b["org"] and b["org"] not in rank})
    if unknown:
        print("    [!] site.json 의 org_order 에 없는 소속이 있어 뒤로 정렬합니다: "
              + ", ".join(unknown), file=sys.stderr)
    for b in out:
        b["org_rank"] = rank.get(b["org"], len(order) + 1)
    out.sort(key=lambda p: (p["org_rank"], [-int(x) for x in p["last_activity"].split("-")]
                            if p["last_activity"] else [0, 0, 0]))
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
    if SITE.get("org_order"):
        site_out["org_order"] = SITE["org_order"]
    if SITE.get("credentials"):
        site_out["credentials"] = SITE["credentials"]
    if SITE.get("glossary"):
        site_out["glossary"] = SITE["glossary"]
    # book: 이론 심화 교재 장 목록. build_textbook.py 가 site.json 에 써 넣는다.
    # 첫 화면의 "연결된 교재 장" 칩이 번호를 제목으로 바꿀 때 쓴다.
    if isinstance(SITE.get("book"), dict) and SITE["book"].get("chapters"):
        site_out["book"] = SITE["book"]
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
