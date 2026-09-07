---
version: "1.0"
name: career-archive
description: >
  로봇 SW 엔지니어의 전체 경력을 소속별로 탐색하고,
  판단 과정과 측정 근거를 PAAR 문서로 읽는 개인 아카이브.
  중성 캔버스, 명확한 한글 글꼴 체계, 제한적인 파란색 강조를 사용한다.

colors:
  light:
    bg: "#FAFAFA"
    surface: "#FFFFFF"
    surface2: "#F4F4F5"
    border: "#D4D4D8"
    control-border: "#85858F"
    text: "#18181B"
    muted: "#62626B"
    accent: "#1D4ED8"
    accent-hover: "#1E40AF"
    accent-soft: "#EFF6FF"
    on-accent: "#FFFFFF"
  dark:
    bg: "#111113"
    surface: "#18181B"
    surface2: "#242427"
    border: "#3F3F46"
    control-border: "#71717A"
    text: "#F4F4F5"
    muted: "#A1A1AA"
    accent: "#93C5FD"
    accent-hover: "#BFDBFE"
    accent-soft: "#172554"
    on-accent: "#111113"

typography:
  fontFamily: '"IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif'
  monoFamily: 'ui-monospace, "SFMono-Regular", Consolas, "Liberation Mono", "IBM Plex Sans KR", monospace'
  fontStylesheet: "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&display=swap"
  site-title:
    fontSize: 36px
    mobileFontSize: 28px
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: -0.025em
  hero:
    fontSize: 20px
    mobileFontSize: 18px
    fontWeight: 500
    lineHeight: 1.6
    letterSpacing: -0.01em
  metric:
    fontSize: 32px
    mobileFontSize: 28px
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: -0.02em
  group-title:
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: -0.01em
  project-title:
    fontSize: 22px
    mobileFontSize: 20px
    fontWeight: 600
    lineHeight: 1.45
    letterSpacing: -0.015em
  headline:
    fontSize: 18px
    mobileFontSize: 17px
    fontWeight: 600
    lineHeight: 1.55
    letterSpacing: -0.01em
  card-title:
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: -0.01em
  card-body:
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.75
    letterSpacing: 0
  ui:
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0
  caption:
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0
  doc-title:
    fontSize: 32px
    mobileFontSize: 26px
    fontWeight: 700
    lineHeight: 1.35
    letterSpacing: -0.02em
  doc-h2:
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.45
    letterSpacing: -0.01em
  doc-h3:
    fontSize: 19px
    fontWeight: 600
    lineHeight: 1.45
    letterSpacing: -0.01em
  doc-body:
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.8
    letterSpacing: 0
  table:
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0
  code:
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0

spacing:
  unit: 4px
  scale: [4px, 8px, 12px, 16px, 24px, 32px, 40px, 48px, 64px]
  card-padding: 24px
  card-padding-mobile: 20px
  card-gap: 16px
  group-gap: 40px
  section-gap: 48px

rounded:
  small: 4px
  control: 6px
  card: 8px

elevation:
  default: none

layout:
  index-max-width: 1080px
  viewer-max-width: 768px
  prose-max-width: 720px
  gutter: 24px
  mobile-gutter: 16px
  mobile-breakpoint: 640px
  document-columns: 2
  touch-target: 44px
---

# Career Archive Design

## 목적과 디자인 방향

Vercel 후보의 절제된 화면 구성과 Mintlify 후보의 문서 읽기
원칙을 참고한다. 브랜드의 폰트·장식·마케팅 레이아웃은 복제하지 않는다.

첫 화면에서 이름, 직무, 전문성, 읽을 사례를 빠르게 파악할 수 있어야 한다.
상세 문서는 판단 근거, 측정 조건, 본인 기여를 확인하기 쉬워야 한다.

공개 사이트는 채용 담당자·면접관·공개 문서를 읽는 동료를 위한 화면이다.
본인의 작업 현황과 운영 절차는 별도 OVERVIEW에서 관리한다.

## 정보 구조

홈:
이름·직무 → 기록 범위 → 전문성 → 연락처 →
검증된 대표 성과(있을 때) → 프로젝트/문서 모드 →
검색 → 소속별 프로젝트 → 푸터.

현재처럼 프로젝트가 적을 때는 대표 작업과 전체 작업을 중복 배치하지 않는다.
자료가 늘면 히어로 아래에 대표 사례 2~3건의 짧은 링크를 추가한다.
소속별 전체 경력은 계속 유지한다.

프로젝트 카드:
제목·기간 → 역할·단계 → 핵심 성과 → 문제와 접근 요약 →
대표 기술 → 사례 읽기 → 관련 문서.

