"""Sync report & manual with final PPT KPIs and sensitivity results."""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
REPORT = ROOT / "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트보고서.docx"
MANUAL = ROOT / "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트사용자매뉴얼.docx"

ASIS = dict(pallets=8, boxes=256, rate=1.6, branches=1, agv=23, pct=2.9)
TOBE = dict(pallets=21, boxes=672, rate=4.2, branches=3, agv=50, pct=7.6)
INC_PCT = round((TOBE["boxes"] - ASIS["boxes"]) / ASIS["boxes"] * 100)

COMMON = [
    ("simulation_orders.xlsx  ← 모델(.alpx)과 동일 경로에 위치해야 함",
     "database/db.script (모델 내장 HSQLDB · SHEET1 8,858건)"),
    ("simulation_orders.xlsx", "database/db.script (SHEET1)"),
    ("−transporter.distanceTo(agent)", "−unit.distanceTo(agent)"),
    ("TransportTo 블록의 TransporterRating", "MoveByTransporter 블록의 TransporterRating"),
    ("총 3개의 이동 블록에 적용", "총 5개의 MoveByTransporter 블록에 적용"),
    ("S/A 박스(75%)", "S/A 박스(이론 75% · DB 91.7%)"),
    ("S/A 박스(약 75%)", "S/A 박스(DB 91.7% · 이론 75%)"),
    ("약 75%)를 제함기1", "DB 91.7% · 이론 75%)를 제함기1"),
    ("S/A 박스 75% 단독 처리", "S/A 박스 91.7% (DB) · 이론 75% 단독 처리"),
    ("6,644 박스", "8,120 박스 (DB 실측 91.7%)"),
    ("6,644개", "8,120개 (91.7%)"),
    ("S/A 박스 6,644개", "S/A 박스 8,120개"),
    ("75% → 약 37.5%", "100% → 약 30%"),
    ("정적 슬롯 배정", "기본 슬롯 로직(selectOutput6)"),
    ("파렛타이저 슬롯 배정 시", "selectOutput6/7 슬롯 배정 시"),
]

KPI = [
    ("20 팔레트 (640 박스)", f"{TOBE['pallets']} 팔레트 ({TOBE['boxes']} 박스)"),
    ("8 팔레트 (256 박스)", f"{ASIS['pallets']} 팔레트 ({ASIS['boxes']} 박스)"),
    ("640 박스", f"{TOBE['boxes']} 박스"),
    ("4.0/hr", f"{TOBE['rate']} 팔레트/hr"),
    ("4.0 박스/hr", f"{TOBE['rate']} 팔레트/hr"),
    ("약 44%", f"약 {TOBE['agv']}%"),
    ("23% → 44%", f"{ASIS['agv']}% → {TOBE['agv']}%"),
    ("약 94%", "약 30%"),
    ("약16%", "약 70%"),
    ("7.2%", f"{TOBE['pct']}%"),
    ("+150%", f"+{INC_PCT}%"),
]

SENSITIVITY = [
    ("15대, 20대, 25대, 30대, 35대, 40대의 6개 수준",
     "15대, 20대, 25대, 35대의 4개 수준"),
    ("시간당 처리량 (박스/hr)", "시간당 처리량 (팔레트/hr)"),
    ("29 팔레트", "14 팔레트"),
    ("3.8/hr", "2.8 팔레트/hr"),
    ("약 27%", "약 80%"),
    ("약 45%", "약 35%"),
    ("0.6/hr", "0.4 팔레트/hr"),
    ("약 34%", "약 30%"),
    ("80%정상", "80%후반 교착 · 운영 불가"),
    ("35%교착 발생운영 불가", "35%1/3 지점 교착 · 운영 불가"),
    ("30%교착 발생운영 불가", "30%초반 교착 · 운영 불가"),
    ("정상( 기준시나리오)", "정상 · 기준 시나리오"),
    (
        "AGV 대수가 지나치게 많으면 동선 충돌 및 대기로 인해 처리량이 오히려 감소하거나 정체된다. "
        "반면 너무 적으면 박스가 제함기에서 생성되어도 수령 AGV가 없어 지연이 발생한다. "
        "25대는 이 두 극단 사이에서 처리량을 최대화하는 최적 대수로 선정하였다.",
        "15·20·35대 실험에서는 교착으로 무진행 구간이 발생하였고, 25대만 5시간(18,000초) 끝까지 정상 운영되었다. "
        "대수가 지나치게 많거나 적으면 교차로 혼잡·교착이 발생하며, 25대가 처리량·가동률의 실용 최적점이다.",
    ),
]

