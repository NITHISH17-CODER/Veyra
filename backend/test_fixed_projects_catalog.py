"""
Automated Validation Test Suite for 90 Fixed Projects Catalog, Strict URL Validation, and AI Analysis.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.connection import SessionLocal
from app.models.project import Project, UserProjectProgress
from app.models.user import User
from app.ai.project_analyzer import validate_submission_url, analyze_project_submission
from app.ai.project_recommender import recommend_projects


class TestFixedProjectsCatalog(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_exact_100_projects_count(self):
        """Verify that the database contains EXACTLY 100 projects."""
        total_projects = self.db.query(Project).count()
        self.assertEqual(total_projects, 100, f"Expected 100 total projects in DB, found {total_projects}")

    def test_20_projects_per_career(self):
        """Verify each of the 5 careers has exactly 20 projects (5 Basic, 5 Intermediate, 5 Advanced, 5 Expert)."""
        careers = [
            "Frontend Developer",
            "Backend Developer",
            "Cybersecurity",
            "Software Development Engineer (SDE)",
            "AI Engineer",
        ]

        for c_name in careers:
            projects = self.db.query(Project).filter(Project.career_name == c_name).all()
            self.assertEqual(
                len(projects), 20,
                f"Career '{c_name}' should have 20 projects, found {len(projects)}"
            )

            basic_count = sum(1 for p in projects if (p.level or "").upper() == "BASIC")
            inter_count = sum(1 for p in projects if (p.level or "").upper() == "INTERMEDIATE")
            adv_count = sum(1 for p in projects if (p.level or "").upper() == "ADVANCED")
            expert_count = sum(1 for p in projects if (p.level or "").upper() == "EXPERT")

            self.assertEqual(basic_count, 5, f"Career '{c_name}' expected 5 Basic projects, found {basic_count}")
            self.assertEqual(inter_count, 5, f"Career '{c_name}' expected 5 Intermediate projects, found {inter_count}")
            self.assertEqual(adv_count, 5, f"Career '{c_name}' expected 5 Advanced projects, found {adv_count}")
            self.assertEqual(expert_count, 5, f"Career '{c_name}' expected 5 Expert projects, found {expert_count}")

    def test_submission_url_validation_rejections(self):
        """Verify invalid submission URLs (Google Drive, LinkedIn, YouTube, etc.) are strictly rejected with exact error message."""
        invalid_urls = [
            "https://drive.google.com/file/d/12345/view",
            "https://www.linkedin.com/in/username",
            "https://youtube.com/watch?v=12345",
            "https://myportfolio.com",
            "invalid-url-string",
            "http://gitlab.com/username/repo",
        ]

        expected_msg = "Invalid submission URL. Please submit a valid GitHub repository URL or Google Colab URL."

        for url in invalid_urls:
            is_valid, platform, msg = validate_submission_url(url)
            self.assertFalse(is_valid, f"URL '{url}' should have been rejected.")
            self.assertEqual(msg, expected_msg, f"URL '{url}' returned wrong error message: {msg}")

    def test_submission_url_validation_acceptances(self):
        """Verify GitHub and Google Colab URLs are accepted."""
        valid_urls = [
            "https://github.com/octocat/Hello-World",
            "https://www.github.com/myuser/my-project-repo",
            "https://colab.research.google.com/drive/1A2B3C4D5E6F7G8H9I",
        ]

        for url in valid_urls:
            is_valid, platform, msg = validate_submission_url(url)
            self.assertTrue(is_valid, f"URL '{url}' should be valid. Error: {msg}")
            self.assertEqual(msg, "")

    def test_ai_project_analysis_engine(self):
        """Verify AI analysis engine compares project submission against requirements and returns full report."""
        project = self.db.query(Project).first()
        self.assertIsNotNone(project)

        project_dict = {
            "title": project.title,
            "level": project.level,
            "career_name": project.career_name,
            "objectives": project.objectives_json or ["Build core app"],
            "technologies": project.technologies_json or ["Python"],
            "requirements": project.requirements_json or ["Clean code"],
            "skills": ["Python", "SQL"],
        }

        res = analyze_project_submission(
            db=self.db,
            project_dict=project_dict,
            submission_url="https://github.com/octocat/Hello-World",
            notes="Testing automated project submission"
        )

        self.assertIn("score", res)
        self.assertGreaterEqual(res["score"], 70)
        self.assertIn("strengths", res)
        self.assertTrue(len(res["strengths"]) > 0)
        self.assertIn("technical_feedback", res)
        self.assertTrue(len(res["technical_feedback"]) > 0)


if __name__ == "__main__":
    unittest.main()