상세:
목록 복귀·프로젝트 맥락 → 제목·기간·역할·단계 →
결과 요약·측정 범위 → 목차 →
문제 → 분석(검토와 판단) → 행동(한 일) → 결과 →
내 기여 → 한계·회고 → 관련 문서.

PAAR 순서는 유지한다. 상단 결과 요약은 정독 전 안내 역할이다.
프로젝트명과 문서명이 다르면 상세 상단에 둘의 관계를 표시한다.

## 색상 적용

frontmatter의 색상 키는 같은 이름의 CSS 변수로 매핑한다.

```css
:root {
  color-scheme: light;
  --bg: #FAFAFA;
  --surface: #FFFFFF;
  --surface2: #F4F4F5;
  --border: #D4D4D8;
  --control-border: #85858F;
  --text: #18181B;
  --muted: #62626B;
  --accent: #1D4ED8;
  --accent-hover: #1E40AF;
  --accent-soft: #EFF6FF;
  --on-accent: #FFFFFF;
  --shadow: none;
}

@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
    --bg: #111113;
    --surface: #18181B;
    --surface2: #242427;
    --border: #3F3F46;
    --control-border: #71717A;
    --text: #F4F4F5;
    --muted: #A1A1AA;
    --accent: #93C5FD;
    --accent-hover: #BFDBFE;
    --accent-soft: #172554;
    --on-accent: #111113;
  }
}
```

기본 테마는 라이트이며 OS의 다크 설정에 대응한다.
수동 테마 선택은 필요할 때 추가하며 두 페이지에 같은 규칙을 적용한다.

accent는 링크·선택·포커스에 사용한다.
성과는 기본 글자색, 크기와 굵기로 강조한다.
accent 배경 위 글자는 반드시 on-accent를 사용한다.
입력과 버튼의 경계는 control-border를 사용한다.
muted는 보조 정보에만 사용하고 핵심 결론을 약하게 표시하지 않는다.

## 한글 글꼴 규칙

IBM Plex Sans KR 400·500·600·700을 제목·UI·본문에 공통 사용한다.
코드만 시스템 고정폭 글꼴을 사용한다.

```html
<link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&display=swap">
```

대안은 Noto Sans KR이다. 대안을 선택하면 링크와 font-family를
함께 바꾸며 두 한글 웹폰트를 동시에 로드하지 않는다.

- 본문 자간은 0, 제목 자간은 -0.025em보다 좁히지 않는다.
- 한글에 영문 대문자 라벨용 넓은 자간을 적용하지 않는다.
- 일반 텍스트는 word-break: keep-all과 overflow-wrap: anywhere를 사용한다.
- 코드 블록은 줄과 들여쓰기를 보존한다.
- 수치·기간에는 font-variant-numeric: tabular-nums를 적용한다.
- 중요한 조건과 태그를 13px 미만으로 줄이지 않는다.
- 제목·성과·측정 조건은 말줄임이나 line-clamp로 감추지 않는다.

## 레이아웃과 표면

인덱스 .wrap의 최대 폭 1080px을 유지한다.
상단 패딩은 데스크톱 40px, 모바일 24px을 기준으로 한다.
좌우 여백은 24px, 640px 미만에서는 16px이다.

프로젝트 카드는 한 열을 유지한다.
문서 카드는 최대 두 열, 모바일 한 열이다.
카드 높이를 고정하지 않고 한글 줄바꿈에 따라 늘어난다.

뷰어 .wrap은 최대 768px, 좌우 24px이다.
article의 바깥 테두리·배경판·내부 패딩을 제거해 본문 폭을 확보한다.
모바일 좌우 여백은 16px이다.

본문 문단 아래는 16px, H2 위는 40px·아래는 16px,
H3 위는 24px·아래는 12px을 기준으로 한다.

기본 그림자와 카드 이동 애니메이션은 사용하지 않는다.
반경은 4·6·8px만 사용한다.
그라데이션, 장식용 점 격자, 가짜 터미널, 의미 없는 로봇 이미지는 두지 않는다.

## 컴포넌트

### 히어로

#site-title에 이름과 직무를 함께 표시한다.
#site-sub는 기록 범위, .hero-tag는 전문성 설명으로 역할을 나눈다.
.hero-tag는 약 44rem 이내에서 읽히도록 한다.

.hero-foot에는 실제 연락처를 표시한다.
공개 저장소 배지는 첫 화면에서 생략하거나 푸터로 옮긴다.
최근 문서 날짜는 푸터 한 곳에 표시한다.

