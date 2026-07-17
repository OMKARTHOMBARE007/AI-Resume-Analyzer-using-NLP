"""
Constants - Skill taxonomy, action verbs, and reference data for NLP processing.
"""

# ============================================================================
# SKILLS TAXONOMY - 500+ skills organized by category
# ============================================================================

SKILLS_DATABASE = {
    "programming_languages": [
        "python", "java", "javascript", "typescript", "c", "c++", "c#", "ruby",
        "go", "golang", "rust", "swift", "kotlin", "scala", "perl", "php",
        "r", "matlab", "julia", "dart", "lua", "haskell", "elixir", "clojure",
        "objective-c", "assembly", "fortran", "cobol", "visual basic", "vba",
        "groovy", "shell", "bash", "powershell", "sql", "plsql", "tsql",
    ],
    "web_frameworks": [
        "react", "react.js", "reactjs", "angular", "angularjs", "vue", "vue.js",
        "vuejs", "next.js", "nextjs", "nuxt.js", "nuxtjs", "svelte", "gatsby",
        "django", "flask", "fastapi", "express", "express.js", "expressjs",
        "spring", "spring boot", "springboot", "rails", "ruby on rails",
        "asp.net", ".net", "dotnet", "laravel", "symfony", "gin", "fiber",
        "nest.js", "nestjs", "remix", "astro", "ember.js",
    ],
    "databases": [
        "mysql", "postgresql", "postgres", "mongodb", "redis", "sqlite",
        "oracle", "sql server", "mssql", "cassandra", "dynamodb", "couchdb",
        "neo4j", "elasticsearch", "mariadb", "firebase", "firestore",
        "supabase", "cockroachdb", "influxdb", "timescaledb", "memcached",
    ],
    "cloud_platforms": [
        "aws", "amazon web services", "azure", "microsoft azure",
        "gcp", "google cloud", "google cloud platform",
        "heroku", "digitalocean", "linode", "cloudflare", "vercel",
        "netlify", "render", "railway", "fly.io",
    ],
    "cloud_services": [
        "ec2", "s3", "lambda", "ecs", "eks", "rds", "dynamodb", "sqs", "sns",
        "cloudformation", "cloudwatch", "api gateway", "cognito", "iam",
        "azure functions", "azure devops", "cloud functions", "bigquery",
        "cloud run", "cloud storage", "pub/sub",
    ],
    "devops_tools": [
        "docker", "kubernetes", "k8s", "jenkins", "gitlab ci", "github actions",
        "circleci", "travis ci", "terraform", "ansible", "puppet", "chef",
        "vagrant", "helm", "argocd", "prometheus", "grafana", "datadog",
        "new relic", "splunk", "elk stack", "nginx", "apache", "caddy",
    ],
    "data_science_ml": [
        "machine learning", "deep learning", "neural networks", "nlp",
        "natural language processing", "computer vision", "data science",
        "data analysis", "data mining", "data visualization",
        "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
        "jupyter", "tableau", "power bi", "apache spark", "hadoop",
        "airflow", "mlflow", "hugging face", "transformers", "bert",
        "gpt", "openai", "langchain", "llm", "generative ai", "gen ai",
        "xgboost", "lightgbm", "catboost", "opencv", "spacy", "nltk",
        "regression", "classification", "clustering", "recommendation systems",
    ],
    "mobile_development": [
        "react native", "flutter", "swift", "swiftui", "kotlin",
        "android", "ios", "xamarin", "ionic", "capacitor",
        "expo", "jetpack compose",
    ],
    "testing": [
        "unit testing", "integration testing", "e2e testing",
        "jest", "mocha", "chai", "pytest", "unittest", "selenium",
        "cypress", "playwright", "puppeteer", "testng", "junit",
        "mockito", "enzyme", "testing library", "vitest",
        "tdd", "bdd", "test driven development",
    ],
    "version_control": [
        "git", "github", "gitlab", "bitbucket", "svn", "subversion",
        "mercurial",
    ],
    "design_tools": [
        "figma", "sketch", "adobe xd", "photoshop", "illustrator",
        "invision", "zeplin", "canva", "balsamiq",
    ],
    "project_management": [
        "jira", "confluence", "trello", "asana", "monday.com",
        "linear", "notion", "clickup", "basecamp",
    ],
    "methodologies": [
        "agile", "scrum", "kanban", "waterfall", "lean", "devops",
        "ci/cd", "continuous integration", "continuous deployment",
        "microservices", "monolithic", "serverless", "event-driven",
        "rest", "restful", "graphql", "grpc", "soap", "websockets",
        "mvc", "mvvm", "clean architecture", "domain-driven design", "ddd",
    ],
    "security": [
        "cybersecurity", "penetration testing", "ethical hacking",
        "owasp", "encryption", "ssl", "tls", "oauth", "oauth2",
        "jwt", "saml", "ldap", "sso", "mfa", "2fa",
        "vulnerability assessment", "siem", "soc", "firewall",
    ],
    "soft_skills": [
        "leadership", "communication", "teamwork", "problem solving",
        "critical thinking", "time management", "adaptability",
        "creativity", "collaboration", "mentoring", "presentation",
        "negotiation", "decision making", "conflict resolution",
        "project management", "stakeholder management", "cross-functional",
    ],
    "other_tools": [
        "linux", "unix", "windows server", "macos",
        "rest api", "api development", "microservices architecture",
        "message queue", "rabbitmq", "kafka", "apache kafka",
        "celery", "websocket", "oauth", "saml",
        "swagger", "openapi", "postman", "insomnia",
        "webpack", "vite", "rollup", "babel", "eslint", "prettier",
        "npm", "yarn", "pnpm", "pip", "conda",
        "redis", "celery", "cron", "systemd",
    ],
}

