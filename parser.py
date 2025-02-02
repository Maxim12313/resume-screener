import re
import sys
import pdfplumber


def get_gpa(text):
    expr = r"([1-4](\.[0-9]{1,2}))?\/4(\.0)?"
    matches = re.findall(expr, text)
    if len(matches):
        return matches[0][0]
    return ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("give resume path")
        exit(1)
    name = sys.argv[1]
    with pdfplumber.open(name) as pdf:
        text = pdf.pages[0].extract_text()
        gpa = get_gpa(text)
        print(gpa)

        # print(text)
        lines = pdf.pages[0].extract_text_lines()
        # print(lines)
        # line = lines[0]
        # print(line.keys())
        # print(line["text"])
        # print(line["x0"])
        for line in lines:
            print(line["x0"], line["x1"], line["text"])
