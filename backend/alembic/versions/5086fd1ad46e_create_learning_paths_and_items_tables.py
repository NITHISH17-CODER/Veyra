"""create_learning_paths_and_items_tables

Revision ID: 5086fd1ad46e
Revises: d493b62bdc2b
Create Date: 2026-08-22 21:10:01.581376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5086fd1ad46e'
down_revision: Union[str, Sequence[str], None] = 'd493b62bdc2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Create 'learning_paths' table ───────────────────────────────
    op.create_table(
        'learning_paths',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('target_career_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('estimated_months', sa.Float(), nullable=True),
        sa.Column('weekly_hours', sa.Float(), nullable=True),
        sa.Column('readiness_score', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint('estimated_months IS NULL OR estimated_months >= 0', name='ck_path_estimated_months_positive'),
        sa.CheckConstraint('readiness_score IS NULL OR (readiness_score >= 0.0 AND readiness_score <= 100.0)', name='ck_path_readiness_score'),
        sa.CheckConstraint('weekly_hours IS NULL OR weekly_hours >= 0', name='ck_path_weekly_hours_positive'),
        sa.ForeignKeyConstraint(['target_career_id'], ['careers.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_learning_paths_target_career_id'), 'learning_paths', ['target_career_id'], unique=False)
    op.create_index(op.f('ix_learning_paths_user_id'), 'learning_paths', ['user_id'], unique=False)

    # ── 2. Create 'learning_path_items' table ──────────────────────────
    op.create_table(
        'learning_path_items',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('learning_path_id', sa.Integer(), nullable=False),
        sa.Column('item_type', sa.String(length=50), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=True),
        sa.Column('sequence_number', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='locked'),
        sa.Column('is_locked', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('estimated_hours', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint("item_type IN ('course', 'project', 'assessment')", name='ck_item_type'),
        sa.CheckConstraint("status IN ('locked', 'current', 'completed', 'skipped')", name='ck_item_status'),
        sa.CheckConstraint('estimated_hours IS NULL OR estimated_hours >= 0', name='ck_item_estimated_hours_positive'),
        sa.ForeignKeyConstraint(['learning_path_id'], ['learning_paths.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('learning_path_id', 'sequence_number', name='uq_path_sequence'),
    )
    op.create_index(op.f('ix_learning_path_items_learning_path_id'), 'learning_path_items', ['learning_path_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_learning_path_items_learning_path_id'), table_name='learning_path_items')
    op.drop_table('learning_path_items')
    op.drop_index(op.f('ix_learning_paths_user_id'), table_name='learning_paths')
    op.drop_index(op.f('ix_learning_paths_target_career_id'), table_name='learning_paths')
    op.drop_table('learning_paths')