# Flatten skills for quick lookup
ALL_SKILLS = set()
SKILL_TO_CATEGORY = {}
for category, skills in SKILLS_DATABASE.items():
    for skill in skills:
        ALL_SKILLS.add(skill.lower())
        SKILL_TO_CATEGORY[skill.lower()] = category


# ============================================================================
# ACTION VERBS - Strong vs weak verbs for resume suggestions
# ============================================================================

STRONG_ACTION_VERBS = [
    "achieved", "accelerated", "accomplished", "administered", "advanced",
    "analyzed", "architected", "automated", "built", "championed",
    "collaborated", "conceptualized", "consolidated", "constructed",
    "converted", "coordinated", "created", "cultivated", "customized",
    "decreased", "delivered", "deployed", "designed", "developed",
    "devised", "directed", "drove", "earned", "eliminated",
    "enabled", "engineered", "enhanced", "established", "evaluated",
    "exceeded", "executed", "expanded", "expedited", "facilitated",
    "formulated", "founded", "generated", "grew", "guided",
    "headed", "identified", "implemented", "improved", "increased",
    "influenced", "initiated", "innovated", "integrated", "introduced",
    "invented", "launched", "led", "leveraged", "maintained",
    "managed", "maximized", "mentored", "migrated", "minimized",
    "modernized", "negotiated", "optimized", "orchestrated", "organized",
    "overhauled", "oversaw", "partnered", "pioneered", "planned",
    "presented", "prioritized", "produced", "programmed", "proposed",
    "published", "rebuilt", "redesigned", "reduced", "refactored",
    "reengineered", "renovated", "reorganized", "resolved", "restructured",
    "revamped", "revitalized", "revolutionized", "scaled", "secured",
    "simplified", "spearheaded", "standardized", "streamlined",
    "strengthened", "supervised", "surpassed", "synthesized",
    "transformed", "troubleshot", "unified", "upgraded", "utilized",
]

WEAK_ACTION_VERBS = [
    "did", "made", "got", "went", "had", "was", "were",
    "helped", "tried", "used", "worked", "handled", "dealt",
    "responsible for", "involved in", "participated in",
    "assisted with", "tasked with", "in charge of",
]

# Mapping of weak verbs to strong alternatives
VERB_IMPROVEMENTS = {
    "did": ["executed", "accomplished", "completed", "delivered"],
    "made": ["created", "developed", "built", "produced"],
    "helped": ["facilitated", "enabled", "supported", "contributed to"],
    "worked": ["collaborated", "partnered", "engaged", "contributed"],
    "handled": ["managed", "coordinated", "directed", "oversaw"],
    "used": ["leveraged", "utilized", "employed", "applied"],
    "responsible for": ["led", "managed", "directed", "spearheaded"],
    "involved in": ["contributed to", "participated in", "engaged in"],
    "tried": ["attempted", "pursued", "endeavored", "strived"],
}


