export const mockAssessmentsList = [
  {
    id: "asm-301",
    title: "Statistics & Probability Diagnostic Test",
    skill: "Statistics",
    questionCount: 5,
    difficulty: "Intermediate",
    estimatedMinutes: 15,
    bestScore: "Pending",
    status: "Available",
    badgeColor: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
    questions: [
      {
        id: "q1",
        question: "In hypothesis testing, what does a p-value of 0.03 indicate when testing at a significance level (alpha) of 0.05?",
        options: [
          "Reject the null hypothesis; there is statistically significant evidence.",
          "Fail to reject the null hypothesis; the result is due to random chance.",
          "The probability that the null hypothesis is true is exactly 3%.",
          "The sample size was too small to make a conclusion."
        ],
        correctIndex: 0,
        explanation: "Since p-value (0.03) is less than alpha (0.05), we reject the null hypothesis in favor of the alternative hypothesis."
      },
      {
        id: "q2",
        question: "Which probability distribution describes the number of successes in a fixed number of independent Bernoulli trials?",
        options: [
          "Poisson Distribution",
          "Binomial Distribution",
          "Normal Distribution",
          "Exponential Distribution"
        ],
        correctIndex: 1,
        explanation: "The Binomial distribution models n independent trial outcomes with binary success/failure outcomes."
      },
      {
        id: "q3",
        question: "What is the primary effect of severe right-skewness on the relationship between Mean, Median, and Mode?",
        options: [
          "Mean < Median < Mode",
          "Mean = Median = Mode",
          "Mode < Median < Mean",
          "Median < Mode < Mean"
        ],
        correctIndex: 2,
        explanation: "Right-skewed distributions have a long tail to the right, pulling the Mean higher than the Median and Mode."
      },
      {
        id: "q4",
        question: "What theorem states that the sampling distribution of the sample mean approaches a Normal distribution as sample size grows, regardless of population shape?",
        options: [
          "Law of Large Numbers",
          "Central Limit Theorem",
          "Bayes' Theorem",
          "Chebyshev's Inequality"
        ],
        correctIndex: 1,
        explanation: "The Central Limit Theorem (CLT) guarantees normality for large sample means."
      },
      {
        id: "q5",
        question: "When evaluating a diagnostic test for fraud where missing a fraud case is extremely costly, which metric should be prioritized?",
        options: [
          "Precision",
          "Recall (Sensitivity)",
          "Accuracy",
          "Specificity"
        ],
        correctIndex: 1,
        explanation: "High Recall minimizes False Negatives, ensuring very few fraud cases are missed."
      }
    ]
  },
  {
    id: "asm-302",
    title: "Python Data Science Mastery",
    skill: "Python",
    questionCount: 5,
    difficulty: "Advanced",
    estimatedMinutes: 15,
    bestScore: "92%",
    status: "Available",
    badgeColor: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
    questions: [
      {
        id: "py1",
        question: "What is the average time complexity of key lookup in a Python dictionary?",
        options: ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        correctIndex: 0,
        explanation: "Python dicts are implemented using hash tables, offering O(1) average lookup complexity."
      },
      {
        id: "py2",
        question: "Which keyword converts a standard Python function into a generator iterator?",
        options: ["return", "yield", "emit", "async"],
        correctIndex: 1,
        explanation: "Functions containing the yield keyword return a generator object instead of terminating."
      },
      {
        id: "py3",
        question: "What is the key functional difference between a list comprehension and a generator expression in Python?",
        options: [
          "List comprehensions return tuples; generator expressions return lists.",
          "List comprehensions construct the entire list in memory immediately; generators evaluate items lazily.",
          "Generator expressions are slower and use more RAM.",
          "There is no difference in memory allocation."
        ],
        correctIndex: 1,
        explanation: "Generator expressions compute items one by one on-demand (lazy evaluation), saving memory."
      },
      {
        id: "py4",
        question: "What does the @classmethod decorator pass as its implicit first argument to the decorated function?",
        options: ["The instance self", "The class object cls", "The global module scope", "No implicit argument"],
        correctIndex: 1,
        explanation: "Class methods receive the class object (cls) as their first positional argument."
      },
      {
        id: "py5",
        question: "How does Pandas copy behavior differ when slicing a DataFrame view versus calling .copy()?",
        options: [
          "Slicing creates a deep copy by default.",
          "Modifying a slice view may trigger a SettingWithCopyWarning, whereas .copy() creates an independent DataFrame.",
          ".copy() is always faster than slicing.",
          "Slice views cannot be modified."
        ],
        correctIndex: 1,
        explanation: "Calling .copy() guarantees a separate data buffer, preventing unintended mutations or SettingWithCopy warnings."
      }
    ]
  },
  {
    id: "asm-303",
    title: "Machine Learning Concepts Assessment",
    skill: "Machine Learning",
    questionCount: 5,
    difficulty: "Intermediate",
    estimatedMinutes: 20,
    bestScore: "Pending",
    status: "Available",
    badgeColor: "bg-slate-800 text-slate-400 border-slate-700",
    questions: [
      {
        id: "ml1",
        question: "What primary issue occurs when a machine learning model scores 99% accuracy on training data but 62% on test data?",
        options: ["Underfitting", "Overfitting (High Variance)", "High Bias", "Data Leakage"],
        correctIndex: 1,
        explanation: "A large gap between high training accuracy and lower test accuracy signifies overfitting."
      },
      {
        id: "ml2",
        question: "Which technique helps penalize large model coefficients in linear regression to prevent overfitting?",
        options: ["L1/L2 Regularization (Lasso/Ridge)", "One-Hot Encoding", "MinMax Scaling", "Principal Component Analysis"],
        correctIndex: 0,
        explanation: "Regularization terms (L1/L2) add penalty constraints on coefficient magnitudes."
      },
      {
        id: "ml3",
        question: "In Random Forest classification, how are individual decision trees made diverse?",
        options: [
          "By boosting residual errors sequentially.",
          "Using Bagging (Bootstrap Aggregation) and random subset feature selection per split.",
          "Using a single gradient descent learning rate.",
          "By removing depth constraints on all trees."
        ],
        correctIndex: 1,
        explanation: "Random Forest combines bootstrap samples with random feature subsets to lower variance."
      },
      {
        id: "ml4",
        question: "What metric is most appropriate for evaluating an imbalanced binary classifier where positive cases are rare?",
        options: ["Accuracy", "Area Under ROC Curve (ROC-AUC) & PR-AUC", "Mean Squared Error", "R-Squared"],
        correctIndex: 1,
        explanation: "ROC-AUC and Precision-Recall AUC reflect ranking quality across all thresholds regardless of class imbalance."
      },
      {
        id: "ml5",
        question: "Which algorithm uses distance metrics (e.g. Euclidean distance) and requires feature normalization before model training?",
        options: ["K-Nearest Neighbors (KNN)", "Decision Trees", "Naive Bayes", "XGBoost"],
        correctIndex: 0,
        explanation: "Distance-based algorithms like KNN are highly sensitive to feature scales and require standardization."
      }
    ]
  },
  {
    id: "asm-304",
    title: "SQL & Relational Databases Test",
    skill: "SQL",
    questionCount: 5,
    difficulty: "Intermediate",
    estimatedMinutes: 15,
    bestScore: "85%",
    status: "Available",
    badgeColor: "bg-blue-500/20 text-blue-300 border-blue-500/30",
    questions: [
      {
        id: "sql1",
        question: "What SQL clause is used to filter aggregated group records calculated by GROUP BY?",
        options: ["WHERE", "HAVING", "ORDER BY", "QUALIFY"],
        correctIndex: 1,
        explanation: "The HAVING clause filters groups after aggregation, whereas WHERE filters raw rows prior to aggregation."
      },
      {
        id: "sql2",
        question: "Which SQL Window function assigns sequential rank values while preserving gaps for duplicate rank ties?",
        options: ["ROW_NUMBER()", "RANK()", "DENSE_RANK()", "LAG()"],
        correctIndex: 1,
        explanation: "RANK() skips rank numbers after ties (e.g., 1, 2, 2, 4), whereas DENSE_RANK() does not leave gaps."
      },
      {
        id: "sql3",
        question: "What type of JOIN returns all records from the left table and matching records from the right table?",
        options: ["INNER JOIN", "LEFT OUTER JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
        correctIndex: 1,
        explanation: "LEFT JOIN preserves all rows from the left table regardless of matching rows in the right table."
      },
      {
        id: "sql4",
        question: "How does creating a B-Tree Index on a frequently queried foreign key column impact performance?",
        options: [
          "Speeds up SELECT queries but may slightly slow down INSERT/UPDATE writes.",
          "Slows down SELECT queries.",
          "Has no effect on database performance.",
          "Eliminates the need for primary keys."
        ],
        correctIndex: 0,
        explanation: "Indexes trade disk space and write overhead for significantly faster read lookups."
      },
      {
        id: "sql5",
        question: "What property in ACID database transactions guarantees that once a transaction commits, it remains committed even during power failures?",
        options: ["Atomicity", "Consistency", "Isolation", "Durability"],
        correctIndex: 3,
        explanation: "Durability ensures committed state changes are persisted permanently to non-volatile storage."
      }
    ]
  }
];

