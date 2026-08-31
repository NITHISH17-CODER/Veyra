export const initialChatMessages = [
  {
    id: "msg-1",
    sender: "ai",
    timestamp: "10:30 AM",
    content: "Hi Nithish 👋 I'm your Veyra AI learning assistant.\n\nI've analyzed your goal of becoming a Machine Learning Engineer. You're currently at 72% career readiness! How can I help guide your learning today?",
    suggestions: [
      "What should I learn today?",
      "Why do I need statistics?",
      "Can I skip this course?",
      "What project should I build next?",
      "How close am I to my goal?",
      "Should I learn TensorFlow or PyTorch?"
    ]
  }
];

export const precalculatedAiAnswers = {
  "What should I learn today?": "Based on your current roadmap position, you should focus on **Phase 2: Practical Statistics & Probability for Data Science** (Module 3: Hypothesis Testing).\n\nCompleting this 45-minute lesson will boost your Statistics foundation from 40% to 55% and bring you one step closer to unlocking Machine Learning projects!",

  "Why do I need statistics?": "Statistics is the underlying engine for all Machine Learning algorithm decisions!\n\n1. **P-values & Confidence Intervals**: Essential for feature selection and A/B test validation.\n2. **Probability Distributions**: Underpin Naive Bayes classifiers and Gaussian Mixture models.\n3. **Model Evaluation**: Metrics like Precision, Recall, and ROC-AUC are based on conditional probability.\n\nMastering statistics now will make learning Scikit-Learn algorithms much easier!",

  "Can I skip this course?": "You can take the **Statistics & Probability Diagnostic Assessment**! If you score **80% or higher**, Veyra AI will automatically mark this module as completed and fast-track you straight to **Phase 3: Machine Learning Fundamentals**.",

  "What project should I build next?": "I strongly recommend the **Customer Churn Prediction Engine**!\n\nIt challenges you to use Pandas for data wrangling and Scikit-Learn for binary classification (Logistic Regression & XGBoost). It addresses the exact skill gaps identified in your profile.",

  "How close am I to my goal?": "You are currently at **72% Career Readiness** for Machine Learning Engineer positions!\n\n- **Python & SQL**: Complete (90% + 70%)\n- **Statistics**: In Progress (40% → 80% target)\n- **Machine Learning**: Upcoming (45% → 90% target)\n\nAt your current pace of 10 hours/week, you'll reach job-readiness in approximately **4.5 months**.",

  "Should I learn TensorFlow or PyTorch?": "For your Machine Learning Engineer track, we recommend **PyTorch**! PyTorch is currently used in over 70% of modern AI research papers and top tech companies (Meta, OpenAI, Apple) for Deep Learning and LLM fine-tuning."
};