# ============================================================================
# EDUCATION KEYWORDS
# ============================================================================

DEGREE_KEYWORDS = [
    "bachelor", "b.s.", "b.sc", "b.a.", "b.tech", "b.e.", "btech", "bsc", "ba",
    "master", "m.s.", "m.sc", "m.a.", "m.tech", "m.e.", "mtech", "msc", "ma", "mba",
    "ph.d", "phd", "doctorate", "doctoral",
    "associate", "a.s.", "a.a.",
    "diploma", "certificate", "certification",
    "high school", "secondary", "hsc", "ssc", "10th", "12th",
]

EDUCATION_FIELDS = [
    "computer science", "information technology", "software engineering",
    "electrical engineering", "electronics", "mechanical engineering",
    "civil engineering", "chemical engineering", "data science",
    "artificial intelligence", "machine learning", "mathematics",
    "statistics", "physics", "chemistry", "biology",
    "business administration", "management", "finance", "economics",
    "marketing", "human resources", "accounting",
    "communication", "journalism", "psychology", "sociology",
    "political science", "law", "medicine", "pharmacy", "nursing",
]


# ============================================================================
# SECTION HEADERS for resume parsing
# ============================================================================

SECTION_HEADERS = {
    "experience": [
        "experience", "work experience", "professional experience",
        "employment history", "work history", "career history",
        "professional background", "employment",
    ],
    "education": [
        "education", "educational background", "academic background",
        "academic qualifications", "qualifications", "academic history",
    ],
    "skills": [
        "skills", "technical skills", "core competencies", "competencies",
        "proficiencies", "areas of expertise", "technologies",
        "technical proficiencies", "tools & technologies",
        "skills & competencies", "key skills",
    ],
    "projects": [
        "projects", "personal projects", "academic projects",
        "key projects", "notable projects", "project experience",
    ],
    "certifications": [
        "certifications", "certificates", "professional certifications",
        "licenses", "credentials", "accreditations",
    ],
    "achievements": [
        "achievements", "accomplishments", "awards", "honors",
        "recognition", "awards & honors",
    ],
    "languages": [
        "languages", "language proficiency", "language skills",
    ],
    "summary": [
        "summary", "professional summary", "objective", "career objective",
        "profile", "professional profile", "about me", "about",
    ],
    "contact": [
        "contact", "contact information", "personal information",
        "personal details",
    ],
    "interests": [
        "interests", "hobbies", "activities", "extracurricular",
    ],
    "publications": [
        "publications", "papers", "research", "research papers",
    ],
    "references": [
        "references",
    ],
}


# ============================================================================
# CERTIFICATION DATABASE for suggestions
# ============================================================================

CERTIFICATION_SUGGESTIONS = {
    "cloud_platforms": [
        "AWS Certified Solutions Architect",
        "AWS Certified Developer",
        "Azure Administrator Associate",
        "Google Cloud Professional Cloud Architect",
    ],
    "data_science_ml": [
        "TensorFlow Developer Certificate",
        "AWS Machine Learning Specialty",
        "Google Professional Machine Learning Engineer",
        "IBM Data Science Professional Certificate",
    ],
    "web_frameworks": [
        "Meta Front-End Developer Certificate",
        "Google UX Design Certificate",
        "AWS Certified Developer Associate",
    ],
    "devops_tools": [
        "Certified Kubernetes Administrator (CKA)",
        "Docker Certified Associate",
        "HashiCorp Terraform Associate",
        "AWS DevOps Engineer Professional",
    ],
    "security": [
        "CompTIA Security+",
        "Certified Ethical Hacker (CEH)",
        "CISSP",
        "OSCP",
    ],
    "project_management": [
        "PMP (Project Management Professional)",
        "Certified ScrumMaster (CSM)",
        "PRINCE2",
        "Agile Certified Practitioner (PMI-ACP)",
    ],
}
