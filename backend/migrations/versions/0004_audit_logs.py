"""Create audit log records.

Revision ID: 0004_audit_logs
Revises: 0003_operations
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_audit_logs"
down_revision: Union[str, Sequence[str], None] = "0003_operations"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("audit_logs", sa.Column("id", sa.String(length=36), nullable=False), sa.Column("actor_id", sa.String(length=36), nullable=True), sa.Column("action", sa.String(length=120), nullable=False), sa.Column("resource", sa.String(length=160), nullable=False), sa.Column("request_id", sa.String(length=100), nullable=False), sa.Column("outcome", sa.String(length=30), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_audit_logs_actor_id"), "audit_logs", ["actor_id"], unique=False)
    op.create_index(op.f("ix_audit_logs_request_id"), "audit_logs", ["request_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_logs_request_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_actor_id"), table_name="audit_logs")
    op.drop_table("audit_logs")