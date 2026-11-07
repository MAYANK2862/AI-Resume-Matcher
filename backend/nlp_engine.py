"""
NLP Engine for Skills Extraction, Job Matching, and Improvement Suggestions
"""
import re
from typing import List, Dict, Any, Set, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Comprehensive Skills Dictionary categorized
SKILLS_TAXONOMY: Dict[str, List[str]] = {
    "Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C", "Go", "Golang",
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "R", "Scala", "Dart", "SQL", "Shell",
        "Bash", "PowerShell", "HTML", "CSS", "HTML5", "CSS3", "Sass", "MATLAB", "Perl"
    ],
    "Frontend": [
        "React", "Next.js", "Vue.js", "Nuxt.js", "Angular", "Svelte", "Tailwind CSS",
        "Bootstrap", "Material-UI", "Redux", "Zustand", "Webpack", "Vite", "GraphQL",
        "HTML/CSS", "Responsive Design", "WebSockets", "Three.js", "Storybook", "Jest",
        "Cypress", "Playwright"
    ],
    "Backend & Frameworks": [
        "FastAPI", "Flask", "Django", "Node.js", "Express.js", "NestJS", "Spring Boot",
        "ASP.NET", ".NET Core", "Ruby on Rails", "Laravel", "REST APIs", "GraphQL",
        "gRPC", "Microservices", "Celery", "Kafka", "RabbitMQ", "Event-Driven Architecture",
        "WebSockets", "Socket.io", "OAuth", "JWT", "Swagger", "OpenAPI"
    ],
    "Databases & Storage": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra", "DynamoDB",
        "Elasticsearch", "Firebase", "Supabase", "Oracle", "SQL Server", "Neo4j",
        "Prisma", "SQLAlchemy", "Snowflake", "BigQuery"
    ],
    "Cloud & DevOps": [
        "AWS", "Amazon Web Services", "Microsoft Azure", "Google Cloud (GCP)", "Docker",
        "Kubernetes", "CI/CD", "GitHub Actions", "GitLab CI", "Jenkins", "Terraform",
        "Ansible", "Linux", "Nginx", "Apache", "Helm", "Prometheus", "Grafana",
        "CloudWatch", "Serverless", "CloudFormation", "ArgoCD"
    ],
    "AI, ML & Data Science": [
        "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
        "Large Language Models", "LLMs", "Generative AI", "RAG", "LangChain", "LlamaIndex",
        "PyTorch", "TensorFlow", "Keras", "Scikit-learn", "Pandas", "NumPy", "OpenCV",
        "Computer Vision", "Hugging Face", "Transformers", "Data Science", "Data Analysis",
        "Data Visualization", "Matplotlib", "Seaborn", "Tableau", "Power BI", "Apache Spark",
        "Prompt Engineering", "Fine-Tuning", "Vector Databases", "ChromaDB", "Pinecone", "Milvus"
    ],
    "Methodologies & Architecture": [
        "System Design", "Object-Oriented Programming", "OOP", "Data Structures",
        "Algorithms", "Design Patterns", "Clean Code", "Test-Driven Development (TDD)",
        "Agile", "Scrum", "Git", "GitHub", "Version Control", "Unit Testing",
        "Integration Testing", "Continuous Integration", "CI", "Continuous Deployment", "CD",
        "Performance Optimization", "Scalability", "Security"
    ],
    "Soft Skills & Management": [
        "Problem Solving", "Critical Thinking", "Team Leadership", "Communication",
        "Project Management", "Cross-Functional Collaboration", "Mentorship",
        "Time Management", "Adaptability", "Stakeholder Management", "Code Reviews",
        "Technical Writing", "Analytical Skills"
    ]
}