# Apply after generic '정상' would break TO-BE row — use row-specific trailing cell text.
SENSITIVITY_ROW_NOTES = []

MANUAL_EXTRA = [
    ("25~35", "15~35 (최적 25)"),
    (
        "AGV 운용 대수 (민감도 분석 핵심)",
        "AGV 운용 대수 (민감도: 15·20·25·35 실험, 기준 25)",
    ),
    (
        "③ 상단 ▶ Run 버튼 클릭 → Simulation 실험 선택 → 실행",
        "③ 상단 ▶ Run 버튼 클릭 → Simulation 실험 선택 → 실행 (Final time 18,000초)",
    ),
]

STABILIZATION_BLOCK = (
    "■ AGV 교착 방지(안정화) "
    "recognizeAllTransporters=true, delayToResumeMovement=1초, "
    "path21·path29=2대, path67·path68=1대 용량 제한."
)

REPORT_STABILIZATION_INSERT_AFTER = ""

EXEC_SUMMARY_ADD = (
    "④ AGV 교착 방지: transporterFleet 안정화 설정 및 교차로 경로 용량 제한으로 "
    "민감도 실험(15·20·25·35대)과 기준 시나리오를 재현한다."
)


def replace_once(text: str, old: str, new: str) -> tuple[str, bool]:
    idx = text.find(old)
    if idx == -1:
        return text, False
    return text[:idx] + new + text[idx + len(old) :], True


