"""Create LangGraph execution records and agent events.

Revision ID: 0002_agent_execution
Revises: 0001_identity
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_agent_execution"
down_revision: Union[str, Sequence[str], None] = "0001_identity"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("agent_executions", sa.Column("id", sa.String(length=36), nullable=False), sa.Column("incident_id", sa.String(length=80), nullable=False), sa.Column("status", sa.String(length=30), nullable=False), sa.Column("started_at", sa.DateTime(timezone=True), nullable=False), sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True), sa.Column("error_count", sa.Integer(), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_agent_executions_incident_id"), "agent_executions", ["incident_id"], unique=False)
    op.create_table("agent_events", sa.Column("id", sa.String(length=36), nullable=False), sa.Column("execution_id", sa.String(length=36), nullable=False), sa.Column("sequence", sa.Integer(), nullable=False), sa.Column("agent_name", sa.String(length=50), nullable=False), sa.Column("status", sa.String(length=30), nullable=False), sa.Column("message", sa.String(length=240), nullable=False), sa.Column("output_json", sa.Text(), nullable=False), sa.ForeignKeyConstraint(["execution_id"], ["agent_executions.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_agent_events_execution_id"), "agent_events", ["execution_id"], unique=False)
    op.create_table("recommendations", sa.Column("id", sa.String(length=36), nullable=False), sa.Column("execution_id", sa.String(length=36), nullable=False), sa.Column("priority", sa.Integer(), nullable=False), sa.Column("title", sa.String(length=200), nullable=False), sa.Column("rationale", sa.Text(), nullable=False), sa.Column("confidence", sa.Float(), nullable=False), sa.ForeignKeyConstraint(["execution_id"], ["agent_executions.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_recommendations_execution_id"), "recommendations", ["execution_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_recommendations_execution_id"), table_name="recommendations")
    op.drop_table("recommendations")
    op.drop_index(op.f("ix_agent_events_execution_id"), table_name="agent_events")
    op.drop_table("agent_events")
    op.drop_index(op.f("ix_agent_executions_incident_id"), table_name="agent_executions")
    op.drop_table("agent_executions")
