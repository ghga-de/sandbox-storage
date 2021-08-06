"""Removed Passport Storage, added metadata for DrsObject

Revision ID: bbb58e66cf6f
Revises: ca00f9342f24
Create Date: 2021-08-06 16:16:12.423573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bbb58e66cf6f'
down_revision = 'ca00f9342f24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visas')
    op.add_column('drs_objects', sa.Column('size', sa.Integer(), nullable=True))
    op.add_column('drs_objects', sa.Column('created_time', sa.DateTime(), nullable=False))
    op.add_column('drs_objects', sa.Column('checksum_md5', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('drs_objects', 'checksum_md5')
    op.drop_column('drs_objects', 'created_time')
    op.drop_column('drs_objects', 'size')
    op.create_table('visas',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('elixir_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('passport', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='visas_pkey')
    )
    # ### end Alembic commands ###
