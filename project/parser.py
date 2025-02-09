from collections import defaultdict
import re
import sys
from utils import read_pdf


# matches with expr,
def matchSub(expr, text):
    matches = re.findall(expr, text)
    cleaned = re.sub(expr, "", text)
    # return the first match if it exists along with the cleaned text
    return matches[0] if len(matches) else "", cleaned


# TODO: add other regex


def get_gpa(text):
    expr = r"[1-4](?:\.[0-9]{1,2})\/4"
    return matchSub(expr, text)


def get_email(text):
    expr = r"(?:(?:[\w-]+(?:\.[\w-]+)*)@(?:(?:[\w-]+\.)*\w[\w-]{0,66})\.(?:[a-z]{2,6}(?:\.[a-z]{2})?))"
    return matchSub(expr, text)


# and cleans
def get_details(text):
    details = dict()
    details["gpa"], text = get_gpa(text)
    details["email"], text = get_email(text)
    return details, text


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
    words = line.lower().split()
    if len(words) > 2:
        return ""
    for word in words:
        if word in SECTION_TITLES:
            return word
    return ""


def sections(lines):
    sectionData = defaultdict(list)

    section = ""
    for line in lines:
        if not len(line):
            continue
        res = section_title(line)
        if res:
            section = res
        elif len(section):
            sectionData[section].append(line)

    return sectionData


def get_sections(text):
    return sections(text.split("\n"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("give resume path")
        exit(1)
    name = sys.argv[1]
    text = read_pdf(name)
    details, text = get_details(text)
    sections = get_sections(text)
    # print(sections)
    # print(details)
