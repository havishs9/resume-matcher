import os

RESUME_FILE = "samples/resume.txt"
POSTING_FILE = "samples/posting.txt"

SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "html", "css",
    "sql", "bash", "kotlin", "swift", "matlab",
    "git", "github", "linux", "docker", "kubernetes", "aws", "azure",
    "react", "node.js", "spring boot", "flask", "django",
    "postgresql", "mysql", "mongodb", "rest api", "json",
    "pandas", "numpy", "machine learning", "data structures", "algorithms",
    "unit testing", "junit", "agile", "scrum", "object-oriented programming",
    "debugging", "excel", "tableau", "communication", "teamwork"
]


def read_file(path):
    if not os.path.exists(path):
        print("Error: could not find " + path)
        return None

    file = open(path, "r")
    text = file.read()
    file.close()

    if text.strip() == "":
        print("Error: " + path + " is empty")
        return None

    return text


def clean_text(text):
    # swap punctuation for spaces so "Java," still counts as "java"
    # but keep + # . - since skills like c++, c#, node.js use them
    text = text.lower()
    cleaned = ""
    for ch in text:
        if ch.isalnum() or ch in "+#.-":
            cleaned = cleaned + ch
        else:
            cleaned = cleaned + " "

    # the padding lets every skill be checked as " skill " so that
    # "java" doesn't match inside "javascript"
    # (also drops periods at the end of sentences, like "Linux.")
    cleaned = " " + cleaned + " "
    return cleaned.replace(". ", " ")


def find_skills(text):
    text = clean_text(text)
    found = []
    for skill in SKILLS:
        if " " + skill + " " in text:
            found.append(skill)
    return found


def compare_skills(resume_skills, posting_skills):
    matched = []
    missing = []
    for skill in posting_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)
    return matched, missing


def match_percent(matched, posting_skills):
    if len(posting_skills) == 0:
        return 0
    return round(len(matched) / len(posting_skills) * 100)


def print_report(percent, matched, missing):
    print("==============================")
    print("        RESUME MATCHER")
    print("==============================")
    print("Match: " + str(percent) + "%")
    print()

    print("Skills you have (" + str(len(matched)) + "):")
    for skill in matched:
        print("  + " + skill)
    print()

    print("Skills you're missing (" + str(len(missing)) + "):")
    if len(missing) == 0:
        print("  none, nice!")
    for skill in missing:
        print("  - " + skill)


def main():
    resume = read_file(RESUME_FILE)
    posting = read_file(POSTING_FILE)
    if resume is None or posting is None:
        return

    resume_skills = find_skills(resume)
    posting_skills = find_skills(posting)

    if len(posting_skills) == 0:
        print("No known skills found in posting")
        return

    matched, missing = compare_skills(resume_skills, posting_skills)
    percent = match_percent(matched, posting_skills)
    print_report(percent, matched, missing)


main()