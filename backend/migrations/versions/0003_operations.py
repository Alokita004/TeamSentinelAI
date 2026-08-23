"""Create evacuation, allocation, and decision records.

Revision ID: 0003_operations
Revises: 0002_agent_execution
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_operations"
down_revision: Union[str, Sequence[str], None] = "0002_agent_execution"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("evacuation_routes", sa.Column("id", sa.String(length=100), nullable=False), sa.Column("incident_id", sa.String(length=80), nullable=False), sa.Column("source_zone_id", sa.String(length=80), nullable=False), sa.Column("destination_shelter_id", sa.String(length=80), nullable=False), sa.Column("status", sa.String(length=30), nullable=False), sa.Column("score", sa.Float(), nullable=False), sa.Column("distance_km", sa.Float(), nullable=False), sa.Column("eta_minutes", sa.Integer(), nullable=False), sa.Column("blocked_reason", sa.String(length=160), nullable=True), sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_evacuation_routes_incident_id"), "evacuation_routes", ["incident_id"], unique=False)
    op.create_table("resource_allocations", sa.Column("id", sa.String(length=100), nullable=False), sa.Column("incident_id", sa.String(length=80), nullable=False), sa.Column("resource_id", sa.String(length=80), nullable=False), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("status", sa.String(length=30), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_resource_allocations_incident_id"), "resource_allocations", ["incident_id"], unique=False)
    op.create_table("decision_records", sa.Column("id", sa.String(length=100), nullable=False), sa.Column("incident_id", sa.String(length=80), nullable=False), sa.Column("summary", sa.Text(), nullable=False), sa.Column("status", sa.String(length=30), nullable=False), sa.Column("capacity_shortfall", sa.Integer(), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_decision_records_incident_id"), "decision_records", ["incident_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_decision_records_incident_id"), table_name="decision_records")
    op.drop_table("decision_records")
    op.drop_index(op.f("ix_resource_allocations_incident_id"), table_name="resource_allocations")
    op.drop_table("resource_allocations")
    op.drop_index(op.f("ix_evacuation_routes_incident_id"), table_name="evacuation_routes")
    op.drop_table("evacuation_routes")
