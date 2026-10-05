import io
import re
import json
from pathlib import Path
from typing import List, Tuple
from pypdf import PdfReader
import docx
from app.schemas.match import ExtractedCandidateProfile

# Load skills taxonomy for keyword extraction
TAXONOMY_PATH = Path(__file__).resolve().parent.parent.parent.parent / "data" / "taxonomy" / "skills_taxonomy.json"

def load_skills_dictionary() -> dict:
    if not TAXONOMY_PATH.exists():
        # Fallback dictionary if file not mounted
        return {
            "Python": ["python", "python3", "py"],
            "FastAPI": ["fastapi"],
            "Java": ["java", "spring boot", "springboot"],
            "React": ["react", "reactjs", "react.js"],
            "Node.js": ["nodejs", "node.js", "node"],
            "Docker": ["docker", "container"],
            "Kubernetes": ["kubernetes", "k8s"],
            "AWS": ["aws", "amazon web services", "ec2", "s3"],
            "PostgreSQL": ["postgres", "postgresql", "psql"],
            "CI/CD": ["ci/cd", "github actions", "gitlab ci", "jenkins"]
        }
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        mapping = {}
        for item in data.get("skills", []):
            mapping[item["name"]] = item.get("aliases", [item["name"].lower()])
        return mapping

SKILLS_MAP = load_skills_dictionary()

class CVParserService:
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text

    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])

    @classmethod
    def parse_cv_content(cls, raw_text: str) -> ExtractedCandidateProfile:
        text_lower = raw_text.lower()
        
        # 1. Detect candidate skills based on taxonomy aliases
        matched_skills = set()
        for canonical_name, aliases in SKILLS_MAP.items():
            for alias in aliases:
                pattern = r'\b' + re.escape(alias.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    matched_skills.add(canonical_name)
                    break
        
        # 2. Extract potential email
        email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', raw_text)
        email = email_match.group(0) if email_match else None
        
        # 3. Estimate years of experience (regex heuristic for English & Vietnamese)
        exp_match = re.search(r'(\d+)\+?\s*(?:years|năm)(?:\s*(?:kinh nghiệm|of\s*experience))?', text_lower)
        if not exp_match:
            exp_match = re.search(r'kinh nghiệm[:\s]+(\d+)\+?\s*năm', text_lower)
        years = float(exp_match.group(1)) if exp_match else 2.5
        
        # 4. Summary preview
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        candidate_name = lines[0][:50] if lines else "Hồ Sơ Ứng Viên"
        summary = " ".join(lines[1:5])[:300] if len(lines) > 1 else raw_text[:200]

        return ExtractedCandidateProfile(
            name=candidate_name,
            email=email,
            years_of_experience=years,
            detected_skills=sorted(list(matched_skills)),
            summary=summary
        )

cv_parser = CVParserService()
