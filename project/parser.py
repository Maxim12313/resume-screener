from collections import defaultdict
import re
import sys
import pdfplumber

def read_pdf(name):
    with pdfplumber.open(name) as pdf:
        return pdf.pages[0].extract_text()


# matches with expr,
def matchSub(expr, text):
    matches = re.findall(expr, text)
    cleaned = re.sub(expr, "", text)
    # return the first match if it exists along with the cleaned text
    return matches[0] if len(matches) else "", cleaned

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


# gives back the section title we're in now
# if this isn't a section, return ""
def section_title(line, titles):
    words = line.lower().split()
    if len(words) > 2:
        return ""
    for word in words:
        if word in titles:
            return word
    return ""


def sections(lines, titles):
    sectionData = defaultdict(list)

    section = ""
    for line in lines:
        if not len(line):
            continue
        line = line.lstrip()
        res = section_title(line, titles)
        if res:
            section = res
        elif len(section):
            sectionData[section].append(line)

    return sectionData


def get_resume_sections(text):
    titles = [
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
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^\x00-\x7f]", " ", text)
    return sections(text.split("\n"), titles)

def get_job_sections(text):
    titles = [
        "about",
        "description",
        "responsibilities",
        "requirements",
        "benefits",
        "1benefits",
    ]
    return sections(text.split("\n"), titles)

def clean(text):
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^\x00-\x7f]", " ", text)
    return text

def read_pdf(name):
    with pdfplumber.open(name) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text();
        return clean(text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("give resume path")
        exit(1)
    name = sys.argv[1]
    text = read_pdf(name)
    sections = get_job_sections(text)
    for key in sections:
        print(key)
        print(sections[key])
        print()
    # print(sections)

