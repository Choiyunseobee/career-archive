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
bash ~/personal_git_package/promote.sh reports/gui_ws/LOG_2026-09-04.md \
     --as projects/visual-servoing.md
# 내용을 확인한 뒤
bash ~/personal_git_package/promote.sh <같은 경로> --as <같은 경로> --publish
```

작성 형식은 `work-journal/guides/PROJECT_TEMPLATE.md` 를 따릅니다.

## 첫 화면 (랜딩 히어로)

`site.json` 의 `hero` 를 고치면 첫 화면의 한 줄 소개, 대표 지표(최대 4개), 연락처가 바뀝니다.
`hero` 를 지우면 히어로도 사라집니다. 최종 업데이트 날짜는 가장 최근 문서의 `date` 에서 자동으로 나옵니다.

```json
"hero": {
  "tagline": "한 줄 정체성",
  "metrics": [ { "value": "97.8%", "label": "픽 성공률", "note": "샘플 500회" } ],
  "contact": { "github": "https://github.com/Choiyunseobee", "email": "" }
}
```

고친 뒤 `python3 scripts/build_manifest.py` 를 다시 실행해야 반영됩니다. 지표 값도 승격 시 민감어 검사를 받습니다.

## 주의

> 이 저장소는 **전 세계에 공개**됩니다.
> 회사 기밀, 미공개 과제 내용, 실험 원본 데이터, 자소서는 올리지 않습니다.
> 한 번 공개된 것은 완전히 지울 수 없습니다.
> 승격 전 `work-journal/guides/PROMOTION_CHECKLIST.md` 를 통과시키세요.

`.gitignore` 는 허용 목록 방식입니다. `.md` 와 사이트 파일 외에는 커밋되지 않습니다.
이미지가 필요하면 `assets/*.svg` 만 허용되며, 사진은 EXIF 를 지운 뒤 `git add -f` 로 개별 추가하세요.
