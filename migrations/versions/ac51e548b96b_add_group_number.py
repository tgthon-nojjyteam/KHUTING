"""add group number

Revision ID: ac51e548b96b
Revises: 6eef20a0de46
Create Date: 2024-08-26 03:14:50.771898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ac51e548b96b'
down_revision = '6eef20a0de46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fcuser', schema=None) as batch_op:
        batch_op.add_column(sa.Column('matched_team_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('groupnumber', sa.String(length=50), nullable=True))
        batch_op.drop_column('room')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fcuser', schema=None) as batch_op:
        batch_op.add_column(sa.Column('room', mysql.VARCHAR(length=50), nullable=True))
        batch_op.drop_column('groupnumber')
        batch_op.drop_column('matched_team_id')

    # ### end Alembic commands ###
