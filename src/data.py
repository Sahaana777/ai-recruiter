# Canonical skill names and their variations

SKILLS = {
    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml",
        "predictive modelling",
        "predictive modeling",
        "predictive analytics"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
        "dl",
        "neural networks",
        "neural network"
    ],

    "computer vision": [
        "computer vision",
        "computer-vision",
        "cv",
        "image processing",
        "image recognition"
    ],

    "natural language processing": [
        "natural language processing",
        "natural-language processing",
        "nlp",
        "language processing"
    ],

    "data analysis": [
        "data analysis",
        "data analytics",
        "data-analysis",
        "data analyst"
    ],

    "data science": [
        "data science",
        "data-science",
        "data scientist"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "artificial-intelligence",
        "ai"
    ],

    "cybersecurity": [
        "cybersecurity",
        "cyber security",
        "cyber-security",
        "information security",
        "infosec"
    ],

    "web development": [
        "web development",
        "web-development",
        "web dev",
        "web developer"
    ],

    "database management": [
        "database management",
        "database",
        "databases",
        "relational databases"
    ]
}


TECHNOLOGIES = {
    "tensorflow": [
        "tensorflow",
        "tf"
    ],

    "pytorch": [
        "pytorch",
        "torch"
    ],

    "scikit-learn": [
        "scikit-learn",
        "sklearn",
        "scikit learn"
    ],

    "opencv": [
        "opencv",
        "open cv"
    ],

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "sql": [
        "sql",
        "structured query language"
    ],

    "mongodb": [
        "mongodb",
        "mongo db",
        "mongo"
    ],

    "docker": [
        "docker",
        "containerization"
    ],

    "git": [
        "git",
        "version control"
    ],

    "github": [
        "github",
        "git hub"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure",
        "microsoft azure"
    ]
}


LANGUAGES = {
    "python": [
        "python",
        "python programming",
        "python programming language"
    ],

    "java": [
        "java",
        "java programming"
    ],

    "c": [
        "c programming",
        "c language"
    ],

    "c++": [
        "c++",
        "cpp",
        "c plus plus"
    ],

    "javascript": [
        "javascript",
        "js",
        "java script"
    ],

    "typescript": [
        "typescript",
        "ts",
        "type script"
    ],

    "go": [
        "golang",
        "go programming"
    ],

    "rust": [
        "rust",
        "rust programming"
    ]
}

JOBS = {

    "Data Scientist": {
        "description": """
        Analyze data and build predictive models using Python,
        SQL, machine learning, statistics, pandas and numpy.
        Experience with data analysis and data science.
        """,

        "skills": [
            "machine learning",
            "data analysis",
            "data science"
        ],

        "technologies": [
            "pandas",
            "numpy",
            "sql"
        ],

        "languages": [
            "python"
        ]
    },


    "Machine Learning Engineer": {
        "description": """
        Develop and deploy machine learning and deep learning
        models using Python, TensorFlow, PyTorch, Docker and Git.
        Experience with computer vision and artificial intelligence.
        """,

        "skills": {
            "machine learning": 5,
            "deep learning": 5,
            "artificial intelligence": 3,
            "computer vision": 3
        },

        "technologies": {
            "tensorflow": 4,
            "pytorch": 4,
            "docker": 1,
            "git": 1
        },

        "languages": {
            "python": 4
        }
    },


    "Backend Developer": {
        "description": """
        Build backend applications and APIs using Python or Java.
        Work with databases, SQL, MongoDB, Git and Docker.
        Experience with web development and database management.
        """,

        "skills": [
            "web development",
            "database management"
        ],

        "technologies": [
            "sql",
            "mongodb",
            "git",
            "docker"
        ],

        "languages": [
            "python",
            "java"
        ]
    },


    "Computer Vision Engineer": {
        "description": """
        Develop computer vision and image processing systems
        using Python, OpenCV, TensorFlow and PyTorch.
        Experience with deep learning and neural networks.
        """,

        "skills": [
            "computer vision",
            "deep learning"
        ],

        "technologies": [
            "opencv",
            "tensorflow",
            "pytorch"
        ],

        "languages": [
            "python",
            "c++"
        ]
    },


    "Data Analyst": {
        "description": """
        Analyze business data using Python, SQL, pandas and
        data visualization tools. Perform data analysis,
        reporting and statistical analysis.
        """,

        "skills": [
            "data analysis"
        ],

        "technologies": [
            "sql",
            "pandas"
        ],

        "languages": [
            "python"
        ]
    },


    "NLP Engineer": {
        "description": """
        Develop natural language processing and artificial
        intelligence applications using Python, machine
        learning, deep learning and NLP techniques.
        """,

        "skills": [
            "natural language processing",
            "machine learning",
            "deep learning",
            "artificial intelligence"
        ],

        "technologies": [
            "tensorflow",
            "pytorch"
        ],

        "languages": [
            "python"
        ]
    },


    "Cybersecurity Engineer": {
        "description": """
        Protect systems and networks using cybersecurity,
        information security and secure software practices.
        Work with Python, Git and cloud technologies.
        """,

        "skills": [
            "cybersecurity"
        ],

        "technologies": [
            "git",
            "aws"
        ],

        "languages": [
            "python"
        ]
    },


    "Cloud Engineer": {
        "description": """
        Design and maintain cloud infrastructure using AWS,
        Azure, Docker and Git. Develop automated systems
        using Python and work with web applications.
        """,

        "skills": [
            "web development"
        ],

        "technologies": [
            "aws",
            "azure",
            "docker",
            "git"
        ],

        "languages": [
            "python"
        ]
    }
}
