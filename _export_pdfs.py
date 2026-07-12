"""Export PPT + report + manual to PDF via Office COM (Windows)."""
from __future__ import annotations

import sys
import time
from pathlib import Path

try:
    import win32com.client
except ImportError:
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "-q"])
    import win32com.client

ROOT = Path(__file__).parent.resolve()

EXPORTS = [
    (
        "PowerPoint.Application",
        "ppt",
        32,
        ROOT / "피킹_프로세스_효율화_및_생산성_극대화_20260709235709.pptx",
        ROOT / "피킹_프로세스_효율화_및_생산성_극대화_20260709235709.pdf",
    ),
    (
        "Word.Application",
        "docx",
        17,
        ROOT / "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트보고서.docx",
        ROOT / "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트보고서.pdf",
    ),
    (
        "Word.Application",
        "docx",
        17,
        ROOT / "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트사용자매뉴얼.docx",
        ROOT / "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트사용자매뉴얼.pdf",
    ),
]


def export_ppt(src: Path, dst: Path, fmt: int) -> None:
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = 1
    pres = app.Presentations.Open(str(src), WithWindow=False)
    pres.SaveAs(str(dst), fmt)
    pres.Close()
    app.Quit()


def export_word(app, src: Path, dst: Path, fmt: int) -> None:
    doc = app.Documents.Open(str(src), ReadOnly=True)
    doc.ExportAsFixedFormat(str(dst), fmt)
    doc.Close(False)


def main() -> None:
    word_app = None
    for prog_id, kind, fmt, src, dst in EXPORTS:
        if not src.exists():
            raise FileNotFoundError(src)
        print(f"export {src.name} -> {dst.name}")
        if kind == "ppt":
            export_ppt(src, dst, fmt)
        else:
            if word_app is None:
                word_app = win32com.client.Dispatch("Word.Application")
                word_app.Visible = False
            export_word(word_app, src, dst, fmt)
        print(f"  OK ({dst.stat().st_size:,} bytes)")
        time.sleep(0.5)
    if word_app:
        word_app.Quit()
    print("All PDF exports finished.")


if __name__ == "__main__":
    main()
