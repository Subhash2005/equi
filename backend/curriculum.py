"""
Monthly quiz and task data per field of study.
Each month has: a quiz (5 MCQ questions) + a practical task to implement.
"""

MONTHLY_CURRICULUM = {
    "Scientist": [
        {
            "month": 1,
            "topic": "Physics Foundations",
            "quiz": [
                {"q": "What is the SI unit of force?", "options": ["Joule", "Newton", "Pascal", "Watt"], "answer": 1},
                {"q": "Which law states F = ma?", "options": ["Newton's 1st", "Newton's 2nd", "Newton's 3rd", "Hooke's Law"], "answer": 1},
                {"q": "What is the speed of light in vacuum?", "options": ["3×10⁶ m/s", "3×10⁸ m/s", "3×10¹⁰ m/s", "3×10⁴ m/s"], "answer": 1},
                {"q": "Which particle has no charge?", "options": ["Proton", "Electron", "Neutron", "Positron"], "answer": 2},
                {"q": "What does E=mc² represent?", "options": ["Kinetic energy", "Mass-energy equivalence", "Potential energy", "Thermal energy"], "answer": 1},
            ],
            "task": {
                "title": "Build a Simple Pendulum Simulator",
                "description": "Create a Python script that simulates a simple pendulum. Calculate the period T = 2π√(L/g) for different lengths (0.5m, 1m, 2m) and plot the results. Submit your code and a screenshot of the output.",
                "deliverable": "Python script + output screenshot",
                "skills": ["Python", "Physics", "Matplotlib"],
            }
        },
        {
            "month": 2,
            "topic": "Mathematics & Calculus",
            "quiz": [
                {"q": "What is the derivative of sin(x)?", "options": ["-cos(x)", "cos(x)", "tan(x)", "-sin(x)"], "answer": 1},
                {"q": "∫x² dx = ?", "options": ["x³", "x³/3 + C", "2x", "x²/2"], "answer": 1},
                {"q": "What is the value of e (Euler's number)?", "options": ["2.718", "3.141", "1.618", "2.303"], "answer": 0},
                {"q": "Which matrix operation is NOT always defined?", "options": ["Addition", "Scalar multiplication", "Matrix multiplication", "Transpose"], "answer": 2},
                {"q": "What is the gradient of a scalar field?", "options": ["A scalar", "A vector", "A matrix", "A tensor"], "answer": 1},
            ],
            "task": {
                "title": "Solve Orbital Mechanics Problem",
                "description": "Using Python, calculate the orbital period of a satellite at altitude 400km (ISS orbit) using Kepler's third law. Then calculate the orbital velocity. Submit your calculations with code.",
                "deliverable": "Python notebook or script with results",
                "skills": ["Python", "Mathematics", "Orbital Mechanics"],
            }
        },
        {
            "month": 3,
            "topic": "Astrophysics Basics",
            "quiz": [
                {"q": "What is a light-year?", "options": ["Time", "Distance", "Speed", "Mass"], "answer": 1},
                {"q": "Which is the closest star to Earth (after Sun)?", "options": ["Sirius", "Proxima Centauri", "Betelgeuse", "Vega"], "answer": 1},
                {"q": "What causes a solar eclipse?", "options": ["Earth's shadow on Moon", "Moon's shadow on Earth", "Sun's rotation", "Earth's rotation"], "answer": 1},
                {"q": "What is the Hubble constant used for?", "options": ["Measuring star mass", "Universe expansion rate", "Black hole radius", "Gravity constant"], "answer": 1},
                {"q": "What type of radiation does a pulsar emit?", "options": ["Visible light", "Radio waves", "X-rays only", "Gamma rays only"], "answer": 1},
            ],
            "task": {
                "title": "Star Classification Project",
                "description": "Download the HYG star database (free CSV) and write a Python script to classify stars by spectral type (O, B, A, F, G, K, M). Create a Hertzsprung-Russell diagram using matplotlib. Submit code + diagram.",
                "deliverable": "Python script + H-R diagram image",
                "skills": ["Python", "Data Analysis", "Astrophysics"],
            }
        },
    ],
    "Software Developer": [
        {
            "month": 1,
            "topic": "Data Structures & Algorithms",
            "quiz": [
                {"q": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"], "answer": 1},
                {"q": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Heap", "Tree"], "answer": 1},
                {"q": "What is a hash collision?", "options": ["Two keys map to same index", "Hash function error", "Memory overflow", "Null pointer"], "answer": 0},
                {"q": "Which sorting algorithm has O(n log n) average case?", "options": ["Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort"], "answer": 2},
                {"q": "What does DFS stand for?", "options": ["Data File System", "Depth First Search", "Dynamic Function Stack", "Direct File Storage"], "answer": 1},
            ],
            "task": {
                "title": "Implement a LRU Cache",
                "description": "Build a Least Recently Used (LRU) Cache in Python using OrderedDict or a doubly linked list + hashmap. It should support get(key) and put(key, value) in O(1) time. Write unit tests. Submit code on GitHub.",
                "deliverable": "GitHub repo link with code + tests",
                "skills": ["Python/Java", "DSA", "Problem Solving"],
            }
        },
        {
            "month": 2,
            "topic": "System Design Fundamentals",
            "quiz": [
                {"q": "What does API stand for?", "options": ["Application Programming Interface", "Automated Process Integration", "Advanced Protocol Interface", "Application Process Interaction"], "answer": 0},
                {"q": "What is horizontal scaling?", "options": ["Adding more RAM", "Adding more servers", "Faster CPU", "Bigger database"], "answer": 1},
                {"q": "What is a CDN used for?", "options": ["Database backup", "Content delivery", "Code deployment", "Network security"], "answer": 1},
                {"q": "What does REST stand for?", "options": ["Remote Execution State Transfer", "Representational State Transfer", "Resource Endpoint Service Transfer", "Reliable Event Stream Transfer"], "answer": 1},
                {"q": "Which database is better for unstructured data?", "options": ["MySQL", "PostgreSQL", "MongoDB", "SQLite"], "answer": 2},
            ],
            "task": {
                "title": "Design a URL Shortener",
                "description": "Design and implement a URL shortener (like bit.ly) using Python + FastAPI. It should: generate short codes, store mappings, redirect on access, and track click counts. Deploy locally and document the API.",
                "deliverable": "GitHub repo + API documentation (Swagger/Postman)",
                "skills": ["FastAPI", "System Design", "Databases"],
            }
        },
        {
            "month": 3,
            "topic": "Web Development",
            "quiz": [
                {"q": "What does DOM stand for?", "options": ["Document Object Model", "Data Object Management", "Dynamic Output Module", "Design Object Map"], "answer": 0},
                {"q": "Which HTTP method is used to update a resource?", "options": ["GET", "POST", "PUT", "DELETE"], "answer": 2},
                {"q": "What is React's virtual DOM?", "options": ["A browser feature", "A lightweight copy of real DOM", "A CSS framework", "A database"], "answer": 1},
                {"q": "What does CSS stand for?", "options": ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style System", "Coded Style Sheets"], "answer": 1},
                {"q": "What is async/await used for?", "options": ["Styling", "Asynchronous operations", "Database queries only", "Error handling"], "answer": 1},
            ],
            "task": {
                "title": "Build a Full-Stack Todo App",
                "description": "Create a full-stack Todo application with React frontend + FastAPI backend + SQLite database. Features: add/edit/delete todos, mark complete, filter by status. Deploy locally. Submit GitHub repo.",
                "deliverable": "GitHub repo with README and screenshots",
                "skills": ["React", "FastAPI", "SQLite", "REST API"],
            }
        },
    ],
    "AI Engineer": [
        {
            "month": 1,
            "topic": "Machine Learning Fundamentals",
            "quiz": [
                {"q": "What is overfitting?", "options": ["Model too simple", "Model memorizes training data", "Model has no bias", "Model trains too fast"], "answer": 1},
                {"q": "Which algorithm is used for classification?", "options": ["Linear Regression", "K-Means", "Logistic Regression", "PCA"], "answer": 2},
                {"q": "What is gradient descent?", "options": ["A data preprocessing step", "Optimization algorithm to minimize loss", "A neural network layer", "A regularization technique"], "answer": 1},
                {"q": "What does 'epoch' mean in ML training?", "options": ["One forward pass", "One full pass through training data", "One batch update", "One validation step"], "answer": 1},
                {"q": "What is the purpose of a validation set?", "options": ["Train the model", "Tune hyperparameters", "Final evaluation", "Data augmentation"], "answer": 1},
            ],
            "task": {
                "title": "Train an Image Classifier",
                "description": "Using scikit-learn or PyTorch, train a classifier on the MNIST dataset (handwritten digits). Achieve >95% accuracy. Plot the confusion matrix and show 5 misclassified examples. Submit Jupyter notebook.",
                "deliverable": "Jupyter notebook with results and confusion matrix",
                "skills": ["Python", "scikit-learn/PyTorch", "Data Analysis"],
            }
        },
        {
            "month": 2,
            "topic": "Deep Learning & Neural Networks",
            "quiz": [
                {"q": "What is a convolutional layer used for?", "options": ["Text processing", "Feature extraction from images", "Sequence modeling", "Dimensionality reduction"], "answer": 1},
                {"q": "What does ReLU stand for?", "options": ["Recurrent Linear Unit", "Rectified Linear Unit", "Recursive Learning Unit", "Regularized Linear Update"], "answer": 1},
                {"q": "What is dropout used for?", "options": ["Speed up training", "Prevent overfitting", "Increase model size", "Data augmentation"], "answer": 1},
                {"q": "What is backpropagation?", "options": ["Forward pass", "Algorithm to compute gradients", "Data loading", "Model evaluation"], "answer": 1},
                {"q": "Which architecture is best for NLP?", "options": ["CNN", "RNN/Transformer", "SVM", "Decision Tree"], "answer": 1},
            ],
            "task": {
                "title": "Build a Sentiment Analyzer",
                "description": "Using HuggingFace Transformers, fine-tune a BERT model on the IMDB movie review dataset for sentiment analysis (positive/negative). Test on 10 custom reviews. Submit code + model performance report.",
                "deliverable": "Python script + performance report (accuracy, F1 score)",
                "skills": ["PyTorch", "HuggingFace", "NLP", "Transformers"],
            }
        },
        {
            "month": 3,
            "topic": "LLMs & Generative AI",
            "quiz": [
                {"q": "What does LLM stand for?", "options": ["Large Language Model", "Linear Learning Module", "Layered Logic Machine", "Long Learning Method"], "answer": 0},
                {"q": "What is prompt engineering?", "options": ["Writing code prompts", "Crafting inputs to guide LLM outputs", "Training LLMs", "Evaluating LLMs"], "answer": 1},
                {"q": "What is RAG?", "options": ["Random Augmentation Generator", "Retrieval Augmented Generation", "Recurrent Attention Gate", "Regularized Auto-Generator"], "answer": 1},
                {"q": "What is a token in LLMs?", "options": ["A password", "A unit of text (word/subword)", "A layer", "A weight"], "answer": 1},
                {"q": "What is fine-tuning?", "options": ["Training from scratch", "Adjusting pre-trained model on specific data", "Pruning a model", "Quantizing a model"], "answer": 1},
            ],
            "task": {
                "title": "Build a RAG Chatbot",
                "description": "Using LangChain + OpenAI API (or free Ollama locally), build a RAG (Retrieval Augmented Generation) chatbot that answers questions about a PDF document. The bot should cite sources. Submit code + demo video.",
                "deliverable": "GitHub repo + 2-minute demo video",
                "skills": ["LangChain", "LLMs", "Vector Databases", "Python"],
            }
        },
    ],
    "Doctor": [
        {
            "month": 1,
            "topic": "Human Anatomy",
            "quiz": [
                {"q": "How many bones are in the adult human body?", "options": ["186", "206", "226", "246"], "answer": 1},
                {"q": "Which organ produces insulin?", "options": ["Liver", "Kidney", "Pancreas", "Spleen"], "answer": 2},
                {"q": "What is the largest organ of the body?", "options": ["Liver", "Brain", "Skin", "Lungs"], "answer": 2},
                {"q": "Which blood type is the universal donor?", "options": ["A+", "B+", "AB+", "O-"], "answer": 3},
                {"q": "What is the normal resting heart rate?", "options": ["40-50 bpm", "60-100 bpm", "100-120 bpm", "120-140 bpm"], "answer": 1},
            ],
            "task": {
                "title": "Create an Anatomy Flashcard App",
                "description": "Build a simple web-based flashcard app (HTML/JS) with 20 anatomy questions covering major organ systems. Include images (use free medical illustrations). Test with 5 classmates and report their scores.",
                "deliverable": "HTML file + test results report",
                "skills": ["HTML/JS", "Medical Knowledge", "Teaching"],
            }
        },
        {
            "month": 2,
            "topic": "Physiology & Pharmacology",
            "quiz": [
                {"q": "What is the normal blood pressure?", "options": ["100/60 mmHg", "120/80 mmHg", "140/90 mmHg", "160/100 mmHg"], "answer": 1},
                {"q": "Which neurotransmitter is deficient in Parkinson's?", "options": ["Serotonin", "Dopamine", "Acetylcholine", "GABA"], "answer": 1},
                {"q": "What is the mechanism of aspirin?", "options": ["COX inhibitor", "ACE inhibitor", "Beta blocker", "Calcium channel blocker"], "answer": 0},
                {"q": "What does ECG measure?", "options": ["Brain activity", "Heart electrical activity", "Lung capacity", "Blood pressure"], "answer": 1},
                {"q": "Which vitamin deficiency causes scurvy?", "options": ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D"], "answer": 2},
            ],
            "task": {
                "title": "Drug Interaction Checker",
                "description": "Research and document 10 common drug interactions (e.g., warfarin + aspirin). Create a simple lookup table in Excel/Google Sheets with: Drug A, Drug B, Interaction type, Clinical significance, Management. Present to your study group.",
                "deliverable": "Excel/Sheets file + 5-minute presentation notes",
                "skills": ["Pharmacology", "Research", "Clinical Reasoning"],
            }
        },
        {
            "month": 3,
            "topic": "Clinical Skills",
            "quiz": [
                {"q": "What is the first step in patient examination?", "options": ["Auscultation", "Inspection", "Palpation", "Percussion"], "answer": 1},
                {"q": "What does SOAP stand for in medical notes?", "options": ["Symptoms, Observations, Assessment, Plan", "Subjective, Objective, Assessment, Plan", "Signs, Observations, Analysis, Prescription", "Symptoms, Objective, Analysis, Plan"], "answer": 1},
                {"q": "Normal SpO2 level is?", "options": ["85-90%", "90-94%", "95-100%", "100%"], "answer": 2},
                {"q": "What is tachycardia?", "options": ["Heart rate <60 bpm", "Heart rate >100 bpm", "Irregular heartbeat", "Heart rate 60-100 bpm"], "answer": 1},
                {"q": "Which is a sign of dehydration?", "options": ["Bradycardia", "Hypertension", "Decreased skin turgor", "Bradypnea"], "answer": 2},
            ],
            "task": {
                "title": "Write a Clinical Case Report",
                "description": "Write a 500-word clinical case report for a hypothetical patient with Type 2 Diabetes. Include: chief complaint, history, examination findings, investigations, diagnosis, and management plan using SOAP format.",
                "deliverable": "Word document / PDF case report",
                "skills": ["Clinical Reasoning", "Medical Writing", "Diagnosis"],
            }
        },
    ],
    "Physiotherapist": [
        {
            "month": 1,
            "topic": "Musculoskeletal Anatomy",
            "quiz": [
                {"q": "Which muscle is the primary hip flexor?", "options": ["Gluteus maximus", "Iliopsoas", "Rectus femoris", "Sartorius"], "answer": 1},
                {"q": "What is the rotator cuff?", "options": ["A knee ligament", "4 shoulder muscles", "A hip joint structure", "An ankle tendon"], "answer": 1},
                {"q": "What does ROM stand for?", "options": ["Rate of Movement", "Range of Motion", "Resistance of Muscle", "Rotation of Movement"], "answer": 1},
                {"q": "Which nerve is affected in carpal tunnel syndrome?", "options": ["Ulnar nerve", "Radial nerve", "Median nerve", "Brachial nerve"], "answer": 2},
                {"q": "What is the function of the ACL?", "options": ["Hip stability", "Prevent forward tibial movement", "Ankle dorsiflexion", "Shoulder rotation"], "answer": 1},
            ],
            "task": {
                "title": "Design a Rehabilitation Protocol",
                "description": "Design a 4-week rehabilitation protocol for a patient with a Grade 2 ankle sprain. Include: Week-by-week exercises, sets/reps, progression criteria, and home exercise program. Use evidence-based guidelines.",
                "deliverable": "PDF protocol document with exercise descriptions",
                "skills": ["Rehabilitation", "Exercise Prescription", "Clinical Reasoning"],
            }
        },
        {
            "month": 2,
            "topic": "Exercise Therapy",
            "quiz": [
                {"q": "What is the RICE protocol?", "options": ["Rest, Ice, Compression, Elevation", "Repeat, Increase, Continue, Evaluate", "Rest, Increase, Compress, Exercise", "Relax, Ice, Compress, Elevate"], "answer": 0},
                {"q": "What is proprioception?", "options": ["Muscle strength", "Body position sense", "Pain perception", "Balance only"], "answer": 1},
                {"q": "Which exercise is best for core stability?", "options": ["Bicep curl", "Plank", "Leg press", "Shoulder press"], "answer": 1},
                {"q": "What is eccentric muscle contraction?", "options": ["Muscle shortens", "Muscle lengthens under load", "No movement", "Isometric"], "answer": 1},
                {"q": "What does DOMS stand for?", "options": ["Delayed Onset Muscle Soreness", "Direct Orthopedic Muscle Strain", "Dynamic Orthopedic Movement System", "Delayed Orthopedic Muscle Syndrome"], "answer": 0},
            ],
            "task": {
                "title": "Record and Analyze a Movement Assessment",
                "description": "Record a 2-minute video of yourself performing a Functional Movement Screen (FMS) on a volunteer. Identify any movement dysfunctions, score each pattern (0-3), and write a corrective exercise plan.",
                "deliverable": "Video + written assessment report",
                "skills": ["Movement Analysis", "FMS", "Exercise Prescription"],
            }
        },
        {
            "month": 3,
            "topic": "Electrotherapy & Modalities",
            "quiz": [
                {"q": "What is TENS used for?", "options": ["Muscle strengthening", "Pain management", "Bone healing", "Inflammation reduction only"], "answer": 1},
                {"q": "What does ultrasound therapy promote?", "options": ["Nerve regeneration", "Tissue healing and collagen synthesis", "Bone density", "Muscle relaxation only"], "answer": 1},
                {"q": "What is the thermal effect of ultrasound?", "options": ["Cooling tissue", "Heating deep tissue", "Surface heating only", "No thermal effect"], "answer": 1},
                {"q": "Which modality uses magnetic fields?", "options": ["TENS", "Ultrasound", "PEMF", "Laser therapy"], "answer": 2},
                {"q": "What is contraindicated with TENS?", "options": ["Chronic pain", "Pacemaker users", "Muscle spasm", "Post-surgical pain"], "answer": 1},
            ],
            "task": {
                "title": "Create a Patient Education Brochure",
                "description": "Design a patient education brochure (A4, 2-sided) explaining TENS therapy to a patient with chronic lower back pain. Include: what it is, how it works, how to use at home, precautions, and when to call the physio.",
                "deliverable": "PDF brochure (designed in Canva or Word)",
                "skills": ["Patient Education", "Communication", "Electrotherapy"],
            }
        },
    ],
}

# Default curriculum for any field not listed
DEFAULT_CURRICULUM = MONTHLY_CURRICULUM["Software Developer"]


def get_curriculum(field: str) -> list:
    return MONTHLY_CURRICULUM.get(field, DEFAULT_CURRICULUM)
