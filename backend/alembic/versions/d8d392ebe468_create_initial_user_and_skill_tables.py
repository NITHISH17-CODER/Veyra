"""create initial user, learner_profile, skill, and user_skill tables

Revision ID: d8d392ebe468
Revises: 
Create Date: 2026-08-22 20:50:52.919564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8d392ebe468'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Create 'users' table ────────────────────────────────────────
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # ── 2. Create 'learner_profiles' table ─────────────────────────────
    op.create_table(
        'learner_profiles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('education', sa.String(length=200), nullable=True),
        sa.Column('experience_level', sa.String(length=50), nullable=True),
        sa.Column('career_goal', sa.String(length=500), nullable=True),
        sa.Column('learning_hours_per_week', sa.Integer(), nullable=True),
        sa.Column('learning_preference', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq_learner_profile_user_id'),
    )
    op.create_index(op.f('ix_learner_profiles_user_id'), 'learner_profiles', ['user_id'], unique=True)

    # ── 3. Create 'skills' table ───────────────────────────────────────
    op.create_table(
        'skills',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_skills_name'), 'skills', ['name'], unique=True)

    # ── 4. Create 'user_skills' table ──────────────────────────────────
    op.create_table(
        'user_skills',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('proficiency', sa.Integer(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint('proficiency >= 1 AND proficiency <= 5', name='ck_proficiency_range'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'skill_id', name='uq_user_skill'),
    )
    op.create_index(op.f('ix_user_skills_skill_id'), 'user_skills', ['skill_id'], unique=False)
    op.create_index(op.f('ix_user_skills_user_id'), 'user_skills', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_skills_user_id'), table_name='user_skills')
    op.drop_index(op.f('ix_user_skills_skill_id'), table_name='user_skills')
    op.drop_table('user_skills')
    op.drop_index(op.f('ix_skills_name'), table_name='skills')
    op.drop_table('skills')
    op.drop_index(op.f('ix_learner_profiles_user_id'), table_name='learner_profiles')
    op.drop_table('learner_profiles')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