# Alias / Normalization Map
SKILL_ALIASES: Dict[str, str] = {
    "k8s": "Kubernetes",
    "reactjs": "React",
    "react.js": "React",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    "angularjs": "Angular",
    "fastapi": "FastAPI",
    "fast-api": "FastAPI",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud (GCP)",
    "google cloud": "Google Cloud (GCP)",
    "google cloud platform": "Google Cloud (GCP)",
    "azure": "Microsoft Azure",
    "microsoft azure": "Microsoft Azure",
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "dl": "Deep Learning",
    "deep learning": "Deep Learning",
    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",
    "llm": "Large Language Models",
    "llms": "Large Language Models",
    "genai": "Generative AI",
    "generative ai": "Generative AI",
    "rag": "RAG",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "restful": "REST APIs",
    "rest api": "REST APIs",
    "rest apis": "REST APIs",
    "restful apis": "REST APIs",
    "graphql": "GraphQL",
    "docker": "Docker",
    "sqlite": "SQLite",
    "sqlite3": "SQLite",
    "express": "Express.js",
    "expressjs": "Express.js",
    "express.js": "Express.js",
    "spring": "Spring Boot",
    "springboot": "Spring Boot",
    "spring boot": "Spring Boot",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "golang": "Go",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scipy": "SciPy",
    "git": "Git",
    "github": "GitHub",
    "system design": "System Design",
    "tdd": "Test-Driven Development (TDD)",
    "agile": "Agile",
    "scrum": "Scrum"
}


def build_skill_patterns():
    """Build normalized search list sorted by phrase length descending."""
    unique_skills = set()
    for cat_skills in SKILLS_TAXONOMY.values():
        for s in cat_skills:
            unique_skills.add(s)

    # Add all aliases
    for alias in SKILL_ALIASES.keys():
        unique_skills.add(alias)

    # Sort descending by length so multi-word terms like "Machine Learning" match before "Learning"
    sorted_skills = sorted(list(unique_skills), key=lambda x: len(x), reverse=True)
    return sorted_skills


ALL_SKILL_PATTERNS = build_skill_patterns()


def extract_skills(text: str) -> List[str]:
    """
    Extract skills from text with word boundary checks and synonym normalization.
    """
    if not text:
        return []

    found_normalized: Set[str] = set()
    lower_text = text.lower()

    for skill in ALL_SKILL_PATTERNS:
        pattern_lower = skill.lower()
        
        # Word-boundary pattern
        # Special characters handling for C++, C#, .NET, CI/CD, Node.js
        escaped = re.escape(pattern_lower)
        if skill in ["C++", "c++"]:
            regex = r'(?:^|[\s,;:(/])c\+\+(?:[\s,;:!.)/]|$)'
        elif skill in ["C#", "c#"]:
            regex = r'(?:^|[\s,;:(/])c#(?:[\s,;:!.)/]|$)'
        elif skill in [".NET", ".net", ".NET Core"]:
            regex = r'(?:^|[\s,;:(/])\.net(?:\s*core)?(?:[\s,;:!.)/]|$)'
        elif skill.lower() in ["c"]:
            regex = r'(?:^|[\s,;:(/])c(?:[\s,;:!.)/]|$)'
        elif skill.lower() in ["r"]:
            regex = r'(?:^|[\s,;:(/])r(?:[\s,;:!.)/]|$)'
        elif skill.lower() in ["go"]:
            regex = r'\bgo\b(?!\s+(?:to|ahead|through|on|back|over))'
        else:
            regex = r'\b' + escaped + r'\b'

        if re.search(regex, lower_text):
            # Map to canonical skill name
            canonical = SKILL_ALIASES.get(pattern_lower)
            if not canonical:
                # Find matching case in taxonomy
                for cat_skills in SKILLS_TAXONOMY.values():
                    for s in cat_skills:
                        if s.lower() == pattern_lower:
                            canonical = s
                            break
                    if canonical:
                        break
            if not canonical:
                canonical = skill.title()
            
            found_normalized.add(canonical)

    return sorted(list(found_normalized))


