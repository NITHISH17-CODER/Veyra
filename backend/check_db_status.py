from app.database.session import SessionLocal
from app.models.course_learning import CourseTrack, CourseModule, CourseLesson, ModuleAssessment, CourseFinalAssessment
from app.models.career import Career
from app.models.skill import Skill

db = SessionLocal()
print("--- CAREERS ---")
careers = db.query(Career).all()
for c in careers:
    print(f"Career {c.id}: {c.name}")

print("\n--- COURSE TRACKS ---")
tracks = db.query(CourseTrack).all()
print('Total Course Tracks:', len(tracks))
for t in tracks:
    m_cnt = db.query(CourseModule).filter(CourseModule.course_id == t.id).count()
    l_cnt = db.query(CourseLesson).join(CourseModule).filter(CourseModule.course_id == t.id).count()
    a_cnt = db.query(ModuleAssessment).join(CourseModule).filter(CourseModule.course_id == t.id).count()
    f_cnt = db.query(CourseFinalAssessment).filter(CourseFinalAssessment.course_id == t.id).count()
    print(f'Track [{t.id}] {t.title} (slug: {t.slug}, career_name: {t.career_name}): {m_cnt} modules, {l_cnt} lessons, {a_cnt} assessments, {f_cnt} final exams')

db.close()
