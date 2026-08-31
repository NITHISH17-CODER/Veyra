"""
Resume Analyzer Module — Extracts skills, technologies, education, and experience 
from uploaded resume text/documents using pattern analysis and natural language processing.
"""

import re
from typing import Dict, Any, List

COMMON_TECH_PATTERNS = [
    # Programming Languages
    ("Python", r"\bpython\b"),
    ("JavaScript", r"\bjavascript\b|\bjs\b"),
    ("TypeScript", r"\btypescript\b|\bts\b"),
    ("Java", r"\bjava\b"),
    ("C++", r"\bc\+\+\b"),
    ("C#", r"\bc#\b"),
    ("Go", r"\bgolang\b|\bgo\b"),
    ("Rust", r"\brust\b"),
    ("HTML & CSS", r"\bhtml5?\b|\bcss3?\b"),
    ("SQL", r"\bsql\b|\bpostgresql\b|\bmysql\b|\bsqlite\b"),
    
    # Frameworks & Libraries
    ("React", r"\breact(?:\.js)?\b"),
    ("Node.js", r"\bnode(?:\.js)?\b"),
    ("Express", r"\bexpress(?:\.js)?\b"),
    ("Next.js", r"\bnext(?:\.js)?\b"),
    ("Vue.js", r"\bvue(?:\.js)?\b"),
    ("FastAPI", r"\bfastapi\b"),
    ("Django", r"\bdjango\b"),
    ("Flask", r"\bflask\b"),
    ("Spring Boot", r"\bspring(?:\s+boot)?\b"),
    ("Tailwind CSS", r"\btailwind(?:\s+css)?\b"),
    ("Bootstrap", r"\bbootstrap\b"),

    # AI / Data Science
    ("Pandas", r"\bpandas\b"),
    ("NumPy", r"\bnumpy\b"),
    ("Scikit-Learn", r"\bscikit-learn\b|\bsklearn\b"),
    ("TensorFlow", r"\btensorflow\b"),
    ("PyTorch", r"\bpytorch\b"),
    ("Machine Learning", r"\bmachine\s+learning\b|\bml\b"),
    ("Deep Learning", r"\bdeep\s+learning\b|\bdl\b"),
    ("Natural Language Processing (NLP)", r"\bnlp\b|\bnatural\s+language\s+processing\b"),
    ("Computer Vision", r"\bcomputer\s+vision\b"),
    ("LLMs", r"\bllms?\b|\blarge\s+language\s+models?\b"),
    ("RAG Systems", r"\brag\b|\bretrieval\s+augmented\s+generation\b"),

    # Cloud & DevOps
    ("Docker", r"\bdocker\b"),
    ("Kubernetes", r"\bkubernetes\b|\bk8s\b"),
    ("AWS", r"\baws\b|\bamazon\s+web\s+services\b"),
    ("Azure", r"\bazure\b"),
    ("GCP", r"\bgcp\b|\bgoogle\s+cloud\b"),
    ("CI/CD Pipelines", r"\bci/cd\b|\bgithub\s+actions\b|\bjenkins\b"),
    ("Git & GitHub", r"\bgit\b|\bgithub\b|\bgitlab\b"),

    # Cybersecurity
    ("Network Security", r"\bnetwork\s+security\b"),
    ("Penetration Testing", r"\bpen\s*testing\b|\bpenetration\s+testing\b"),
    ("Cryptography", r"\bcryptography\b"),
    ("Ethical Hacking", r"\bethical\s+hacking\b|\bwireshark\b"),
    ("Log Analysis", r"\bsiem\b|\bsoar\b|\blog\s+analysis\b"),
]


def extract_text_from_file_content(file_bytes: bytes, filename: str) -> str:
    """Extract plain text from uploaded file bytes (PDF, DOCX, TXT)."""
    text = ""
    lower_fname = filename.lower()

    if lower_fname.endswith(".txt"):
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            return ""

    if lower_fname.endswith(".pdf"):
        try:
            import io
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
            return text
        except Exception:
            pass

    if lower_fname.endswith(".docx") or lower_fname.endswith(".doc"):
        try:
            import io
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            for p in doc.paragraphs:
                text += p.text + "\n"
            return text
        except Exception:
            pass

    # Fallback to string decoding with ascii filter
    try:
        raw_str = file_bytes.decode("latin-1", errors="ignore")
        # Extract readable ASCII chunks
        words = re.findall(r"[A-Za-z0-9+#.-]{2,}", raw_str)
        return " ".join(words)
    except Exception:
        return ""


def analyze_resume_text(resume_text: str) -> Dict[str, Any]:
    """
    Parses resume text and extracts evidence of skills, technologies, 
    education keywords, and experience summary.
    """
    if not resume_text or not isinstance(resume_text, str):
        return {
            "skills": [],
            "technologies": [],
            "education_found": [],
            "experience_keywords": [],
            "raw_snippet": "",
        }

    clean_text = resume_text.lower()
    extracted_skills: List[Dict[str, Any]] = []
    extracted_tech: List[str] = []

    for name, pattern in COMMON_TECH_PATTERNS:
        matches = re.findall(pattern, clean_text, re.IGNORECASE)
        if matches:
            count = len(matches)
            # Estimate confidence & proficiency level based on occurrence & context
            confidence = min(0.95, 0.70 + (count * 0.05))
            prof = 3 if count >= 3 else 2
            extracted_skills.append({
                "name": name,
                "proficiency": prof,
                "source": "resume",
                "evidence_text": f"Found {count} reference(s) in resume text.",
                "confidence_score": round(confidence, 2),
            })
            extracted_tech.append(name)

    # Detect Education Keywords
    education_keywords = []
    if "b.tech" in clean_text or "bachelor of technology" in clean_text:
        education_keywords.append("B.Tech")
    if "b.e." in clean_text or "bachelor of engineering" in clean_text:
        education_keywords.append("B.E.")
    if "bca" in clean_text or "bachelor of computer applications" in clean_text:
        education_keywords.append("BCA")
    if "mca" in clean_text or "master of computer applications" in clean_text:
        education_keywords.append("MCA")
    if "computer science" in clean_text or "cse" in clean_text:
        education_keywords.append("Computer Science")

    snippet = resume_text[:300].strip().replace("\n", " ")

    return {
        "skills": extracted_skills,
        "technologies": extracted_tech,
        "education_found": education_keywords,
        "total_skills_detected": len(extracted_skills),
        "raw_snippet": snippet,
    }
