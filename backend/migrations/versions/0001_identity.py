"""Create roles, users, and user role assignments.

Revision ID: 0001_identity
Revises:
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_identity"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("roles", sa.Column("id", sa.String(length=36), nullable=False), sa.Column("name", sa.String(length=80), nullable=False), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("name"))
    op.create_table("users", sa.Column("id", sa.String(length=36), nullable=False), sa.Column("email", sa.String(length=320), nullable=False), sa.Column("password_hash", sa.String(length=256), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("email"))
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table("user_roles", sa.Column("user_id", sa.String(length=36), nullable=False), sa.Column("role_id", sa.String(length=36), nullable=False), sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"), sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("user_id", "role_id"))
    op.create_table("incidents", sa.Column("id", sa.String(length=80), nullable=False), sa.Column("disaster_type", sa.String(length=40), nullable=False), sa.Column("name", sa.String(length=160), nullable=False), sa.Column("status", sa.String(length=30), nullable=False), sa.Column("severity", sa.String(length=30), nullable=False), sa.Column("started_at", sa.DateTime(timezone=True), nullable=True), sa.Column("signal_provider", sa.String(length=100), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_table("affected_zones", sa.Column("id", sa.String(length=80), nullable=False), sa.Column("incident_id", sa.String(length=80), nullable=True), sa.Column("name", sa.String(length=120), nullable=False), sa.Column("risk_level", sa.String(length=30), nullable=False), sa.Column("population", sa.Integer(), nullable=False), sa.ForeignKeyConstraint(["incident_id"], ["incidents.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_table("shelters", sa.Column("id", sa.String(length=80), nullable=False), sa.Column("name", sa.String(length=160), nullable=False), sa.Column("capacity", sa.Integer(), nullable=False), sa.Column("available", sa.Integer(), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_table("resources", sa.Column("id", sa.String(length=80), nullable=False), sa.Column("name", sa.String(length=160), nullable=False), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("unit", sa.String(length=40), nullable=False), sa.PrimaryKeyConstraint("id"))


def downgrade() -> None:
    op.drop_table("resources")
    op.drop_table("shelters")
    op.drop_table("affected_zones")
    op.drop_table("incidents")
    op.drop_table("user_roles")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("roles")
