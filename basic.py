import re
import sys
import pdfplumber


def get_gpa(text):
    expr = r"([1-4](\.[0-9]{1,2}))?\/4(\.0)?"
    matches = re.findall(expr, text)  # expr, replace, text
    text = re.sub(expr, "", text)

    # If I matched anything
    if len(matches):
        # combine all matched groups of the first occurence
        return matches[0], text
    return "", text


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
