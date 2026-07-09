# 최종 컨펌 — 문제_수정.pdf · 모델 · 보고서 · 매뉴얼 · 발표자료 대조

문서 기준: `제23회 한국 대학생 컴퓨터 시뮬레이션 경진대회 예선 문제_수정.pdf`
모델 기준: `To_Be_Model/To_Be_Model.alpx`, `AS_IS_Model/AS_IS_Model.alpx`
재시뮬 기준: **18,000초(5시간) · agvCount=25 · 동일 주문 DB(8,858박스, 60지점)**

---

## 1. 문제 요구사항 vs 구현 대조

| 문제_수정.pdf 요구사항 | 모델 구현 | 상태 |
|---|---|---|
| 프로세스: 제함 → 피킹 → 봉함 → 팔레타이징 | Erector → Station 피킹 → Sealer → Palletizer | OK |
| 60개 지점 (A 30 · B 20 · C 10) | 주문 DB `db.script` 60지점 | OK |
| 총 8,858 박스 | DB 8,858행 | OK |
| S/A급: AGV로 스테이션 피킹 후 투입구 1/2 | `moveByTransporter1/2` + 투입구 이동 | OK |
| B/C급: 제함기3 → 컨베이어 → B/C 스테이션 | 제함기3 라인 + 컨베이어 | OK |
| S/A+B/C 혼합: S/A 피킹 후 투입구3 합류 | 투입구3 합류 + 충돌 제어 로직 | OK |
| 투입구3 충돌 방지 제어 로직 필수 | 경로 용량 제한(`path29/67/68/21`) + `delayToResumeMovement` | OK |
| 제함기 3대 · 30 box/min | Erector 2초/box (=30/min), capacity 4 | OK |
| AGV 초기 40대 → 최적 대수 제안 | AS-IS 40대 / TO-BE 25대(`agvCount`) + 민감도 분석 | OK |
| AGV 1.5 m/s · 적재/하역 5초 | 동일 설정 | OK |
| 컨베이어 0.5 m/s | 동일 | OK |
| 봉함기 25 box/min | 동일 | OK |
| 파렛타이저 2대 × 2슬롯(=4슬롯) · 15 box/min | 4슬롯 · `selectOutput6/7` 슬롯 배정 | OK |
| 팔레트 최대 32박스(4×8) | `batchSizes=[32,32,32,32]` | OK |
| 슬롯 점유: 지점 완료까지 독점 | `slotBranches[4]` + `branchRemainingTotal` | OK |
| 등급 포함확률 독립사건 (합≠100%) | 주문 생성 로직 반영(DB 확정 데이터) | OK |
| 결과보고서 + 애니메이션 + 재현성 | 보고서·매뉴얼·2D/3D 애니메이션·GitHub 재현 | OK |
| 성능지표: 완료시간·처리량·AGV 가동률·슬롯 효율 | 「5시간 처리 실적」 패널에서 측정 | OK |

> **주의(이론값 vs 실측):** 문제의 등급 포함확률(S 50%·A 50%)로 계산한 이론 P(S∪A)=**75%**와, 실제 배포 주문 DB의 S/A 포함 비율 **91.7%(8,120/8,858)** 는 다릅니다. 시뮬레이션·모든 문서는 **실제 주문 DB**를 입력으로 사용하며, 이 차이를 각 문서에 명시했습니다.

---

## 2. 재시뮬 KPI (18,000초, 동일 조건)

| 지표 | AS-IS | TO-BE | 변화 |
|---|---|---|---|
| 완료 팔레트 | 8 | **21** | ×2.6 |
| 완료 박스 | 256 | **672** | +416 (**+162%**) |
| 시간당 처리량 | 1.6/hr | **4.2/hr** | ×2.6 |
| 완료 지점 | 1/60 | **3/60** | ×3 |
| 완료율 | 2.9% | **7.6%** | — |
| AGV 평균 가동률 | 23% | **50%** | ×2.2 |
| 제함기1 / 제함기2 | 100% / 0% | **약 30% / 약 70%** | 부하 재분배 |

