import re
import sys
import pdfplumber


# matches with expr,
def matchSub(expr, text):
    matches = re.findall(expr, text)
    cleaned = re.sub(expr, "", text)
    # return the first match if it exists along with the cleaned text
    return matches[0] if len(matches) else "", cleaned


def get_gpa(text):
    expr = r"[1-4](?:\.[0-9]{1,2})\/4"
    return matchSub(expr, text)


# TODO: add other regex


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("give resume path")
        exit(1)
    name = sys.argv[1]
    with pdfplumber.open(name) as pdf:
        text = pdf.pages[0].extract_text()
        gpa, text = get_gpa(text)
        print(gpa)
        print(text)
