"""create_careers_and_career_skills_tables

Revision ID: 33f527297adc
Revises: d8d392ebe468
Create Date: 2026-08-22 21:00:43.574386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33f527297adc'
down_revision: Union[str, Sequence[str], None] = 'd8d392ebe468'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Create 'careers' table ───────────────────────────────────────
    op.create_table(
        'careers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_careers_name'), 'careers', ['name'], unique=True)

    # ── 2. Create 'career_skills' table ────────────────────────────────
    op.create_table(
        'career_skills',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('career_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('required_level', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('importance', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint('required_level >= 1 AND required_level <= 5', name='ck_career_skill_required_level'),
        sa.CheckConstraint('importance >= 1 AND importance <= 5', name='ck_career_skill_importance'),
        sa.ForeignKeyConstraint(['career_id'], ['careers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('career_id', 'skill_id', name='uq_career_skill'),
    )
    op.create_index(op.f('ix_career_skills_career_id'), 'career_skills', ['career_id'], unique=False)
    op.create_index(op.f('ix_career_skills_skill_id'), 'career_skills', ['skill_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_career_skills_skill_id'), table_name='career_skills')
    op.drop_index(op.f('ix_career_skills_career_id'), table_name='career_skills')
    op.drop_table('career_skills')
    op.drop_index(op.f('ix_careers_name'), table_name='careers')
    op.drop_table('careers')