def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Compute Cosine Similarity between Resume and Job Description using TF-IDF.
    Returns score out of 100.
    """
    if not text1.strip() or not text2.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        # Cosine similarity for full documents usually ranges from 0.15 to 0.75
        # Scale moderately to reflect practical match percentage
        normalized_sim = min(100.0, max(0.0, sim * 125.0))
        return round(float(normalized_sim), 1)
    except Exception:
        return 40.0


def match_resume_to_job(
    resume_text: str,
    job_description: str,
    candidate_skills: List[str] = None
) -> Dict[str, Any]:
    """
    Complete matching pipeline:
    - Extracts job skills and candidate skills
    - Calculates Skill Match %
    - Calculates Semantic Similarity %
    - Determines Matched & Missing skills
    - Generates Composite Score and detailed actionable suggestions
    """
    if candidate_skills is None:
        candidate_skills = extract_skills(resume_text)
    
    job_skills = extract_skills(job_description)

    cand_set = {s.lower(): s for s in candidate_skills}
    job_set = {s.lower(): s for s in job_skills}

    matched_keys = set(cand_set.keys()).intersection(set(job_set.keys()))
    missing_keys = set(job_set.keys()) - set(cand_set.keys())

    matched_skills = sorted([job_set[k] for k in matched_keys])
    missing_skills = sorted([job_set[k] for k in missing_keys])

    # Skill match score calculation
    if job_skills:
        skill_match_score = (len(matched_skills) / len(job_skills)) * 100.0
    else:
        skill_match_score = 75.0  # fallback when generic JD has few explicit skills

    skill_match_score = round(min(100.0, max(0.0, skill_match_score)), 1)

    # Semantic similarity using TF-IDF
    semantic_score = calculate_semantic_similarity(resume_text, job_description)

    # Weighted Overall Match Score
    # 65% weighted on skill coverage, 35% on context/semantic overlap
    raw_match_score = (0.65 * skill_match_score) + (0.35 * semantic_score)
    match_score = round(min(100.0, max(0.0, raw_match_score)), 1)

    return {
        "candidate_skills": candidate_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_score": skill_match_score,
        "semantic_score": semantic_score,
        "match_score": match_score
    }


def calculate_ats_score(
    sections: Dict[str, bool],
    contact_info: Dict[str, Any],
    metrics_count: int,
    action_verbs_count: int,
    word_count: int
) -> float:
    """
    Calculate ATS compatibility score out of 100:
    - Standard Section Headers (40 pts)
    - Contact Info Completeness (20 pts)
    - Quantifiable Achievements (20 pts)
    - Action Verbs Strength (10 pts)
    - Optimal Length / Word Count (10 pts)
    """
    score = 0.0

    # Sections check: Summary, Experience, Education, Skills are crucial (8 pts each) + Projects/Certs (4 pts each)
    section_weights = {
        "experience": 12,
        "skills": 12,
        "education": 8,
        "summary": 4,
        "projects": 4
    }
    for sec, pts in section_weights.items():
        if sections.get(sec, False):
            score += pts

    # Contact info: Email (8 pts), Phone (6 pts), Name (4 pts), LinkedIn/GitHub (2 pts)
    if contact_info.get("email"):
        score += 8
    if contact_info.get("phone"):
        score += 6
    if contact_info.get("candidate_name") and contact_info["candidate_name"] != "Candidate":
        score += 4
    if contact_info.get("linkedin") or contact_info.get("github"):
        score += 2

    # Quantifiable metrics: 5+ metrics is great (20 pts), 2-4 (12 pts), 1 (6 pts)
    if metrics_count >= 5:
        score += 20
    elif metrics_count >= 3:
        score += 15
    elif metrics_count >= 1:
        score += 8

    # Action verbs: 8+ verbs (10 pts), 4-7 (6 pts), 1-3 (3 pts)
    if action_verbs_count >= 8:
        score += 10
    elif action_verbs_count >= 4:
        score += 6
    elif action_verbs_count >= 1:
        score += 3

    # Word count: Ideal resume is 300 to 900 words
    if 300 <= word_count <= 900:
        score += 10
    elif 200 <= word_count < 300 or 900 < word_count <= 1200:
        score += 6
    else:
        score += 2

    return round(min(100.0, max(10.0, score)), 1)


def generate_improvement_suggestions(
    missing_skills: List[str],
    matched_skills: List[str],
    sections: Dict[str, bool],
    contact_info: Dict[str, Any],
    metrics_count: int,
    action_verbs_count: int,
    match_score: float,
    job_title: str
) -> List[Dict[str, Any]]:
    """
    Generate prioritized, actionable feedback and suggestions to optimize the resume.
    """
    suggestions = []

    # 1. Missing Technical Skills
    if missing_skills:
        top_missing = missing_skills[:5]
        suggestions.append({
            "category": "Missing Skills",
            "priority": "high",
            "title": f"Target Missing Core Skills: {', '.join(top_missing[:3])}",
            "description": f"The job description explicitly mentions {len(missing_skills)} skills not found on your resume.",
            "actionable_tip": f"If you have hands-on experience with {', '.join(top_missing)}, add them to your 'Technical Skills' section and cite specific examples under your Work Experience or Projects."
        })
        if len(missing_skills) > 5:
            suggestions.append({
                "category": "Missing Skills",
                "priority": "medium",
                "title": f"Secondary Missing Skills: {', '.join(missing_skills[5:10])}",
                "description": "Additional tools or frameworks identified in the target role requirements.",
                "actionable_tip": "Review these secondary skills and weave relevant coursework, personal projects, or equivalent tools you've used into your resume."
            })

    # 2. Section Completeness
    missing_sections = [sec.capitalize() for sec, detected in sections.items() if not detected and sec != "certifications"]
    if missing_sections:
        suggestions.append({
            "category": "Formatting & ATS",
            "priority": "high",
            "title": f"Missing Resume Sections: {', '.join(missing_sections)}",
            "description": "Applicant Tracking Systems look for standard section headings to parse and categorize your qualifications accurately.",
            "actionable_tip": f"Add standard headings for {', '.join(missing_sections)}. For instance, use 'Professional Experience' or 'Work Experience' rather than unconventional titles."
        })

    # 3. Quantifiable Impact & Metrics
    if metrics_count < 3:
        suggestions.append({
            "category": "Impact & Metrics",
            "priority": "high",
            "title": "Quantify Achievements with Data & Percentages",
            "description": f"Only {metrics_count} metric(s) or numbers were detected in your bullet points.",
            "actionable_tip": "Transform passive duty descriptions into high-impact metrics using the Google XYZ formula: 'Accomplished [X] as measured by [Y] by doing [Z]'. Example: 'Reduced API response time by 45% by implementing Redis caching'."
        })
    else:
        suggestions.append({
            "category": "Impact & Metrics",
            "priority": "low",
            "title": "Strong Quantifiable Results",
            "description": f"Detected {metrics_count} quantifiable data points/metrics.",
            "actionable_tip": "Keep highlighting measurable ROI, latency reductions, user scale, and cost savings in future role entries."
        })

    # 4. Action Verbs
    if action_verbs_count < 5:
        suggestions.append({
            "category": "Action Verbs",
            "priority": "medium",
            "title": "Strengthen Bullet Points with Power Action Verbs",
            "description": "Weak or passive openers (e.g., 'Responsible for', 'Assisted with', 'Worked on') reduce ATS and recruiter engagement.",
            "actionable_tip": "Start every bullet with commanding verbs: 'Architected', 'Spearheaded', 'Optimized', 'Engineered', 'Automated', or 'Orchestrated'."
        })

    # 5. Contact Information Check
    if not contact_info.get("email") or not contact_info.get("phone"):
        suggestions.append({
            "category": "Formatting & ATS",
            "priority": "high",
            "title": "Incomplete Contact Header",
            "description": "Missing either phone number or email address in the extracted header.",
            "actionable_tip": "Ensure your phone number, professional email, LinkedIn URL, and GitHub profile are prominently located at the top of page 1."
        })

    # 6. Role Specific Alignment
    if match_score < 70:
        suggestions.append({
            "category": "Job Alignment",
            "priority": "medium",
            "title": f"Tailor Resume Summary for '{job_title}'",
            "description": "Your current overall match score is under 70%, suggesting the resume may be too generic for this position.",
            "actionable_tip": f"Write a 2-3 sentence tailored Professional Summary at the top: 'Results-driven engineer with expertise in {', '.join(matched_skills[:3]) if matched_skills else 'software engineering'} seeking to deliver value as {job_title}'."
        })

    return suggestions