측정 위치: AnyLogic 실행 → **Charts 탭 「5시간 처리 실적」** 패널
- `완료: N팔레트 (M박스)` (M = N×32)
- `처리율: X/hr` (팔레트/hr)
- `완료 지점: N / 60`
- AGV 가동률 · 제함기1/2/3 가동률 차트

---

## 3. 코드 정합성 (보고서·PPT 표기 = 실제 코드)

| 항목 | 실제 코드 | 문서 표기 |
|---|---|---|
| 제함기 부하 분산 | `selectOutput1`: `delay_Erector1.size() <= delay_Erector2.size()` | 일치 |
| AGV 최근접 배차 | `-unit.distanceTo(agent)` (`transporter` 아님) | **정정 반영** |
| 배차 블록 수 | **5개** MoveByTransporter (S/A·투입·B/C) | **정정 반영** (3→5) |
| AGV 대수 | `transporterFleet.capacity = agvCount(25)` | 일치 |
| 슬롯 배정 | `selectOutput6/7` · `TYPE_EXIT_NUMBER` · `branchRemainingTotal` | 일치 |
| B존 분기 | `selectOutput5` = 25%×4 확률 분기 (팔레타이저 로직 아님) | 일치 |
| 교착 방지 | `recognizeAllTransporters=true`, `delayToResumeMovement=1s`, 경로용량 제한 | 반영 |
| 시뮬 시간 | `FinalTime=18000`, Stop at specified time | 일치 |

---

## 4. 매뉴얼 정합성

| 항목 | 정정 전 | 정정 후 |
|---|---|---|
| 주문 데이터 위치 | `simulation_orders.xlsx` | **`database/db.script` (SHEET1, 8,858박스)** |
| 실행 파일 | `To_Be_Model/To_Be_Model.alpx` | 유지 (정확) |
| 결과 확인 | 「5시간 처리 실적」 패널 항목 설명 | 유지 (정확) |
| agvCount | 기본 25 · UI 변경 절차 | 유지 (정확) |

---

## 5. 보고서 정합성 (정정 완료)

- 표 8 (AS-IS vs TO-BE): 8팔레트(256박스) → **21팔레트(672박스)**, 1/60 → 3/60, 1.6 → **4.2/hr**, AGV 23% → **50%**, 제함기1/2 = **약 30% / 약 70%**
- 표 9 (민감도): 25대(TO-BE) = **21팔레트 · 4.2/hr · 약 50%**
- 본문: `-transporter` → **`-unit.distanceTo(agent)`**, 이동 블록 3개 → **5개**
- 1.2절·병목 분석·결론: S/A 비율을 **이론 75% · 실제 DB 91.7%** 병기로 정정
- 이론 6,644박스 표기 → **실측 8,120박스(91.7%)** 기준으로 정정

---

## 6. 잔여 확인 권장 (수치 근거 재확인용)

1. **민감도 표 15대 행** (`29팔레트 / 3.8/hr`): 팔레트/hr 환산(29/5=5.8)과 표기(3.8)가 불일치 → 팀 원자료로 재확인 권장.
2. **요약문 "제함기1 부하 37.5%"**: 이론 균등분배 목표값. 실측은 제함기1 약 30% / 제함기2 약 70%로, 부하가 제함기2로 더 이동함 → 발표 시 "실측 기준 부하 재분배"로 설명.
3. PPT 원본이 PowerPoint에서 열려 있어 수정본은 **`...095810.updated.pptx`** 로 저장됨. 원본을 닫은 뒤 이 파일로 교체 사용 권장.

---

## 7. 재현 절차 (제출물 검증)

```bash
git clone https://github.com/cholin3721/simulation_contest2.git
cd simulation_contest2
# AnyLogic PLE 8.9.x 로 열기
#   AS-IS: AS_IS_Model/AS_IS_Model.alpx
#   TO-BE: To_Be_Model/To_Be_Model.alpx (agvCount=25 확인)
# Run → 18,000초 자동 정지 → Charts 탭에서 KPI 캡처
```
