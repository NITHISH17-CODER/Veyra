"""create_courses_and_course_skills_tables

Revision ID: 7fa1fcf3d7aa
Revises: 33f527297adc
Create Date: 2026-08-22 21:04:19.985416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fa1fcf3d7aa'
down_revision: Union[str, Sequence[str], None] = '33f527297adc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Create 'courses' table ──────────────────────────────────────
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('provider', sa.String(length=100), nullable=True),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('is_free', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True, server_default='0.00'),
        sa.Column('currency', sa.String(length=10), nullable=True, server_default='USD'),
        sa.Column('difficulty', sa.String(length=50), nullable=True),
        sa.Column('duration_hours', sa.Float(), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint('duration_hours IS NULL OR duration_hours >= 0', name='ck_course_duration_positive'),
        sa.CheckConstraint('price IS NULL OR price >= 0', name='ck_course_price_positive'),
        sa.CheckConstraint('rating IS NULL OR (rating >= 0.0 AND rating <= 5.0)', name='ck_course_rating_range'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_courses_title'), 'courses', ['title'], unique=False)

    # ── 2. Create 'course_skills' table ────────────────────────────────
    op.create_table(
        'course_skills',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('coverage_level', sa.Integer(), nullable=False, server_default='1'),
        sa.CheckConstraint('coverage_level >= 1 AND coverage_level <= 5', name='ck_course_skill_coverage_level'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('course_id', 'skill_id', name='uq_course_skill'),
    )
    op.create_index(op.f('ix_course_skills_course_id'), 'course_skills', ['course_id'], unique=False)
    op.create_index(op.f('ix_course_skills_skill_id'), 'course_skills', ['skill_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_course_skills_skill_id'), table_name='course_skills')
    op.drop_index(op.f('ix_course_skills_course_id'), table_name='course_skills')
    op.drop_table('course_skills')
    op.drop_index(op.f('ix_courses_title'), table_name='courses')
    op.drop_table('courses')
