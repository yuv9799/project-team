import re

SKILL_ALIASES = {
    "react": ["react", "next.js", "nextjs"], "machine learning": ["machine learning", "ml", "ai"],
    "python": ["python"], "backend": ["backend", "api", "fastapi", "node"], "database": ["database", "postgres", "sql", "mongodb"],
    "ui/ux": ["ui", "ux", "figma", "design"], "computer vision": ["computer vision", "face recognition", "image recognition"],
    "nlp": ["nlp", "natural language", "llm"], "docker": ["docker"], "typescript": ["typescript"],
}

def extract_project(text: str):
    lower = text.lower()
    skills = []
    for canonical, aliases in SKILL_ALIASES.items():
        if any(re.search(r"\b" + re.escape(a) + r"\b", lower) for a in aliases):
            skills.append(canonical)
    roles = []
    if any(x in lower for x in ["frontend", "react", "web dashboard"]): roles.append("Frontend Developer")
    if any(x in lower for x in ["backend", "api"]): roles.append("Backend Developer")
    if any(x in lower for x in ["ml", "machine learning", "ai", "computer vision", "nlp"]): roles.append("ML Engineer")
    if any(x in lower for x in ["ui", "ux", "design"]): roles.append("UI/UX Designer")
    return {"skills": sorted(set(skills)), "roles": sorted(set(roles)), "category": "AI / Web Development" if any(x in lower for x in ["ai", "ml", "react", "web"]) else "Other"}
