# 최윤섭 · 경험 아카이브

로봇 SW 엔지니어로 해온 일을 프로젝트 단위로 정리한 공개 아카이브입니다.

**공개 사이트:** https://choiyunseobee.github.io/career-archive/

## 구조

- `projects/` — 프로젝트 문서. 같은 `project:` 값을 가진 문서는 사이트에서 하나의 카드로 묶이고, `org:`(소속·시기)가 있으면 소속별로 묶여 보입니다.
- `notes/` — 트러블슈팅 등 기술 노트
- `manifest.json` — 전체 목록 (프로그램이 읽는 용도)
- `index.html` — 프로젝트 뷰와 문서 뷰
- `viewer.html` — 문서 본문 뷰어

## 새 항목 추가

원본은 비공개 저장소(`work-journal`)에 두고, 다듬은 것만 승격합니다.

```bash
bash ~/personal_git_package/promote.sh reports/gui_ws/LOG_<날짜>.md \
     --as projects/visual-servoing.md
# 내용을 확인한 뒤
bash ~/personal_git_package/promote.sh <같은 경로> --as <같은 경로> --publish
```

작성 형식은 `work-journal/guides/PROJECT_TEMPLATE.md` 를 따릅니다.

## 첫 화면 (랜딩 히어로)

`site.json` 의 `hero` 를 고치면 첫 화면의 한 줄 소개, 대표 지표(화면은 최대 2개), 연락처가 바뀝니다.
`hero` 를 지우면 히어로도 사라집니다. 최종 업데이트 날짜는 가장 최근 문서의 `date` 에서 자동으로 나옵니다.

```json
"hero": {
  "tagline": "한 줄 정체성",
  "metrics": [ { "value": "<전> → <후>", "label": "<지표명>", "note": "<측정 조건과 범위>" } ],
  "contact": { "github": "https://github.com/Choiyunseobee", "email": "" }
}
```

고친 뒤 `python3 scripts/build_manifest.py` 를 다시 실행해야 반영됩니다.
**지표는 근거가 확인된 값만 넣습니다.** 예시 값이나 미측정 추정치를 대표 성과 자리에 두지 않습니다.
민감어 검사는 `promote.sh` 로 승격할 때 동작하며, `site.json` 을 직접 고칠 때는 사람이 확인해야 합니다.

## 주의

> 이 저장소는 **전 세계에 공개**됩니다.
> 회사 기밀, 미공개 과제 내용, 실험 원본 데이터, 자소서는 올리지 않습니다.
> 한 번 공개된 것은 완전히 지울 수 없습니다.
> 승격 전 `work-journal/guides/PROMOTION_CHECKLIST.md` 를 통과시키세요.

`.gitignore` 는 허용 목록 방식입니다. 허용 경로는 `README.md`, `DESIGN.md`, `projects/*.md`, `notes/*.md`, 사이트 파일, `assets/*.svg` 뿐입니다.
증명서·성적표·자격증 스캔·사진 등 증빙 원본은 **어느 저장소에도 올리지 않습니다.**
공개 저장소는 물론 비공개 `work-journal` 에도 두지 않고, 개인 PC 의 저장소 밖 보관소
(`CareerLocal/originals/`)에만 둡니다. 저장소에는 자료 ID 와 확인한 사실만 남깁니다.
