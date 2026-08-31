export const mockCareersData = {
  primaryTarget: {
    title: "Machine Learning Engineer",
    matchPercentage: 92,
    readinessScore: 72,
    averageSalary: "$135,000 / yr",
    demandLevel: "High",
    summary: "Build, deploy, and scale machine learning models into production software systems.",
    strengths: [
      "Strong Python programming foundation",
      "Proficient in Data Manipulation with Pandas & SQL",
      "High affinity for project-based learning",
      "Solid understanding of Git & version control"
    ],
    skillBreakdown: [
      { skill: "Python", current: 95, required: 90, gap: 0, status: "Ready" },
      { skill: "SQL & Databases", current: 70, required: 75, gap: 5, status: "Ready" },
      { skill: "Statistics & Math", current: 40, required: 85, gap: 45, status: "Needs Improvement" },
      { skill: "Machine Learning", current: 45, required: 90, gap: 45, status: "Needs Improvement" },
      { skill: "Deep Learning", current: 15, required: 75, gap: 60, status: "Major Gap" },
      { skill: "MLOps & CI/CD", current: 10, required: 70, gap: 60, status: "Major Gap" }
    ]
  },
  alternatives: [
    {
      id: "car-ds",
      title: "Data Scientist",
      matchPercentage: 87,
      readinessScore: 78,
      demandLevel: "Very High",
      strengths: ["Python", "SQL", "Pandas", "Data Wrangling"],
      mainGaps: ["Advanced Hypothesis Testing", "Business Analytics", "A/B Testing"],
      description: "Extract insights from raw data using statistical models and storytelling."
    },
    {
      id: "car-ai",
      title: "AI Engineer",
      matchPercentage: 81,
      readinessScore: 65,
      demandLevel: "Extremely High",
      strengths: ["Python", "Fast Prototyping", "API Integration"],
      mainGaps: ["LLM Fine-tuning", "RAG Systems", "Vector Databases"],
      description: "Design applications powered by Large Language Models and Foundation APIs."
    },
    {
      id: "car-da",
      title: "Data Analyst",
      matchPercentage: 74,
      readinessScore: 90,
      demandLevel: "High",
      strengths: ["SQL", "Pandas", "Reporting", "Python"],
      mainGaps: ["PowerBI / Tableau", "Advanced Dashboarding"],
      description: "Transform business data into actionable visualizations and strategic insights."
    }
  ]
};
