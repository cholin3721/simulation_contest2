# 제23회 한국 대학생 컴퓨터 시뮬레이션 경진대회

**팀원:** 202444085  
**주제:** K-Logistics 풀필먼트 센터 피킹 프로세스 최적화  
**도구:** AnyLogic Personal Learning Edition

---

## 문제 상황 (AS-IS)

### K-Logistics 풀필먼트 센터 구조

전국 60개 지점(Type A 30개 / Type B 20개 / Type C 10개)의 주문 박스를 피킹하여 파렛타이징하는 물류 센터.

```
[제함기1/2/3] → [S/A: AGV 이동] → [컨베이어] → [봉함기] → [파렛타이저(4슬롯)] → 출하
               → [B/C: 컨베이어]  ↗
```

### 주요 설비 스펙

| 설비 | 수량 | 처리 속도 |
|------|------|----------|
| 제함기 | 3대 | 2초/박스 |
| AGV | 40대 | 1.5 m/s, 적재/하역 5초 |
| 컨베이어 | - | 0.5 m/s |
| 봉함기 | - | 25 박스/분 |
| 파렛타이저 | 2대 × 2슬롯 = 4슬롯 | 15 박스/분 |

### 지점별 주문 규모

| 타입 | 지점 수 | 박스 수 |
|------|---------|--------|
| A | 30개 | 180~200 박스 |
| B | 20개 | 120~150 박스 |
| C | 10개 | 30~80 박스 |

총 예상 박스 수: 약 8,950개

### AS-IS 병목 원인

SKU 구성 확률: S(50%), A(50%), B(30%), C(5%) (독립 사건)

- **P(S 또는 A 포함) = 1 - 0.5×0.5 = 75%**
- 현행 라우팅: `agent.sSkuCnt > 0 || agent.aSkuCnt > 0` → 모두 제함기1로 집중
- 제함기1이 전체 박스의 75%를 단독 처리 → 극심한 병목
- 5시간 PLE 제한 내 처리 완료: **8팔레트(256박스)** = 전체의 약 2.9%

---

## 개선 모델 (TO-BE)

### 개선 방향

1. **제함기 부하 분산**: S/A 박스를 제함기1/2에 고르게 배분
2. **슬롯 배정 최적화**: 지점별 잔여 박스 기반 파렛타이저 슬롯 동적 할당
3. **AGV 운영 효율화**: 불필요한 경로 최소화

### 핵심 비교 지표 (5시간 기준)

- 완료 팔레트 수 (박스 수)
- 시간당 처리량 (팔레트/hr)
- 완료 지점 수 (N / 60)
- 제함기 가동률
- AGV 가동률

---

## 폴더 구조

```
simulation/
├── AS_IS_Model/               ← AS-IS 기준 모델
│   ├── _alp/                  ← XML 소스 (AnyLogic 편집용)
│   │   ├── Agents/Main/       ← 메인 에이전트 (프로세스 로직)
│   │   ├── Agents/AGV/        ← AGV 에이전트
│   │   ├── Agents/Box/        ← 박스 에이전트
│   │   ├── Experiments.xml    ← 시뮬레이션 실행 설정
│   │   └── ModelResources.xml
│   ├── 3d/                    ← AGV·박스 3D 모델 (.dae)
│   ├── database/              ← 내장 HSQLDB (주문 데이터)
│   └── AS_IS_Model.alpx       ← AnyLogic 프로젝트 파일
├── TO_BE_Model/               ← TO-BE 개선 모델 (AS_IS 기반 복사)
│   ├── _alp/
│   │   ├── Agents/Main/
│   │   ├── Agents/AGV/
│   │   ├── Agents/Box/
│   │   ├── Experiments.xml
│   │   └── ModelResources.xml
│   ├── 3d/
│   ├── database/
│   └── TO_BE_Model.alpx       ← AnyLogic 프로젝트 파일 (더블클릭으로 열기)
├── simulation_orders.xlsx     ← 주문 데이터 (60개 지점, SKU별 수량)
├── simulation_rules.md        ← 모델 설계 규칙 메모
├── 제23회 한국 대학생 컴퓨터 시뮬레이션 경진대회 예선 문제_수정.pdf
├── 제23회 한국 대학생 컴퓨터 시뮬레이션 경진대회 안내 및 규칙.pdf
└── README.md
```

## 실행 방법

| 모델 | 파일 경로 |
|------|----------|
| AS-IS (기준) | `AS_IS_Model/AS_IS_Model.alpx` |
| TO-BE (개선) | `TO_BE_Model/TO_BE_Model.alpx` |

1. 위 `.alpx` 파일 더블클릭 → AnyLogic 자동 실행
2. Run → Simulation 실행
3. 좌측 chartArea에서 실시간 지표 확인
4. 5시간(18,000초) 후 자동 종료 (PLE 제한)

> **주의:** AnyLogic Personal Learning Edition은 Material Handling Library 사용 시 시뮬레이션 시간이 5시간으로 제한됩니다.
