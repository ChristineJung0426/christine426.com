# christine426.com

Creatorlink 없이 직접 관리하는 GitHub Pages 정적 포트폴리오입니다.
홈페이지의 기존 검정 배경, 글꼴, 카드 배열은 유지했습니다.

## 케이스 스터디 수정

1. `_build/layouts/프로젝트이름.html`에서 내용과 갤러리/카드 구성을 수정합니다.
2. 이미지와 영상은 `images/web/`에 넣고 `src`에 사이트 루트 기준 경로를 적습니다.
3. Python 3으로 `python _build/build.py`를 실행합니다.
4. `python _build/validate.py`로 내부 링크와 재생성을 확인합니다.
5. 변경된 파일을 GitHub에 커밋하고 푸시합니다.

별도 Python 패키지, Creatorlink 계정, 원본 이미지 폴더나 네트워크 연결 없이 빌드할 수 있습니다.
`projects/*.html`은 생성 결과이므로 내용을 바꿀 때는 `_build/layouts/`의 해당 HTML을 먼저 수정하세요.
기존 `_build/content.py`는 이전 버전의 기록이며 현재 빌드에서는 사용하지 않습니다.

지원하는 블록: `heading`, `text`, `image` (`src`, `alt`), `video` (`src`, `title`),
`embed` (YouTube `src`, `title`), `caption`, `anchor` (`id`), `link` (`href`, `text`).
`order`는 프로젝트 이동 순서입니다. 새 프로젝트는 홈페이지 카드도 별도로 추가해야 합니다.

## 파일 구성

- `index.html` — 기존 홈페이지. 이번 업데이트에서 변경하지 않았습니다.
- `projects/*.html` — 케이스 스터디 16개
- `_build/content.json` — 케이스 스터디 내용, 미디어 순서, 출처
- `_build/project-template.html` — 공통 헤더와 푸터
- `_build/build.py`, `_build/validate.py` — 생성 및 검증
- `style.css`, `site.js` — 기존 스타일 및 동작
- `images/web/` — 배포에 필요한 로컬 미디어

## 2026-10-28 내용 업데이트

최신 내용은 https://christinejung426.com/ 의 대응 프로젝트 페이지를 기준으로 반영했습니다.
케이스 스터디는 XR 사이트의 원래 HTML/CSS 레이아웃을 사용하며 색상만 어두운 테마로 변경했습니다. 홈페이지와 전용 XR 프로젝트 목록은 변경하지 않았습니다.

- Kitchen: 최신 렌더/소품/재질/진행 과정, 수상 및 기사 링크, Quixel 식물 크레딧.
- Alleyway: 재질과 에셋 단계 구분, Brick Arch 설명, 최신 이미지.
- Forest: 낮/밤 환경, 물·코스틱·젖음 셰이더와 노드 그래프.
- Arctic Epoch: 생성기별 설명, 문제와 해결, 팀 기여 및 미사용 Snowflake R&D 구분.
- Brick Arch: 문제, 컨트롤, 데모, 기존 형상 적용, 개발 과정, 관련 프로젝트.
- Kettles/Legos: 최신 소개와 메타데이터를 반영하고 기존 상세 제작 과정을 유지.
- Ivy/Daisy 및 대응 재질 페이지: 최신 내용/이미지 반영.
- Terracotta/Stylized Water: 기존 자료를 유지하고 소개를 정리.
- Wood와 Versailles는 최신 사이트의 통합 페이지에서 해당 재질만 각각 반영.

도메인/CNAME과 검색 노출 설정은 변경하지 않았습니다. 커밋·푸시·배포는 별도입니다.

## 레이아웃 및 이미지 동작 업데이트

- `_build/layouts/`: 현재 16개 페이지의 편집 원본. 기존 content.json보다 우선합니다.
- `case-base.css`, `case-layout.css`: XR 사이트의 글꼴과 원래 카드/갤러리/슬라이더 구성.
- `case-dark.css`: 어두운 배경과 카드 색상.
- `case-interactions.js`: 클릭/키보드 확대, 닫기, 우클릭·드래그 저장 억제.
- 우클릭 방지는 완전한 복제 방지가 아닙니다. 브라우저에 표시된 이미지는 캡처하거나 추출할 수 있습니다.
- 이 작업은 저장소 공개 설정을 바꾸거나 커밋·푸시·배포하지 않습니다.