.hero-metrics는 근거가 있는 성과만 최대 두 개 표시한다.
데스크톱 두 열, 모바일 한 열이다.
.metric .v는 text 색을 사용한다.
프로젝트명과 측정 조건은 가까이에 13px 이상으로 표시한다.
지표가 없으면 해당 공간을 남겨두지 않는다.

### 모드와 필터

.modes의 프로젝트 / 문서 전체 구분을 유지한다.
선택된 .mode는 굵기와 2px 밑줄로 표시한다.

#search에는 보이는 검색 라벨을 제공한다.
프로젝트 뷰의 #tagbar는 기본 접고, 펼치는 동작을 제공한다.
접는 기능을 도입할 때 선택된 필터는 계속 보이게 한다.

.tagchip과 .tab은 필터 버튼이다.
선택 상태는 accent-soft 배경, accent 글자·경계, 굵기로 표시한다.
점선 경계는 사용하지 않는다.
버튼의 높이는 최소 44px이다.

### 소속 그룹

.ogroup은 18px/600, text 색을 사용한다.
프로젝트 개수는 13px muted로 표시한다.
그룹 사이 40px, 그룹명과 첫 카드 사이 12px을 둔다.
첫 그룹에는 불필요한 상단 간격을 추가하지 않는다.

소속별 묶음과 현재의 경력 탐색 흐름을 유지한다.
그룹화된 목록에서는 카드의 소속 반복을 줄이고 역할을 우선한다.

### 프로젝트 카드

.pcard:
surface 배경, border 1px, 반경 8px, 그림자 없음.
패딩 24px, 모바일 20px.

.pname은 22px, 모바일 20px이다.
.pperiod는 14px muted이며 모바일에서 제목 아래에 둔다.

.pmeta는 역할을 먼저, 단계·문서 수를 뒤에 표시한다.
.headline은 surface2 배경과 text 색, 18px/600을 사용한다.
패딩은 12px 16px, 반경은 4px이다.
선택적으로 border 색의 2px 왼쪽 선을 사용한다.

.psum은 문제와 접근을 짧게 설명한다.
성과 헤드라인을 같은 표현으로 반복하지 않는다.

.chips의 정적 라벨은 13px, surface2 배경, muted 글자색이다.
편집 단계에서 대표 기술 3~5개를 우선한다.
숨긴 태그 수를 표시한다면 전체를 확인할 방법도 제공한다.

.pactions의 주요 링크 문구는 '사례 읽기'를 기본으로 한다.
카드당 주요 행동은 하나다.
.btn.primary는 accent 배경과 on-accent 글자색을 사용한다.

.docs는 관련 문서가 있을 때 펼쳐 읽는다.
모바일에서는 제목과 날짜·분류를 두 줄로 배치할 수 있다.

### 문서 카드

.grid는 데스크톱 최대 두 열, 모바일 한 열이다.
.card는 surface 배경, border 1px, 반경 8px, 패딩 20px이다.

문서 제목 18px/600, 프로젝트 맥락 13px,
요약 15px, 날짜·분류 13px을 사용한다.
제목과 프로젝트 맥락을 날짜보다 먼저 읽히게 한다.

.card-tags는 정적 라벨이며 accent를 반복하지 않는다.
호버에서 카드를 이동하지 않고 경계선만 강조한다.

### 뷰어 탐색

.back과 #meta, #doc를 유지한다.
#meta에는 문서 날짜와 구분되는 프로젝트 기간·역할·단계를 표시한다.

긴 문서는 본문 위에 H2 기준의 짧은 목차를 제공한다.
필요하면 넓은 화면에만 보조 목차를 추가한다.
현재 규모에서는 좌우 사이드바가 있는 3열 레이아웃을 만들지 않는다.

목차와 수치 출처 링크는 실제 문서 위치로 연결한다.
CSS만으로 없는 목차나 출처 관계가 생긴다고 가정하지 않는다.

### 표

표는 15px, 행간 1.6, 셀 패딩 10px 12px을 사용한다.
헤더는 surface2 배경과 600 굵기다.
셀은 위쪽 정렬이며 기본 구분은 가로선이다.

결과 표의 지표·측정 조건은 왼쪽, before·after 숫자는 오른쪽 정렬한다.
숫자 열에는 tabular-nums를 적용한다.
대안 비교표의 두 번째 열을 숫자 열로 취급하지 않는다.
정렬은 명시적인 열 정보 또는 마크다운 정렬로 지정한다.