def apply_pairs(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def patch_docx(path: Path, pairs: list[tuple[str, str]], *, once: list[tuple[str, str]] | None = None) -> int:
    with zipfile.ZipFile(path, "r") as zin:
        buf = {}
        changed = 0
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                xml = data.decode("utf-8")
                before = xml
                xml = apply_pairs(xml, pairs)
                if once:
                    for old, new in once:
                        xml, _ = replace_once(xml, old, new)
                if xml != before:
                    changed += 1
                data = xml.encode("utf-8")
            buf[item.filename] = (item, data)
    with zipfile.ZipFile(path, "w") as zout:
        for fname, (item, data) in buf.items():
            zout.writestr(item, data)
    return changed


def fix_table9_segment(xml: str) -> str:
    marker = "AGV 대수별 성능 비교"
    idx = xml.find(marker)
    if idx < 0:
        return xml
    end = xml.find("4. 결론", idx)
    if end < 0:
        end = idx + 20000
    seg = xml[idx:end]
    seg = seg.replace("<w:t>정상</w:t>", "<w:t>후반 교착 · 운영 불가</w:t>", 1)
    seg = seg.replace("<w:t>교착 발생</w:t>", "<w:t>1/3 지점 교착</w:t>", 1)
    seg = seg.replace("<w:t>교착 발생</w:t>", "<w:t>초반 교착</w:t>", 1)
    seg = seg.replace("정상( 기준시나리오)", "정상 · 기준 시나리오")
    seg = seg.replace(
        "25대는 이 두 극단 사이에서 처리량을 최대화하는 최적 대수로 선정하였다.",
        "15·20·35대 실험에서는 교착으로 무진행 구간이 발생하였고, 25대만 5시간(18,000초) 끝까지 정상 운영되었다. "
        "대수가 지나치게 많거나 적으면 교차로 혼잡·교착이 발생하며, 25대가 처리량·가동률의 실용 최적점이다.",
    )
    return xml[:idx] + seg + xml[end:]


def fixup_report_xml(xml: str) -> str:
    """Idempotent fixes for report after bulk replace."""
    fixes = [
        ("0.2 팔레트/hr", "0.4 팔레트/hr"),
        ("12 팔레트", "14 팔레트"),
        ("1/3 지점 교착운영 불가", "1/3 지점 교착 · 운영 불가"),
        ("초반 교착운영 불가", "초반 교착 · 운영 불가"),
        ("정상( 기준시나리오)", "정상 · 기준 시나리오"),
    ]
    for old, new in fixes:
        xml = xml.replace(old, new)
    xml = fix_table9_segment(xml)
    return xml


def main() -> None:
    report_pairs = COMMON + KPI + SENSITIVITY
    # 20행: 두 번째 '측정 불가'만 처리율로 (첫 번째는 팔레트)
    report_once = [
        ("측정 불가", "8 팔레트"),
        ("측정 불가", "1.6 팔레트/hr"),
    ]

    manual_pairs = COMMON + KPI + MANUAL_EXTRA

    r = patch_docx(REPORT, report_pairs, once=report_once)
    m = patch_docx(MANUAL, manual_pairs)

    # Conclusion + stabilization mention in report body text
    with zipfile.ZipFile(REPORT, "r") as zin:
        xml = zin.read("word/document.xml").decode("utf-8")
    xml = xml.replace(
        "세 가지 개선을 통해 병목을 해소",
        "세 가지 운영 개선과 안정화를 통해 병목을 해소",
    )
    if "recognizeAllTransporters" not in xml:
        xml = xml.replace(
            "TO-BE는 세 가지 개선을 모두 적용한 최종 개선 모델이다.",
            "TO-BE는 세 가지 운영 개선과 AGV 교착 방지(안정화)를 적용한 최종 개선 모델이다. "
            + STABILIZATION_BLOCK,
        )
    if EXEC_SUMMARY_ADD.split("④")[1][:8] not in xml:
        xml = xml.replace(
            "슬롯 점유 효율을 향상시킨다.",
            "슬롯 점유 효율을 향상시킨다. " + EXEC_SUMMARY_ADD,
        )
    with zipfile.ZipFile(REPORT, "r") as zin:
        buf = {i.filename: (i, zin.read(i.filename)) for i in zin.infolist()}
    buf["word/document.xml"] = (buf["word/document.xml"][0], xml.encode("utf-8"))
    with zipfile.ZipFile(REPORT, "w") as zout:
        for item, data in buf.values():
            zout.writestr(item, data)

    # Final idempotent report fixups (always apply)
    with zipfile.ZipFile(REPORT, "r") as zin:
        buf = {i.filename: (i, zin.read(i.filename)) for i in zin.infolist()}
    xml = buf["word/document.xml"][1].decode("utf-8")
    fixed = fixup_report_xml(xml)
    buf["word/document.xml"] = (buf["word/document.xml"][0], fixed.encode("utf-8"))
    with zipfile.ZipFile(REPORT, "w") as zout:
        for item, data in buf.values():
            zout.writestr(item, data)

    # Manual: sensitivity + stabilization note
    with zipfile.ZipFile(MANUAL, "r") as zin:
        xml = zin.read("word/document.xml").decode("utf-8")
    manual_note = (
        "▶ 민감도 실험 (agvCount)\n"
        "15 · 20 · 25 · 35대 각각 18,000초 실행 후 Charts 「5시간 처리 실적」 캡처. "
        "25대가 TO-BE 기준 시나리오.\n"
        "▶ 안정화 설정 (TO-BE)\n"
        "recognizeAllTransporters=true · delayToResumeMovement=1초 · "
        "path21·path29=2 · path67·path68=1"
    )
    if "민감도 실험 (agvCount)" not in xml:
        xml = xml.replace("4. 결과 확인", manual_note + "\n4. 결과 확인")
        with zipfile.ZipFile(MANUAL, "r") as zin:
            buf = {i.filename: (i, zin.read(i.filename)) for i in zin.infolist()}
        buf["word/document.xml"] = (buf["word/document.xml"][0], xml.encode("utf-8"))
        with zipfile.ZipFile(MANUAL, "w") as zout:
            for item, data in buf.values():
                zout.writestr(item, data)

    print(f"report patched: {r}, manual patched: {m}")

    # extract text for verification
    for p in (REPORT, MANUAL):
        xml = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
        out = ROOT / f"_extract_{p.stem}.txt"
        import re

        text = re.sub(r"</w:p>", "\n", re.sub(r"<[^>]+>", "", xml))
        out.write_text(text, encoding="utf-8")
        print("wrote", out.name)


if __name__ == "__main__":
    main()
