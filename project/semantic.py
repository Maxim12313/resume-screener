import sys
from parser import get_job_sections, get_resume_sections, read_pdf
from sentence_transformers import SentenceTransformer

def similarity(model, text1, text2):
    embed1, embed2 = model.encode([text1, text2])
    res = model.similarity([embed1], [embed2])[0]
    print(res)
    return res

def compare_semantic(resume_sections, job_sections):
    # for conveniece
    r = resume_sections
    j = job_sections

    model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")
    resume_experience = "".join(r["experience"] + r["projects"])
    resume_skills = "".join(r["skills"] + r["technologies"] + r["education"]+r["coursework"])

    experience_similarity = similarity(model, resume_experience, j["responsibilities"])
    skill_similarity = similarity(model, resume_skills, j["requirements"])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("give resume, job")
        exit(1)
    resume = sys.argv[1]
    job = sys.argv[2]

    resume_text = read_pdf(resume)
    job_text = read_pdf(job)

    resume_sections = get_resume_sections(resume_text)
    job_sections = get_job_sections(job_text)

    compare_semantic(resume_sections, job_sections)
