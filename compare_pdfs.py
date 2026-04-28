import fitz
import sys
import difflib

def extract_text(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = []
        for page in doc:
            text.append(page.get_text())
        return "\n".join(text)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

file1 = "제23회 한국 대학생 컴퓨터 시뮬레이션 경진대회 예선 문제.pdf"
file2 = "제23회 한국 대학생 컴퓨터 시뮬레이션 경진대회 예선 문제_수정.pdf"

text1 = extract_text(file1).splitlines()
text2 = extract_text(file2).splitlines()

# Clean empty lines for better diff
text1 = [line.strip() for line in text1 if line.strip()]
text2 = [line.strip() for line in text2 if line.strip()]

diff = difflib.unified_diff(text1, text2, fromfile='Original', tofile='Modified', lineterm='')

diff_out = list(diff)
if not diff_out:
    print("No textual differences found.")
else:
    for line in diff_out:
        print(line)
