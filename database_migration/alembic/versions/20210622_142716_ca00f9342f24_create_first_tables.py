"""Create first tables

Revision ID: ca00f9342f24
Revises: 
Create Date: 2021-06-22 14:27:16.079255

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ca00f9342f24"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "drs_objects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("drs_id", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "visas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("elixir_id", sa.String(), nullable=False),
        sa.Column("passport", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("visas")
    op.drop_table("drs_objects")
    # ### end Alembic commands ###