숫자·단위는 한 덩어리로 읽히게 하고 조건 설명은 줄바꿈한다.
넓은 표는 표 영역 안에서 가로 스크롤하며 페이지 전체를 밀어내지 않는다.
측정 조건은 작은 각주로 멀리 보내지 않고 결과 행과 함께 둔다.

### 코드와 인용

article code:
중성 배경 surface2, 글자 text, 14px, 반경 4px.

article pre:
surface2 배경, border 1px, 반경 8px, 패딩 16px.
pre code에는 중첩 배경과 패딩을 적용하지 않는다.
원문 줄바꿈과 들여쓰기를 보존하며 블록 안에서 가로 스크롤한다.
짧은 인라인 코드·경로는 필요할 때 줄바꿈한다.

인용문:
기본 글자색 text, 왼쪽 선 border, 좌우 내부 여백 16px.
예시 표시와 해석상 중요한 조건을 muted로 약화하지 않는다.

## 성과와 콘텐츠 규칙

- 공개 성과 영역에는 실제 근거가 준비된 결과만 표시한다.
- 예시 문서는 제목 근처에 '예시 데이터'를 명시한다.
- 예시 수치를 실제 경력의 대표 성과로 사용하지 않는다.
- 수치는 before → after, 단위, 측정 조건, 적용 범위를 함께 제시한다.
- 기준값이 없거나 측정 전이면 그 상태를 명시하고 개선율을 만들지 않는다.
- 성공률 변화의 %p와 상대 개선율 %를 구분한다.
- 팀의 결과와 본인의 역할을 구분한다.
- 채택한 방법뿐 아니라 버린 대안과 이유를 남긴다.
- 그림·그래프는 실제 판단이나 결과를 설명할 때만 사용한다.
- 증거가 없는 성과를 채우기 위해 수치나 시각 자료를 만들지 않는다.

## 상호작용

링크는 본문에서 밑줄로 식별할 수 있게 한다.
모든 상호작용 요소의 focus-visible은 accent 2px,
outline-offset 3px을 기준으로 한다.

색상만으로 선택 상태를 전달하지 않는다.
카드 호버 이동은 사용하지 않는다.
전환을 사용한다면 색·경계에 120ms 정도만 적용하고
prefers-reduced-motion에서는 제거한다.

## 기존 구조에 적용하는 범위

유지:
#site-title, #site-sub, #hero, #search, #tabs, #tagbar,
#count, #plist, #grid, #footer, #meta, #doc.
renderHero(), projectHead(), projectCard(), render()의 역할.

CSS 중심 변경:
토큰, 폰트, 간격, 반경, 카드 열 수, 뷰어 본문 폭,
표·코드 스타일, 호버·포커스.

소폭 마크업·렌더 변경:
메타 표시 순서, 공개 배지 위치, 필터 접기,
프로젝트 맥락, 결과 요약, 목차, 출처 링크.

추후 데이터 확장:
대표 사례 선정과 지표 출처는 필요할 때 명시적인 필드로 추가한다.
현재 없는 데이터를 기존 필드가 제공한다고 가정하지 않는다.
임의의 헤드라인 문자열에서 숫자를 추정해 의미별로 꾸미지 않는다.

이 사양은 index.html과 viewer.html에 적용한다.
OVERVIEW.html은 독립적인 운영 문서 디자인을 유지한다.
DESIGN.md는 프로젝트 문서 목록에 포함하지 않는다.

## 확인과 개선

적용 후 실제 화면에서 확인한다.

- 1440px, 768px, 375px, 320px 폭의 라이트·다크.
- 긴 한글 제목, 긴 소속명, 긴 기술명.
- 성과 없음, 관련 문서 없음, 문서 여러 건, 검색 결과 없음.
- 모바일에서 표·코드 외 페이지 전체 가로 스크롤이 없는지.
- 200% 확대와 키보드 포커스에서 내용과 기능이 유지되는지.
- 웹폰트 로딩 전에도 읽고 탐색할 수 있는지.
- 첫 화면에서 이름·직무·전문성을 찾을 수 있는지.
- 첫 화면의 수치에서 해당 측정 근거로 이동할 수 있는지.

현재 사양은 제안이며 브라우저 시각 검증을 완료한 상태가 아니다.
변경 시에는 바꾼 규칙과 이유를 함께 기록한다.

<!-- 출처: Codex CLI 디자인 검토 2026-09-07 (work-journal/notes/codex-design-review-20260907.md). Vercel 후보의 화면 구성 + Mintlify 후보의 문서 읽기 규칙을 이 사이트에 맞게 줄인 것. 바꿀 때는 바꾼 규칙과 이유를 여기와 REVIEW.md 에 함께 적는다. -->
