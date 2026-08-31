export const mockProgressData = {
  overallProgress: 72,
  streakDays: 7,
  weeklyGoalHours: 10,
  hoursLearnedThisWeek: 8.5,
  totalHoursLearned: 34.5,
  skillsMasteredCount: 8,
  coursesCompletedCount: 4,
  projectsCompletedCount: 2,
  
  weeklyLearningHours: [
    { day: "Mon", hours: 1.5, target: 1.5 },
    { day: "Tue", hours: 2.0, target: 1.5 },
    { day: "Wed", hours: 1.0, target: 1.5 },
    { day: "Thu", hours: 2.5, target: 1.5 },
    { day: "Fri", hours: 1.5, target: 1.5 },
    { day: "Sat", hours: 3.0, target: 2.0 },
    { day: "Sun", hours: 0.0, target: 1.0 }
  ],

  skillGrowthTimeline: [
    { month: "Jan", Python: 40, SQL: 30, Statistics: 10, MachineLearning: 5 },
    { month: "Feb", Python: 60, SQL: 50, Statistics: 20, MachineLearning: 15 },
    { month: "Mar", Python: 75, SQL: 65, Statistics: 30, MachineLearning: 25 },
    { month: "Apr", Python: 90, SQL: 70, Statistics: 40, MachineLearning: 45 }
  ],

  skillComparison: [
    { skill: "Python", start: 40, current: 90, target: 95 },
    { skill: "SQL", start: 30, current: 70, target: 80 },
    { skill: "Pandas", start: 20, current: 75, target: 85 },
    { skill: "Statistics", start: 10, current: 40, target: 85 },
    { skill: "Machine Learning", start: 5, current: 45, target: 90 },
    { skill: "Deep Learning", start: 0, current: 15, target: 75 },
    { skill: "MLOps", start: 0, current: 10, target: 70 }
  ],

  assessmentScoresHistory: [
    { test: "Python Fundamentals", score: 92, date: "2026-02-10" },
    { test: "SQL Query Optimization", score: 85, date: "2026-03-01" },
    { test: "Pandas Data Wrangling", score: 88, date: "2026-03-20" },
    { test: "Statistics Diagnostic", score: 82, date: "2026-04-12" }
  ]
};
