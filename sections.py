import pdfplumber
import sys
from collections import defaultdict

SECTION_TITLES = [
    "employment",
    "education",
    "experience",
    "projects",
    "skills",
    "coursework",
    "research",
    "achievements",
    "technologies",
]


# gives back the section title we're in now
# if this isn't a section, return ""
def section_title(line):
    words = line["text"].lower().split()
    if len(words) > 2:
        return ""
    for word in words:
        if word in SECTION_TITLES:
            return word
    return ""


def get_sections(lines):
    sectionData = defaultdict(list)

    section = ""
    for line in lines:
        if not len(line):
            continue
        res = section_title(line)
        if res:
            section = res
        elif len(section):
            sectionData[section].append(line["text"])

    return sectionData


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("give resume path")
        exit(1)

    name = sys.argv[1]
    with pdfplumber.open(name) as pdf:
        lines = pdf.pages[0].extract_text_lines()
        data = get_sections(lines)
        for key in data:
            print(key)
            for line in data[key]:
                print(line)
            print()
