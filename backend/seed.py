"""
Seed MongoDB with rich organization data.
Each org has org-specific roadmap steps with estimated fees and funding.
Run: python seed.py
"""
from datetime import datetime
from database import (
    organizations_col, work_listings_col, disability_jobs_col, create_indexes
)

# ── Org roadmaps ───────────────────────────────────────────────────────────────
ORGS = [
    # ── SCIENTIST ──────────────────────────────────────────────────────────────
    {
        "name": "ISRO",
        "field": "Scientist",
        "description": "Indian Space Research Organisation – pushing the boundaries of space exploration and satellite technology.",
        "logo_emoji": "🚀",
        "total_funding": 220000,
        "roadmap": [
            {"step": 1, "title": "B.Sc Physics / Mathematics", "duration": "3 years", "description": "Foundation in classical mechanics, electromagnetism, quantum physics, and advanced mathematics.", "estimated_fee": 80000, "funding_available": True, "funding_source": "ISRO Scholarship", "funding_amount": 40000, "skills": ["Physics", "Mathematics", "Lab work"]},
            {"step": 2, "title": "M.Sc Astrophysics / Space Science", "duration": "2 years", "description": "Specialised study in orbital mechanics, satellite dynamics, remote sensing, and space instrumentation.", "estimated_fee": 120000, "funding_available": True, "funding_source": "ISRO RESPOND Grant", "funding_amount": 60000, "skills": ["Astrophysics", "MATLAB", "Python"]},
            {"step": 3, "title": "Technical Certifications", "duration": "6 months", "description": "ISRO Young Scientist Programme (YUVIKA), NPTEL courses in Aerospace Engineering.", "estimated_fee": 5000, "funding_available": True, "funding_source": "Govt. AICTE Grant", "funding_amount": 5000, "skills": ["Satellite Tech", "Remote Sensing"]},
            {"step": 4, "title": "Research Internship at ISRO", "duration": "6 months", "description": "Hands-on internship at ISRO centres (VSSC, SAC, URSC). Work on live satellite projects.", "estimated_fee": 0, "funding_available": True, "funding_source": "ISRO Stipend", "funding_amount": 60000, "skills": ["Research", "CAD", "Simulation"]},
            {"step": 5, "title": "Publish Research Paper", "duration": "3 months", "description": "Publish in peer-reviewed journals like Acta Astronautica or IJRS.", "estimated_fee": 10000, "funding_available": True, "funding_source": "ISRO Publication Grant", "funding_amount": 10000, "skills": ["Research Writing", "Data Analysis"]},
            {"step": 6, "title": "ISRO Scientist/Engineer Exam", "duration": "3 months", "description": "Appear for ISRO Centralised Recruitment Board exam. Syllabus: Physics, Maths, Electronics.", "estimated_fee": 500, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Problem Solving", "Technical Aptitude"]},
            {"step": 7, "title": "Join as Scientist-SC", "duration": "Permanent", "description": "Entry-level scientist role. Work on satellite design, launch vehicles, or space applications.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    {
        "name": "NASA",
        "field": "Scientist",
        "description": "National Aeronautics and Space Administration – humanity's gateway to the cosmos.",
        "logo_emoji": "🌌",
        "total_funding": 350000,
        "roadmap": [
            {"step": 1, "title": "B.S. in Physics / Aerospace Engineering", "duration": "4 years", "description": "Strong foundation in classical mechanics, thermodynamics, fluid dynamics, and aerospace principles.", "estimated_fee": 400000, "funding_available": True, "funding_source": "NASA Space Grant", "funding_amount": 150000, "skills": ["Physics", "Aerospace", "CAD"]},
            {"step": 2, "title": "M.S. / Ph.D. in Aerospace or Astrophysics", "duration": "2–5 years", "description": "Graduate research in propulsion, orbital mechanics, or planetary science.", "estimated_fee": 600000, "funding_available": True, "funding_source": "NASA Fellowship", "funding_amount": 200000, "skills": ["Research", "Python", "MATLAB"]},
            {"step": 3, "title": "NASA Internship (OSSI)", "duration": "3–6 months", "description": "NASA One Stop Shopping Initiative internship at JPL, Goddard, or Johnson Space Center.", "estimated_fee": 0, "funding_available": True, "funding_source": "NASA Stipend", "funding_amount": 120000, "skills": ["Mission Design", "Data Analysis"]},
            {"step": 4, "title": "GRE + TOEFL (for international)", "duration": "3 months", "description": "Standardised tests required for US graduate admissions.", "estimated_fee": 25000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Test Prep"]},
            {"step": 5, "title": "Research Publications", "duration": "Ongoing", "description": "Publish in Nature, Science, or Astrophysical Journal.", "estimated_fee": 15000, "funding_available": True, "funding_source": "University Grant", "funding_amount": 15000, "skills": ["Research Writing"]},
            {"step": 6, "title": "Apply as NASA Civil Servant / Contractor", "duration": "Ongoing", "description": "Apply via USAJOBS for NASA positions. Contractors via Lockheed, Boeing, SpaceX.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    {
        "name": "DRDO",
        "field": "Scientist",
        "description": "Defence Research and Development Organisation – advanced defence technology for India.",
        "logo_emoji": "🛡️",
        "total_funding": 180000,
        "roadmap": [
            {"step": 1, "title": "B.Tech / B.E. in Engineering", "duration": "4 years", "description": "Electronics, Mechanical, or Computer Science engineering from AICTE-approved college.", "estimated_fee": 200000, "funding_available": True, "funding_source": "DRDO Scholarship", "funding_amount": 80000, "skills": ["Engineering", "Physics", "Electronics"]},
            {"step": 2, "title": "GATE Exam", "duration": "6 months", "description": "Graduate Aptitude Test in Engineering – mandatory for DRDO Scientist B entry.", "estimated_fee": 2000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Problem Solving"]},
            {"step": 3, "title": "M.Tech (optional but preferred)", "duration": "2 years", "description": "Specialisation in Defence Electronics, Missiles, or Radar Systems.", "estimated_fee": 100000, "funding_available": True, "funding_source": "DRDO Research Fellowship", "funding_amount": 60000, "skills": ["Radar", "Missiles", "Signal Processing"]},
            {"step": 4, "title": "DRDO SET Exam", "duration": "3 months", "description": "DRDO Scientist Entry Test – written exam + interview for Scientist B position.", "estimated_fee": 500, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Technical Aptitude"]},
            {"step": 5, "title": "Join as Scientist B", "duration": "Permanent", "description": "Entry-level scientist at DRDO labs. Work on missiles, radar, electronic warfare.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    # ── SOFTWARE DEVELOPER ─────────────────────────────────────────────────────
    {
        "name": "Google",
        "field": "Software Developer",
        "description": "World's leading tech company – building products used by billions every day.",
        "logo_emoji": "🔍",
        "total_funding": 150000,
        "roadmap": [
            {"step": 1, "title": "B.Tech / B.E. in Computer Science", "duration": "4 years", "description": "Core CS fundamentals: Data Structures, Algorithms, OS, DBMS, Computer Networks, OOP.", "estimated_fee": 400000, "funding_available": True, "funding_source": "Google Generation Scholarship", "funding_amount": 100000, "skills": ["DSA", "OOP", "Databases"]},
            {"step": 2, "title": "Master DSA & System Design", "duration": "6 months", "description": "LeetCode 300+ problems, System Design (HLD/LLD), Distributed Systems concepts.", "estimated_fee": 15000, "funding_available": True, "funding_source": "Google Developer Scholarship", "funding_amount": 10000, "skills": ["LeetCode", "System Design", "Distributed Systems"]},
            {"step": 3, "title": "Build Projects & Open Source", "duration": "6 months", "description": "Build 3–5 production-quality projects. Contribute to open source on GitHub.", "estimated_fee": 5000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["React", "Node.js", "Docker", "Git"]},
            {"step": 4, "title": "Google STEP / SWE Internship", "duration": "3 months", "description": "Google's internship program for students. Competitive selection via online assessment + interviews.", "estimated_fee": 0, "funding_available": True, "funding_source": "Google Intern Stipend", "funding_amount": 150000, "skills": ["Coding", "Problem Solving"]},
            {"step": 5, "title": "Google Certifications", "duration": "3 months", "description": "Google Cloud Professional, TensorFlow Developer Certificate, Android Developer.", "estimated_fee": 20000, "funding_available": True, "funding_source": "Google Career Certificates Grant", "funding_amount": 10000, "skills": ["Cloud", "ML", "Android"]},
            {"step": 6, "title": "SWE Interview Preparation", "duration": "3 months", "description": "Mock interviews, behavioural prep (STAR method), Google's interview process (5–6 rounds).", "estimated_fee": 10000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Interview Skills"]},
            {"step": 7, "title": "Join as Software Engineer L3/L4", "duration": "Permanent", "description": "Entry-level SWE at Google. Work on Search, Maps, YouTube, Cloud, or AI products.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    {
        "name": "Microsoft",
        "field": "Software Developer",
        "description": "Enterprise software and cloud computing giant powering businesses worldwide.",
        "logo_emoji": "🪟",
        "total_funding": 130000,
        "roadmap": [
            {"step": 1, "title": "B.Tech in CS / IT", "duration": "4 years", "description": "Core CS: DSA, OS, DBMS, Networks. Focus on C++, Java, or C#.", "estimated_fee": 350000, "funding_available": True, "funding_source": "Microsoft Scholarship", "funding_amount": 80000, "skills": ["C++", "Java", "DSA"]},
            {"step": 2, "title": "Microsoft Learn Certifications", "duration": "4 months", "description": "Azure Fundamentals (AZ-900), Azure Developer (AZ-204), Power Platform.", "estimated_fee": 15000, "funding_available": True, "funding_source": "Microsoft Learn Grant", "funding_amount": 10000, "skills": ["Azure", "Cloud", ".NET"]},
            {"step": 3, "title": "Microsoft Engage / Internship", "duration": "3 months", "description": "Microsoft's mentorship + internship program. Apply via campus or online.", "estimated_fee": 0, "funding_available": True, "funding_source": "Microsoft Intern Stipend", "funding_amount": 120000, "skills": ["Product Dev", "Agile"]},
            {"step": 4, "title": "Build Portfolio Projects", "duration": "4 months", "description": "Full-stack apps using .NET, React, Azure. Contribute to Microsoft open source repos.", "estimated_fee": 5000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["React", ".NET", "Azure"]},
            {"step": 5, "title": "SWE Interview Prep", "duration": "2 months", "description": "Microsoft interviews: 4–5 rounds of coding + behavioural. Focus on DSA and system design.", "estimated_fee": 8000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Interview Skills"]},
            {"step": 6, "title": "Join as SDE I", "duration": "Permanent", "description": "Software Development Engineer at Microsoft. Work on Azure, Office 365, Teams, or Xbox.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    {
        "name": "Infosys",
        "field": "Software Developer",
        "description": "India's premier IT services and consulting company with global presence.",
        "logo_emoji": "💻",
        "total_funding": 60000,
        "roadmap": [
            {"step": 1, "title": "B.Tech / BCA / B.Sc CS", "duration": "3–4 years", "description": "Any CS/IT degree with 60%+ aggregate. Infosys hires from all engineering streams.", "estimated_fee": 200000, "funding_available": True, "funding_source": "Infosys Foundation Scholarship", "funding_amount": 40000, "skills": ["Programming", "DBMS", "Networking"]},
            {"step": 2, "title": "InfyTQ Certification", "duration": "3 months", "description": "Infosys's own platform for students. Earn certification to get shortlisted directly.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Java", "Python", "SQL"]},
            {"step": 3, "title": "Infosys Campus Placement", "duration": "1 month", "description": "Online test (Aptitude + Coding) + HR interview. Very high hiring volume.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Aptitude", "Coding"]},
            {"step": 4, "title": "Infosys Springboard Training", "duration": "3 months", "description": "Mandatory training at Mysore campus. Learn Java, Agile, DevOps, and domain skills.", "estimated_fee": 0, "funding_available": True, "funding_source": "Infosys Training Stipend", "funding_amount": 20000, "skills": ["Java", "Agile", "DevOps"]},
            {"step": 5, "title": "Join as Systems Engineer", "duration": "Permanent", "description": "Entry-level role. Work on client projects across banking, retail, healthcare domains.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    # ── AI ENGINEER ────────────────────────────────────────────────────────────
    {
        "name": "OpenAI",
        "field": "AI Engineer",
        "description": "Frontier AI research lab building safe and beneficial artificial general intelligence.",
        "logo_emoji": "🤖",
        "total_funding": 280000,
        "roadmap": [
            {"step": 1, "title": "B.Tech / M.Tech in CS with AI/ML", "duration": "4–6 years", "description": "Strong foundation in linear algebra, statistics, probability, and machine learning theory.", "estimated_fee": 500000, "funding_available": True, "funding_source": "OpenAI Scholars Program", "funding_amount": 150000, "skills": ["Linear Algebra", "Statistics", "Python"]},
            {"step": 2, "title": "Deep Learning Specialisation", "duration": "4 months", "description": "Coursera Deep Learning Specialisation (Andrew Ng), fast.ai, Hugging Face courses.", "estimated_fee": 20000, "funding_available": True, "funding_source": "OpenAI Education Grant", "funding_amount": 10000, "skills": ["PyTorch", "TensorFlow", "Transformers"]},
            {"step": 3, "title": "Build AI Projects & Kaggle", "duration": "6 months", "description": "Win Kaggle competitions, build LLM apps, fine-tune models, publish on GitHub.", "estimated_fee": 10000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["LLMs", "Fine-tuning", "RAG", "LangChain"]},
            {"step": 4, "title": "Research Papers on ArXiv", "duration": "6 months", "description": "Publish original AI research. Focus on NLP, computer vision, or reinforcement learning.", "estimated_fee": 5000, "funding_available": True, "funding_source": "University Research Grant", "funding_amount": 20000, "skills": ["Research", "LaTeX", "Experimentation"]},
            {"step": 5, "title": "OpenAI Residency / Internship", "duration": "6 months", "description": "Highly competitive residency program. Work alongside OpenAI researchers on frontier models.", "estimated_fee": 0, "funding_available": True, "funding_source": "OpenAI Residency Stipend", "funding_amount": 200000, "skills": ["Research", "PyTorch", "Distributed Training"]},
            {"step": 6, "title": "Join as AI Engineer / Research Scientist", "duration": "Permanent", "description": "Work on GPT, DALL-E, Codex, or safety research. Remote-friendly.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    {
        "name": "DeepMind",
        "field": "AI Engineer",
        "description": "Google's world-leading AI research lab – solving intelligence to advance science.",
        "logo_emoji": "🧠",
        "total_funding": 300000,
        "roadmap": [
            {"step": 1, "title": "PhD in CS / ML / Neuroscience", "duration": "4–5 years", "description": "DeepMind strongly prefers PhD candidates. Research in RL, game theory, or neuroscience.", "estimated_fee": 0, "funding_available": True, "funding_source": "DeepMind PhD Scholarship", "funding_amount": 200000, "skills": ["Research", "RL", "Mathematics"]},
            {"step": 2, "title": "Master Advanced ML Frameworks", "duration": "6 months", "description": "JAX, PyTorch, TensorFlow. Distributed training, TPU programming.", "estimated_fee": 10000, "funding_available": True, "funding_source": "Google Developer Grant", "funding_amount": 10000, "skills": ["JAX", "PyTorch", "TPU"]},
            {"step": 3, "title": "Publish Top-Tier Research", "duration": "Ongoing", "description": "Papers at NeurIPS, ICML, ICLR, Nature. Strong publication record is essential.", "estimated_fee": 20000, "funding_available": True, "funding_source": "Conference Travel Grant", "funding_amount": 30000, "skills": ["Research", "Writing"]},
            {"step": 4, "title": "DeepMind Internship", "duration": "3–6 months", "description": "Research internship at London or Paris office. Work on AlphaFold, Gemini, or safety.", "estimated_fee": 0, "funding_available": True, "funding_source": "DeepMind Intern Stipend", "funding_amount": 180000, "skills": ["Research", "Coding"]},
            {"step": 5, "title": "Join as Research Scientist", "duration": "Permanent", "description": "Work on cutting-edge AI research. Collaborate with Nobel laureates and top researchers.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    # ── DOCTOR ─────────────────────────────────────────────────────────────────
    {
        "name": "Apollo Hospitals",
        "field": "Doctor",
        "description": "India's largest integrated healthcare group with 70+ hospitals across Asia.",
        "logo_emoji": "🏥",
        "total_funding": 400000,
        "roadmap": [
            {"step": 1, "title": "MBBS (Bachelor of Medicine)", "duration": "5.5 years", "description": "MCI-recognised MBBS from government or private medical college. Includes 1-year internship.", "estimated_fee": 2000000, "funding_available": True, "funding_source": "Apollo Foundation Scholarship", "funding_amount": 300000, "skills": ["Anatomy", "Physiology", "Clinical Skills"]},
            {"step": 2, "title": "NEET-PG Preparation", "duration": "1 year", "description": "National Eligibility cum Entrance Test for postgraduate medical admissions.", "estimated_fee": 50000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Medicine", "Surgery", "Pharmacology"]},
            {"step": 3, "title": "MD / MS Specialisation", "duration": "3 years", "description": "Postgraduate specialisation in General Medicine, Surgery, Cardiology, Orthopaedics, etc.", "estimated_fee": 1500000, "funding_available": True, "funding_source": "Apollo Medical Education Grant", "funding_amount": 200000, "skills": ["Specialisation", "Clinical Research"]},
            {"step": 4, "title": "Apollo Fellowship / Residency", "duration": "1–2 years", "description": "Clinical fellowship at Apollo hospitals. Hands-on training in super-speciality departments.", "estimated_fee": 0, "funding_available": True, "funding_source": "Apollo Fellowship Stipend", "funding_amount": 120000, "skills": ["Clinical Practice", "Patient Management"]},
            {"step": 5, "title": "Medical Council Registration", "duration": "1 month", "description": "Register with State Medical Council and National Medical Commission.", "estimated_fee": 5000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Compliance"]},
            {"step": 6, "title": "Join Apollo as Consultant", "duration": "Permanent", "description": "Consultant physician or surgeon at Apollo. Excellent salary + research opportunities.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    {
        "name": "AIIMS",
        "field": "Doctor",
        "description": "All India Institute of Medical Sciences – India's most prestigious medical institution.",
        "logo_emoji": "⚕️",
        "total_funding": 500000,
        "roadmap": [
            {"step": 1, "title": "NEET-UG (Top 50 rank)", "duration": "2 years prep", "description": "Extremely competitive. Top 50 rank needed for AIIMS MBBS. Physics, Chemistry, Biology.", "estimated_fee": 100000, "funding_available": True, "funding_source": "Govt. Merit Scholarship", "funding_amount": 50000, "skills": ["Biology", "Chemistry", "Physics"]},
            {"step": 2, "title": "MBBS at AIIMS", "duration": "5.5 years", "description": "World-class MBBS program. Nominal fees (₹1,628/year for govt students).", "estimated_fee": 10000, "funding_available": True, "funding_source": "AIIMS Govt. Subsidy", "funding_amount": 300000, "skills": ["Medicine", "Surgery", "Research"]},
            {"step": 3, "title": "AIIMS MD/MS (NEET-PG)", "duration": "3 years", "description": "Postgraduate at AIIMS – most competitive PG seats in India.", "estimated_fee": 50000, "funding_available": True, "funding_source": "AIIMS Senior Residency Stipend", "funding_amount": 180000, "skills": ["Specialisation", "Research"]},
            {"step": 4, "title": "DM / MCh Super-Speciality", "duration": "3 years", "description": "Super-specialisation in Cardiology, Neurology, Oncology, etc.", "estimated_fee": 100000, "funding_available": True, "funding_source": "AIIMS Research Fellowship", "funding_amount": 150000, "skills": ["Super-Speciality", "Research"]},
            {"step": 5, "title": "Join AIIMS as Faculty / Consultant", "duration": "Permanent", "description": "Assistant Professor or Senior Resident at AIIMS. Prestigious career with research focus.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    # ── PHYSIOTHERAPIST ────────────────────────────────────────────────────────
    {
        "name": "Manipal Hospitals",
        "field": "Physiotherapist",
        "description": "Leading physiotherapy and rehabilitation services across India.",
        "logo_emoji": "🏥",
        "total_funding": 120000,
        "roadmap": [
            {"step": 1, "title": "BPT – Bachelor of Physiotherapy", "duration": "4.5 years", "description": "4-year program + 6-month internship. Covers anatomy, biomechanics, exercise therapy, electrotherapy.", "estimated_fee": 400000, "funding_available": True, "funding_source": "Manipal Foundation Scholarship", "funding_amount": 80000, "skills": ["Anatomy", "Biomechanics", "Manual Therapy"]},
            {"step": 2, "title": "MPT Specialisation", "duration": "2 years", "description": "Master of Physiotherapy in Sports, Neuro, Ortho, or Cardiopulmonary.", "estimated_fee": 200000, "funding_available": True, "funding_source": "Manipal PG Grant", "funding_amount": 60000, "skills": ["Specialisation", "Clinical Research"]},
            {"step": 3, "title": "Manipal Clinical Internship", "duration": "6 months", "description": "Rotational internship across Manipal's departments: ortho, neuro, ICU, sports.", "estimated_fee": 0, "funding_available": True, "funding_source": "Manipal Internship Stipend", "funding_amount": 30000, "skills": ["Patient Care", "Rehabilitation"]},
            {"step": 4, "title": "IAP / WCPT Certification", "duration": "3 months", "description": "Indian Association of Physiotherapists membership + WCPT international certification.", "estimated_fee": 10000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Professional Certification"]},
            {"step": 5, "title": "Join Manipal as Physiotherapist", "duration": "Permanent", "description": "Clinical physiotherapist at Manipal. Specialise in sports rehab, neuro, or geriatric care.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    {
        "name": "HealthFirst Clinic",
        "field": "Physiotherapist",
        "description": "Specialized physiotherapy and sports medicine center with modern equipment.",
        "logo_emoji": "🏃",
        "total_funding": 80000,
        "roadmap": [
            {"step": 1, "title": "BPT Degree", "duration": "4.5 years", "description": "Bachelor of Physiotherapy from any MCI-recognised college.", "estimated_fee": 300000, "funding_available": True, "funding_source": "HealthFirst Scholarship", "funding_amount": 50000, "skills": ["Anatomy", "Exercise Therapy"]},
            {"step": 2, "title": "Sports Physiotherapy Certification", "duration": "6 months", "description": "Certified Sports Physiotherapist (CSP) from Sports Authority of India.", "estimated_fee": 30000, "funding_available": True, "funding_source": "SAI Grant", "funding_amount": 20000, "skills": ["Sports Rehab", "Taping", "Dry Needling"]},
            {"step": 3, "title": "Clinical Practice (2 years)", "duration": "2 years", "description": "Work at any physiotherapy clinic or hospital to build experience.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["Patient Management", "Rehab Planning"]},
            {"step": 4, "title": "Join HealthFirst as Sports Physio", "duration": "Permanent", "description": "Sports physiotherapist treating athletes, corporate clients, and post-surgical patients.", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
    # ── NVIDIA (AI Engineer) ───────────────────────────────────────────────────
    {
        "name": "NVIDIA",
        "field": "AI Engineer",
        "description": "GPU and AI computing leader powering the AI revolution worldwide.",
        "logo_emoji": "⚡",
        "total_funding": 200000,
        "roadmap": [
            {"step": 1, "title": "B.Tech in CS / ECE", "duration": "4 years", "description": "Strong foundation in computer architecture, parallel computing, and C/C++.", "estimated_fee": 400000, "funding_available": True, "funding_source": "NVIDIA Graduate Fellowship", "funding_amount": 100000, "skills": ["C++", "Computer Architecture", "Parallel Computing"]},
            {"step": 2, "title": "CUDA & GPU Programming", "duration": "4 months", "description": "Master CUDA programming, GPU architecture, parallel algorithms.", "estimated_fee": 10000, "funding_available": True, "funding_source": "NVIDIA DLI Grant", "funding_amount": 10000, "skills": ["CUDA", "GPU", "Parallel Algorithms"]},
            {"step": 3, "title": "NVIDIA DLI Certifications", "duration": "3 months", "description": "NVIDIA Deep Learning Institute: Fundamentals of Deep Learning, Computer Vision, NLP.", "estimated_fee": 15000, "funding_available": True, "funding_source": "NVIDIA DLI Scholarship", "funding_amount": 15000, "skills": ["Deep Learning", "Computer Vision", "NLP"]},
            {"step": 4, "title": "Build GPU-Accelerated Projects", "duration": "4 months", "description": "Real-time object detection, LLM inference optimisation, autonomous driving simulations.", "estimated_fee": 5000, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["TensorRT", "Triton", "cuDNN"]},
            {"step": 5, "title": "NVIDIA Internship", "duration": "3 months", "description": "Internship in GPU architecture, AI frameworks, or autonomous vehicles (DRIVE platform).", "estimated_fee": 0, "funding_available": True, "funding_source": "NVIDIA Intern Stipend", "funding_amount": 150000, "skills": ["Research", "GPU Optimization"]},
            {"step": 6, "title": "Join as AI Engineer / GPU Architect", "duration": "Permanent", "description": "Work on next-gen GPUs, AI frameworks, or NVIDIA's AI products (Jetson, DRIVE, Clara).", "estimated_fee": 0, "funding_available": False, "funding_source": "", "funding_amount": 0, "skills": ["All above"]},
        ]
    },
]

# ── Work Listings ──────────────────────────────────────────────────────────────
WORK_LISTINGS = [
    {"title": "AC Repair", "description": "Fix split AC unit at residential apartment. Tools provided.", "location": "Koramangala, Bangalore", "pay": 800, "category": "Electrical", "emoji": "❄️", "status": "open"},
    {"title": "Plumbing Fix", "description": "Repair leaking pipe under kitchen sink.", "location": "Indiranagar, Bangalore", "pay": 600, "category": "Plumbing", "emoji": "🔧", "status": "open"},
    {"title": "Tailoring Work", "description": "Stitch 5 salwar suits. Material provided by client.", "location": "Jayanagar, Bangalore", "pay": 1200, "category": "Tailoring", "emoji": "🧵", "status": "open"},
    {"title": "House Painting", "description": "Paint 2BHK apartment interior walls. Paint provided.", "location": "HSR Layout, Bangalore", "pay": 3500, "category": "Painting", "emoji": "🎨", "status": "open"},
    {"title": "Carpentry", "description": "Build wooden bookshelf from design. Wood provided.", "location": "Whitefield, Bangalore", "pay": 2000, "category": "Carpentry", "emoji": "🪚", "status": "open"},
    {"title": "Electrical Wiring", "description": "Install new switchboard and wiring in office room.", "location": "MG Road, Bangalore", "pay": 1500, "category": "Electrical", "emoji": "⚡", "status": "open"},
    {"title": "Garden Maintenance", "description": "Trim hedges, water plants, and clean garden area.", "location": "Sadashivanagar, Bangalore", "pay": 500, "category": "Gardening", "emoji": "🌿", "status": "open"},
    {"title": "Delivery Run", "description": "Deliver 20 packages across 5km radius. Bike required.", "location": "BTM Layout, Bangalore", "pay": 700, "category": "Delivery", "emoji": "📦", "status": "open"},
    {"title": "Cooking Help", "description": "Prepare lunch for 10 people at office event.", "location": "Electronic City, Bangalore", "pay": 1000, "category": "Cooking", "emoji": "👨‍🍳", "status": "open"},
    {"title": "Car Wash", "description": "Full exterior and interior cleaning of 3 cars.", "location": "JP Nagar, Bangalore", "pay": 450, "category": "Cleaning", "emoji": "🚗", "status": "open"},
]

# ── Disability Jobs ────────────────────────────────────────────────────────────
DISABILITY_JOBS = [
    {"title": "Remote Stitching Orders", "description": "Stitch garments from home. Designs sent digitally. Flexible hours.", "profession": "Tailor", "pay": 3000, "company": "FabricHub India", "job_type": "remote", "emoji": "🧵", "status": "open"},
    {"title": "Embroidery Work", "description": "Hand embroidery on sarees and suits. Work from home.", "profession": "Tailor", "pay": 2500, "company": "Craftify", "job_type": "remote", "emoji": "🪡", "status": "open"},
    {"title": "Customer Support Executive", "description": "Handle inbound calls and emails for e-commerce queries.", "profession": "Customer Support", "pay": 18000, "company": "ShopEasy", "job_type": "remote", "emoji": "🎧", "status": "open"},
    {"title": "Chat Support Agent", "description": "Respond to customer queries via live chat. Flexible shifts.", "profession": "Customer Support", "pay": 15000, "company": "HelpDesk Pro", "job_type": "remote", "emoji": "💬", "status": "open"},
    {"title": "Data Entry Operator", "description": "Enter structured data into spreadsheets. Work from home.", "profession": "Data Entry", "pay": 12000, "company": "DataCorp", "job_type": "remote", "emoji": "📊", "status": "open"},
    {"title": "Content Transcription", "description": "Transcribe audio recordings to text. Flexible hours.", "profession": "Data Entry", "pay": 10000, "company": "TranscribeNow", "job_type": "remote", "emoji": "📝", "status": "open"},
    {"title": "Online Tutor – Mathematics", "description": "Teach students via video call. Set your own schedule.", "profession": "Teacher", "pay": 20000, "company": "EduBridge", "job_type": "remote", "emoji": "📐", "status": "open"},
    {"title": "Graphic Design (Freelance)", "description": "Create social media posts and banners. Work from home.", "profession": "Designer", "pay": 25000, "company": "CreativeHub", "job_type": "remote", "emoji": "🎨", "status": "open"},
    {"title": "Bookkeeping Assistant", "description": "Maintain accounts and invoices for small business. Remote.", "profession": "Accountant", "pay": 16000, "company": "FinTrack", "job_type": "remote", "emoji": "📒", "status": "open"},
    {"title": "Podcast Editor", "description": "Edit audio recordings and add effects. Work from home.", "profession": "Media", "pay": 14000, "company": "SoundWave Studios", "job_type": "remote", "emoji": "🎙️", "status": "open"},
]


def seed():
    create_indexes()

    if organizations_col.count_documents({}) == 0:
        for org in ORGS:
            org["created_at"] = datetime.utcnow()
        organizations_col.insert_many(ORGS)
        print(f"✅ Seeded {len(ORGS)} organizations with roadmaps")

    if work_listings_col.count_documents({}) == 0:
        for w in WORK_LISTINGS:
            w["created_at"] = datetime.utcnow()
            w["accepted_by"] = None
        work_listings_col.insert_many(WORK_LISTINGS)
        print(f"✅ Seeded {len(WORK_LISTINGS)} work listings")

    if disability_jobs_col.count_documents({}) == 0:
        for j in DISABILITY_JOBS:
            j["created_at"] = datetime.utcnow()
            j["accepted_by"] = None
        disability_jobs_col.insert_many(DISABILITY_JOBS)
        print(f"✅ Seeded {len(DISABILITY_JOBS)} disability jobs")

    print("🌱 MongoDB seeded successfully!")


if __name__ == "__main__":
    seed()
