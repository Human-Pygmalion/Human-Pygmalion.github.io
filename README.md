# Human-Pygmalion.github.io

Human Pygmalion 프로젝트 홈페이지 (GitHub Pages, 단일 정적 페이지).

- `index.html` : 페이지 전체 (마크업 + CSS + JS, 외부 의존성은 Google Fonts뿐)
- `assets/img/` : 갤러리, 히어로 포스터, 모집 섹션 배경 (웹용 리사이즈, 장변 1600~1800 px, JPEG q85)
- `assets/video/` : 히어로 배경 영상, 다리 구동 테스트 영상 (H.264 720p)

## 편집 규칙

- "동아리" 표현 금지, "프로젝트"로 쓴다.
- em dash(—)와 가운뎃점(·) 금지. 하이픈이나 쉼표로 쓴다.
- 갤러리 이미지는 크롭하지 않는다 (`object-fit: cover` 금지). 배치는 JS LPT masonry가 담당하므로 걷어내지 말 것.
- 수식 카드 폰트 최대치 26px를 올리지 말 것 (넓은 화면에서 줄바꿈 재발).
- 사람 유사성이 아니라 "기능적 능력 격차 축소"로 프레이밍한다.
