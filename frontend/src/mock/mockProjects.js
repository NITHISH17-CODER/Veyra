export const mockProjectsData = [
  {
    id: "proj-201",
    title: "Customer Churn Prediction Engine",
    category: "Classification & ML",
    difficulty: "Intermediate",
    estimatedHours: 12,
    skills: ["Python", "Pandas", "Scikit-Learn", "Machine Learning", "Classification"],
    image: "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=600&q=80",
    whyRecommended: "Builds the exact classification skills missing from your current profile, applying Random Forest & Logistic Regression.",
    problemStatement: "Telecommunication provider is experiencing a 15% monthly subscriber loss. The goal is to predict customer churn probability 30 days prior to contract expiration.",
    objectives: [
      "Clean and preprocess telecom dataset of 10,000 subscriber records",
      "Perform Exploratory Data Analysis (EDA) on customer retention factors",
      "Train Logistic Regression, XGBoost, and Random Forest classifiers",
      "Evaluate models using ROC-AUC, Precision, and Recall metrics",
      "Generate business recommendations to reduce churn by 20%"
    ],
    expectedOutcome: "A clean Python notebook, serialized Scikit-Learn pipeline, and executive report with feature importance rankings.",
    datasetInfo: "7,043 rows, 21 feature columns (Tenure, MonthlyCharges, TechSupport, ContractType, Churn).",
    suggestedTechnologies: ["Python 3.11", "Pandas", "Scikit-Learn", "XGBoost", "Matplotlib", "Seaborn"],
    milestones: [
      { step: "Data Cleaning & Imputation", status: "Done" },
      { step: "Exploratory Data Analysis (EDA)", status: "In Progress" },
      { step: "Model Training & Hyperparameter Tuning", status: "Pending" },
      { step: "Model Evaluation & Confusion Matrix", status: "Pending" },
      { step: "Final Project Submission & Code Review", status: "Pending" }
    ]
  },
  {
    id: "proj-202",
    title: "E-Commerce Recommendation System",
    category: "Recommendation Engines",
    difficulty: "Intermediate",
    estimatedHours: 16,
    skills: ["Python", "Pandas", "Collaborative Filtering", "Matrix Factorization"],
    image: "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=600&q=80",
    whyRecommended: "Directly aligns with your goal of mastering personalized recommendation algorithms.",
    problemStatement: "Build item-based and user-based collaborative filtering models to recommend top 5 products based on previous shopping carts.",
    objectives: [
      "Construct user-item interaction matrix",
      "Implement Cosine Similarity and SVD factorization",
      "Calculate Mean Absolute Error (MAE) and Precision@K",
      "Deploy interactive Streamlit UI for live recommendations"
    ],
    expectedOutcome: "Interactive Streamlit web interface demonstrating live recommendations.",
    datasetInfo: "MovieLens / Amazon Product Review dataset (100k ratings).",
    suggestedTechnologies: ["Python", "Surprise Lib", "Pandas", "Streamlit"],
    milestones: [
      { step: "Interaction Matrix Setup", status: "Done" },
      { step: "Cosine Similarity Implementation", status: "In Progress" },
      { step: "Streamlit UI Build", status: "Pending" }
    ]
  },
  {
    id: "proj-203",
    title: "Automated Chest X-Ray Pneumonia Classifier",
    category: "Computer Vision & PyTorch",
    difficulty: "Advanced",
    estimatedHours: 20,
    skills: ["Deep Learning", "PyTorch", "CNN", "Transfer Learning"],
    image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=600&q=80",
    whyRecommended: "Accelerates your Deep Learning readiness with real-world medical image classification.",
    problemStatement: "Classify chest X-Ray images as Normal or Pneumonia with >94% sensitivity.",
    objectives: [
      "Preprocess DICOM / JPEG medical image dataset",
      "Fine-tune ResNet50 vision transformer",
      "Generate Grad-CAM heatmaps for model interpretability",
      "Evaluate ROC-AUC & Confusion Matrix on held-out test split"
    ],
    expectedOutcome: "Trained PyTorch model weights and visual interpretability dashboard.",
    datasetInfo: "5,863 chest X-Ray images categorized into Pneumonia vs Normal.",
    suggestedTechnologies: ["PyTorch", "Torchvision", "Albumentations", "OpenCV"],
    milestones: [
      { step: "Data Loading & Transformations", status: "Done" },
      { step: "ResNet Fine-Tuning", status: "Pending" },
      { step: "Grad-CAM Visualization", status: "Pending" }
    ]
  },
  {
    id: "proj-204",
    title: "Real-Time Fraud Detection Microservice with MLOps",
    category: "MLOps & FastAPI",
    difficulty: "Advanced",
    estimatedHours: 24,
    skills: ["MLOps", "FastAPI", "Docker", "MLflow", "Scikit-Learn"],
    image: "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=600&q=80",
    whyRecommended: "Demonstrates production MLOps deployment skills for top-tier Machine Learning Engineer roles.",
    problemStatement: "Deploy a credit card fraud classification model as a sub-10ms REST API using FastAPI and Docker containers.",
    objectives: [
      "Train isolation forest & LightGBM on imbalanced credit dataset",
      "Wrap inference in FastAPI async endpoint",
      "Build Docker image and test endpoint latency with Locust",
      "Setup GitHub Actions for continuous integration"
    ],
    expectedOutcome: "Production-ready GitHub repo with CI/CD GitHub Actions and Dockerfile.",
    datasetInfo: "Kaggle Credit Card Fraud dataset (284k transactions).",
    suggestedTechnologies: ["FastAPI", "Docker", "LightGBM", "MLflow", "Locust"],
    milestones: [
      { step: "Imbalanced Training", status: "Done" },
      { step: "FastAPI REST Server", status: "In Progress" },
      { step: "Docker Containerization", status: "Pending" }
    ]
  }
];

