# Agent 365 초기 설정 및 구성 가이드

Copilot Studio(New experience)에서 만든 에이전트의 기본 보안 설정을 안내하는 웹 가이드입니다.
에이전트 생성(0)부터 트래픽 모니터링(7)까지 8단계를 스크린샷과 함께 순서대로 정리했습니다.

## 배포

`main` 브랜치에 push하면 GitHub Actions(`.github/workflows/deploy.yml`)가 `index.html`과 `img/`를
GitHub Pages로 배포합니다.

## 소스 재생성

- `extract.py` — 원본 PPTX에서 슬라이드 구조를 `deck.json`으로 추출
- `crop.py` — 슬라이드 PNG에서 제목/설명을 제외한 콘텐츠 영역만 크롭
- `build2.py` — `index.html` 생성

`slides/`(원본 슬라이드 PNG)와 원본 PPTX는 저장소에 포함되지 않습니다.
