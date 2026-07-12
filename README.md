# 제23회 한국 대학생 컴퓨터 시뮬레이션 경진대회

**팀원:** 202444085 (인하이트)  
**주제:** K-Logistics 풀필먼트 센터 피킹 프로세스 효율화  
**도구:** AnyLogic Personal Learning Edition 8.9.8

---

## 문제 상황 (AS-IS)

### K-Logistics 풀필먼트 센터 구조

전국 **60개 지점**(Type A 30 · B 20 · C 10)의 주문 **8,858박스**를 제함 → 피킹 → 봉함 → 팔레타이징하는 허브 물류센터.

```
[제함기1/2/3] → [S/A: AGV 이동] → [컨베이어] → [봉함기] → [파렛타이저(4슬롯)] → 출하
               → [B/C: 컨베이어]  ↗
```

### 주요 설비 스펙 (모델 기준)

| 설비 | 수량 | 처리 속도 / 비고 |
|------|------|------------------|
| 제함기 | 3대 | 2초/박스, **capacity 1** (병렬) |
| AGV | AS-IS **40대** / TO-BE **25대** (`agvCount`) | 1.5 m/s, 적재·하역 각 5초 |
| 컨베이어 | - | 0.5 m/s |
| 봉함기 | - | 25 box/min |
| 파렛타이저 | 2대 × 2슬롯 = 4슬롯 | 15 box/min, 팔레트당 최대 32박스 |

### 주문 데이터 (내장 DB)

| 항목 | 값 |
|------|-----|
| 총 박스 | 8,858 |
| 지점 수 | 60 |
| S/A 포함 (실측) | **8,120 (91.7%)** |
| B/C 전용 (실측) | **738 (8.3%)** |
| 저장 위치 | `To_Be_Model/database/db.script` · `AS_IS_Model/database/db.script` |

> **참고:** SKU 독립 확률 이론값 P(S∪A)=**75%**와 실제 DB **91.7%**는 다릅니다. 시뮬레이션은 **실제 주문 DB**를 사용합니다.

### AS-IS 병목 원인

- 라우팅: `agent.sSkuCnt > 0 || agent.aSkuCnt > 0` → **제함기1 집중**
- 제함기2 유휴, S/A 물량이 한 라인에 몰림
- 시뮬레이션 시간: **18,000초 (5시간)**, 종료 조건: **Stop at specified time**

---

## 개선 모델 (TO-BE)

### 코드에 반영된 3가지 개선 (슬라이드 13)

| # | 위치 | 내용 |
|---|------|------|
| 1 | `selectOutput1` | `delay_Erector1.size() <= delay_Erector2.size()` — 제함기 부하 분산 |
| 2 | `moveByTransporter` ×5 | `-unit.distanceTo(agent)` 최근접 배차 · `agvCount = 25` |
| 3 | `selectOutput6/7` | `branchRemainingTotal` · `slotBranches[4]` 동적 슬롯 배정 |

### 안정화 설정 (교착 방지, 발표 부록 권장)

| 항목 | 설정 |
|------|------|
| `transporterFleet` | `recognizeAllTransporters = true` |
| | `delayToResumeMovement = 1초` |
| 경로 용량 | `path29`=2대, `path67/68`=1대, `path21`=2대 |

### B존 라우팅 (주의)

- **`selectOutput5`**: B존 컨베이어 **25%×4 확률 분기**만 담당
- **팔레타이저 슬롯 로직**은 `selectOutput6` / `selectOutput7`에만 있음

### 핵심 비교 지표 (5시간 기준)

- 완료 팔레트·박스 수
- 시간당 처리량 (box/hr)
- 완료 지점 수 (N / 60)
- 제함기·AGV 가동률

> KPI 수치는 AnyLogic **Charts** 탭에서 AS-IS / TO-BE 각각 18,000초 실행 후 확인하세요.  
> 발표 자료 수치 갱신 가이드: [`PRESENTATION_CHECKLIST.md`](PRESENTATION_CHECKLIST.md)

---

## 폴더 구조

```
simulation_contest2/
├── AS_IS_Model/
│   ├── _alp/Agents/Main/       ← 프로세스 로직 (XML)
│   ├── database/               ← 주문 HSQLDB
│   ├── 3d/
│   └── AS_IS_Model.alpx
├── To_Be_Model/                ← TO-BE 개선 모델 (폴더명 대소문자 주의)
│   ├── _alp/Agents/Main/
│   ├── database/
│   ├── 3d/
│   └── To_Be_Model.alpx
├── TO_BE_Model_v2/             ← 별도 프로토타입 (본선 발표 모델 아님)
├── simulation_rules.md
├── PRESENTATION_CHECKLIST.md   ← PPT 슬라이드별 수정 체크리스트
├── K-Logistics_...발표.pptx
└── README.md
```

---

## 실행 방법

### 1. 클론

```bash
git clone https://github.com/cholin3721/simulation_contest2.git
cd simulation_contest2
```

### 2. AnyLogic에서 열기

| 모델 | 파일 |
|------|------|
| AS-IS | `AS_IS_Model/AS_IS_Model.alpx` |
| TO-BE | `To_Be_Model/To_Be_Model.alpx` |

1. `.alpx` 더블클릭 → AnyLogic 실행  
2. TO-BE: Main 화면에서 **`agvCount = 25`** 확인 (UI 파라미터)  
3. **Run → Simulation**  
4. **Charts** 탭에서 KPI 확인  
5. **18,000초** 후 자동 종료 (PLE 5시간 제한)

### 3. 발표 자료와 맞추기

- PPT 문구·수치 수정 목록: [`PRESENTATION_CHECKLIST.md`](PRESENTATION_CHECKLIST.md)
- 코드와 다른 API 표기: 슬라이드의 `transporter` → 실제 코드는 **`unit.distanceTo(agent)`**

---

## 관련 문서

- [`simulation_rules.md`](simulation_rules.md) — 스테이션·랙·C급 존 모델링 규칙
- [`PRESENTATION_CHECKLIST.md`](PRESENTATION_CHECKLIST.md) — 슬라이드별 「이 문장 → 이렇게」 체크리스트
