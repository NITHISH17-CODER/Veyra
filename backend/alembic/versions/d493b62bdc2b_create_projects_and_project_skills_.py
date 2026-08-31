"""create_projects_and_project_skills_tables

Revision ID: d493b62bdc2b
Revises: 7fa1fcf3d7aa
Create Date: 2026-08-22 21:07:01.209684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd493b62bdc2b'
down_revision: Union[str, Sequence[str], None] = '7fa1fcf3d7aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Create 'projects' table ─────────────────────────────────────
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(length=50), nullable=True),
        sa.Column('estimated_hours', sa.Float(), nullable=True),
        sa.Column('github_url', sa.String(length=500), nullable=True),
        sa.Column('dataset_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint('estimated_hours IS NULL OR estimated_hours >= 0', name='ck_project_estimated_hours_positive'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_projects_title'), 'projects', ['title'], unique=False)

    # ── 2. Create 'project_skills' table ───────────────────────────────
    op.create_table(
        'project_skills',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('importance', sa.Integer(), nullable=False, server_default='3'),
        sa.CheckConstraint('importance >= 1 AND importance <= 5', name='ck_project_skill_importance'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id', 'skill_id', name='uq_project_skill'),
    )
    op.create_index(op.f('ix_project_skills_project_id'), 'project_skills', ['project_id'], unique=False)
    op.create_index(op.f('ix_project_skills_skill_id'), 'project_skills', ['skill_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_project_skills_skill_id'), table_name='project_skills')
    op.drop_index(op.f('ix_project_skills_project_id'), table_name='project_skills')
    op.drop_table('project_skills')
    op.drop_index(op.f('ix_projects_title'), table_name='projects')
    op.drop_table('projects')
