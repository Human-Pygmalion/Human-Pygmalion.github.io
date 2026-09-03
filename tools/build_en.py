#!/usr/bin/env python3
"""Generate en/index.html from index.html (Korean source of truth).

Same markup/CSS/JS; only visible text is replaced from the table below.
Every source string must still exist in index.html - the script aborts on
a missing one so the English page can never silently drift from the Korean one.
Run after editing index.html:  python3 tools/build_en.py
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / 'index.html').read_text(encoding='utf-8')

T = [
 ('<html lang="ko">', '<html lang="en">'),
 ('content="Human Pygmalion: 서울대학교 자율로봇지능 연구실(ARILab)의 풀사이즈 휴머노이드 제작 프로젝트. 몸(기구)과 제어를 함께 설계해 사람과 휴머노이드의 능력 격차를 줄입니다."',
  'content="Human Pygmalion: a full-size humanoid project at the Autonomous Robot Intelligence Lab (ARIL), Seoul National University. We co-design body and control to close the capability gap between humans and humanoids."'),
 ('content="서울대학교 자율로봇지능 연구실(ARILab)의 풀사이즈 휴머노이드 제작 프로젝트. 몸과 제어를 함께 설계합니다."',
  'content="A full-size humanoid project at ARIL, Seoul National University. Body and control, designed together."'),
 ('<meta property="og:url" content="https://human-pygmalion.github.io/">', '<meta property="og:url" content="https://human-pygmalion.github.io/en/">'),
 # hero
 ('사람이 할 수 있는 일을, 로봇도 할 수 있도록,<br>몸과 두뇌인 제어와 학습을 함께 설계하는 팀입니다.',
  'Whatever a human can do, a robot should be able to do too.<br>We design the body and the brain, control and learning, together.'),
 ('>팀에 합류하기</a>', '>Join the team</a>'),
 # recruiting
 ('새로운 도전적 여정에 함께할 여러분을 기다립니다.', 'We are looking for people to join a new and ambitious journey.'),
 ('QTY : 1~2명', 'OPENINGS : 1 to 2', 2), ('QTY : 1~3명', 'OPENINGS : 1 to 3'),
 ('<div class="pos-name">설계</div>', '<div class="pos-name">Design</div>'),
 ('<div class="pos-name">제작</div>', '<div class="pos-name">Fabrication</div>'),
 ('<div class="pos-name">제어</div>', '<div class="pos-name">Control</div>'),
 ('휴머노이드 외관 디자인 및 설계 - 마운트, 커버 등 하드웨어 인터페이스 포함', 'Humanoid exterior design and mechanical design, including hardware interfaces such as mounts and covers'),
 ('우대 - 3D CAD 경험 (Fusion360 외)', 'PREFERRED - 3D CAD experience (Fusion 360 or similar)'),
 ('설계된 부품을 정밀 가공(CNC, 3D 프린팅)으로 구현하는 제조 엔지니어링', 'Manufacturing engineering: turning designed parts into precision-machined (CNC) and 3D-printed hardware'),
 ('우대 - 3D 프린터, CNC 경험자, 2D / 3D 도면 작성에 관심', 'PREFERRED - 3D printing or CNC experience, interest in 2D / 3D drafting'),
 ('모터 제어, 강화학습 기반 보행 제어, 시스템 아키텍처 설계', 'Motor control, reinforcement-learning-based locomotion control, system architecture design'),
 ('우대 - C++/Python, 강화학습 또는 로보틱스 제어에 관심', 'PREFERRED - C++/Python, interest in reinforcement learning or robot control'),
 ('프로젝트에 관심이 있다면 메일로 연락해 주세요.', 'Interested in the project? Send us an e-mail.'),
 ('>연락하기 ↗</a>', '>Get in touch ↗</a>'),
 # roadmap
 ('STATUS - Huphy 1.0 하체 조립 완료, 기립과 보행 제어 준비 중', 'STATUS - Huphy 1.0 lower body assembled, standing and walking control in preparation'),
 ('<div class="rmap-name">하체 설계와 제작</div>', '<div class="rmap-name">Lower-body design and build</div>'),
 ('CAD 설계, CNC/3D프린팅 부품 가공, RobStride 액추에이터 통합 - Huphy 1.0', 'CAD design, CNC and 3D-printed parts, RobStride actuator integration - Huphy 1.0'),
 ('<div class="rmap-name">기립과 보행 제어</div>', '<div class="rmap-name">Standing and walking control</div>'),
 ('밸런싱 및 보행 제어기 개발, 센서 통합, Sim2Real 이식', 'Balancing and locomotion controllers, sensor integration, sim-to-real transfer'),
 ('<div class="rmap-name">상체 설계와 제작</div>', '<div class="rmap-name">Upper-body design and build</div>'),
 ('상체와 팔 설계 및 전신 하드웨어 완성', 'Torso and arm design, completing the full-body hardware'),
 ('<div class="rmap-name">다양한 환경 적응</div>', '<div class="rmap-name">Adapting to varied environments</div>'),
 ('다양한 환경에서도 유연하게 걷고, 춤추고, 무거운 페이로드를 운반', 'Walking robustly across environments, dancing, carrying heavy payloads'),
 # build log
 ('컨셉부터 실제 프로토타입 Huphy 1.0 제작까지의 여정', 'The journey from concept to the working prototype, Huphy 1.0'),
 ('data-caption="REAL : Huphy 1.0 하체 실물" aria-label="확대 보기: Huphy 1.0 하체 실물"', 'data-caption="REAL : Huphy 1.0 lower body" aria-label="Enlarge: Huphy 1.0 lower body"'),
 ('alt="Huphy 1.0 하체 조립 실물 사진"', 'alt="Photo of the assembled Huphy 1.0 lower body"'),
 ('<span class="feat-idx">REAL</span>실물 - Huphy 1.0 하체', '<span class="feat-idx">REAL</span>Hardware - Huphy 1.0 lower body'),
 ('data-caption="CONCEPT : 초기 컨셉 스케치" aria-label="확대 보기: 초기 컨셉 스케치"', 'data-caption="CONCEPT : early concept sketches" aria-label="Enlarge: early concept sketches"'),
 ('alt="휴머노이드 외형 초기 컨셉 스케치 노트"', 'alt="Sketchbook with early humanoid concept drawings"'),
 ('<span class="feat-idx">CONCEPT</span>컨셉아트 - 초기 스케치', '<span class="feat-idx">CONCEPT</span>Concept art - early sketches'),
 ('data-caption="DESIGN : 외형 디자인 렌더" aria-label="확대 보기: 외형 디자인 렌더"', 'data-caption="DESIGN : exterior design render" aria-label="Enlarge: exterior design render"'),
 ('alt="휴머노이드 외형 디자인 CAD 렌더, 측면"', 'alt="Side-view CAD render of the humanoid exterior design"'),
 ('<span class="feat-idx">DESIGN</span>디자인 - 외형 렌더', '<span class="feat-idx">DESIGN</span>Design - exterior render'),
 ('data-caption="CAD : 다리 구동부 설계, 인체 오버레이" aria-label="확대 보기: 다리 구동부 CAD 설계 및 인체 오버레이"', 'data-caption="CAD : leg drivetrain design with human overlay" aria-label="Enlarge: leg drivetrain CAD with human body overlay"'),
 ('alt="다리 구동부 CAD 설계 단면 및 인체 골격 오버레이"', 'alt="Leg drivetrain CAD section with a human body overlay"'),
 ('<span class="feat-idx">CAD</span>설계 - 다리 구동부, 인체 오버레이', '<span class="feat-idx">CAD</span>Design - leg drivetrain, human overlay'),
 ('data-caption="FAB : 부품 정밀 가공 중" aria-label="확대 보기: 부품 정밀 가공 중"', 'data-caption="FAB : precision machining a part" aria-label="Enlarge: precision machining a part"'),
 ('alt="바이스에 고정한 부품을 렌치와 해머로 가공하는 모습"', 'alt="Working a part clamped in a vise with a wrench and hammer"'),
 ('<span class="feat-idx">FAB</span>가공 중 - 부품 정밀 가공', '<span class="feat-idx">FAB</span>In the shop - precision machining'),
 ('aria-label="다리 구동 테스트 동작 영상"', 'aria-label="Leg actuation test video"'),
 ('<span class="feat-idx">MOTION</span>동작 - 다리 구동 테스트', '<span class="feat-idx">MOTION</span>Motion - leg actuation test'),
 ('data-caption="SIM : 시뮬레이션 모델" aria-label="확대 보기: 시뮬레이션 모델"', 'data-caption="SIM : simulation model" aria-label="Enlarge: simulation model"'),
 ('alt="다리 구동부 및 텔레오퍼레이션 마스터 암 시뮬레이션 모델 렌더"', 'alt="Render of the simulation model with legs and teleoperation master arms"'),
 ('<span class="feat-idx">SIM</span>시뮬레이션 모델', '<span class="feat-idx">SIM</span>Simulation model'),
 ('data-caption="01 : CAD - 하체 설계도면" aria-label="확대 보기: CAD - 하체 설계도면"', 'data-caption="01 : CAD - lower-body design drawings" aria-label="Enlarge: CAD lower-body design drawings"'),
 ('alt="하체 CAD 설계도면, 인체 오버레이와 관절별 상세"', 'alt="Lower-body CAD drawings with human overlay and per-joint details"'),
 ('<span class="feat-idx">01</span>CAD - 하체 설계도면', '<span class="feat-idx">01</span>CAD - lower-body design drawings'),
 ('data-caption="02 : 사람 외형 → 강화학습 → 프로토타입 → 하드웨어 설계 → Huphy 1.0" aria-label="확대 보기: 사람 외형에서 Huphy 1.0까지의 개발 과정"', 'data-caption="02 : human mesh → reinforcement learning → prototype → hardware design → Huphy 1.0" aria-label="Enlarge: development path from human mesh to Huphy 1.0"'),
 ('alt="사람 외형, 강화학습, 프로토타입, 하드웨어 설계, Huphy 1.0 배포까지의 개발 과정 5단계"', 'alt="Five development stages: human mesh, reinforcement learning, prototype, hardware design, Huphy 1.0 deployment"'),
 ('<span class="feat-idx">02</span>사람 외형 → 강화학습 → 프로토타입 → 하드웨어 설계 → Huphy 1.0', '<span class="feat-idx">02</span>Human mesh → reinforcement learning → prototype → hardware design → Huphy 1.0'),
 ('data-caption="03 : 하체 조립 완료" aria-label="확대 보기: 하체 조립 완료"', 'data-caption="03 : lower body assembled" aria-label="Enlarge: lower body assembled"'),
 ('alt="Huphy 1.0 하체 조립 완료, 세 각도"', 'alt="Assembled Huphy 1.0 lower body from three angles"'),
 ('<span class="feat-idx">03</span>하체 조립 완료', '<span class="feat-idx">03</span>Lower body assembled'),
 ('data-caption="04 : 가공 &amp; 조립 진행" aria-label="확대 보기: 가공 및 조립 진행"', 'data-caption="04 : machining &amp; assembly in progress" aria-label="Enlarge: machining and assembly in progress"'),
 ('alt="부품 가공 및 조립 진행 과정 4컷"', 'alt="Four shots of parts being machined and assembled"'),
 ('<span class="feat-idx">04</span>가공 &amp; 조립 진행', '<span class="feat-idx">04</span>Machining &amp; assembly in progress'),
 ('aria-label="이미지 확대 보기"', 'aria-label="Image viewer"'), ('aria-label="닫기"', 'aria-label="Close"'),
 # members
 ('<span class="m-name">신동엽</span>', '<span class="m-name">Dongyeop Shin</span>'),
 ('기구 H/W 설계, Policy 학습, 부품 제작 총괄', 'Mechanical hardware design, policy training, parts fabrication lead'),
 ('<span class="m-name">김진희</span>', '<span class="m-name">Jinhee Kim</span>'),
 ('전장 설계, 배선 및 전원 계통, 센서와 구동부 전기 연결 총괄', 'Electrical design, wiring and power systems, sensor and actuator electrical integration lead'),
 ('<span class="m-name">황찬희</span>', '<span class="m-name">Chanhee Hwang</span>'),
 ('액추에이터 제어 및 기립과 보행 제어 알고리즘 개발', 'Actuator control, standing and walking control algorithms'),
 ('<span class="m-name">고주현</span>', '<span class="m-name">Juhyun Ko</span>'),
 ('<div class="m-task">컨셉아트, 외형 디자인</div>', '<div class="m-task">Concept art, exterior design</div>'),
 ('<span class="m-name">서동우</span>', '<span class="m-name">Dongwoo Seo</span>'),
 ('다리 구동부 기구 설계 및 초기 제어 실험 참여', 'Leg drivetrain mechanical design, early control experiments'),
 ('<span class="m-name">이지원</span>', '<span class="m-name">Jiwon Lee</span>'),
 ('부품 조립 및 전장 배선 지원', 'Parts assembly and electrical wiring support'),
 ('<span class="m-name">황제연</span>', '<span class="m-name">Jeyeon Hwang</span>'),
 ('휴머노이드 외형 프로토타입, hull 디자인, 관절 위치와 형상 자문', 'Humanoid exterior prototype, hull design, advice on joint placement and form'),
 # footer
 ('aria-label="Autonomous Robot Intelligence Lab 홈페이지"', 'aria-label="Autonomous Robot Intelligence Lab website"'),
 ('alt="ARIL 로고"', 'alt="ARIL logo"'),
 ('<div class="foot-card-sub">서울대학교 자율로봇지능 연구실</div>', '<div class="foot-card-sub">Seoul National University</div>'),
 ('<p>Location : 서울대학교 36동 212호, 자율로봇지능 연구실 (ARILab)<br>서울특별시 관악구 관악로 1</p>',
  '<p>Location : Room 212, Building 36, Seoul National University (ARIL)<br>1 Gwanak-ro, Gwanak-gu, Seoul, Korea</p>'),
 # language toggle + hreflang
 ('<a class="nav-lang" href="en/">EN</a>', '<a class="nav-lang" href="../">KO</a>'),
 ('<link rel="alternate" hreflang="ko" href="https://human-pygmalion.github.io/">\n<link rel="alternate" hreflang="en" href="https://human-pygmalion.github.io/en/">\n<link rel="canonical" href="https://human-pygmalion.github.io/">',
  '<link rel="alternate" hreflang="ko" href="https://human-pygmalion.github.io/">\n<link rel="alternate" hreflang="en" href="https://human-pygmalion.github.io/en/">\n<link rel="canonical" href="https://human-pygmalion.github.io/en/">'),
]
out = src
for row in T:
    ko, en = row[0], row[1]
    want = row[2] if len(row) > 2 else 1
    n = out.count(ko)
    if n != want:
        sys.exit(f'ABORT: expected {want} match(es), got {n}: {ko[:70]}')
    out = out.replace(ko, en)
# shared assets live one level up
out = re.sub(r'(src|poster|href)="assets/', r'\1="../assets/', out)
out = out.replace("url('assets/", "url('../assets/")
left = re.findall(r'[가-힣]+', out)
if left:
    sys.exit(f'ABORT: Korean text left untranslated: {left[:10]}')
(ROOT / 'en' / 'index.html').write_text(out, encoding='utf-8')
print('wrote en/index.html', len(out))
