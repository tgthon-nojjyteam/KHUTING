"""Remove name field from Team model

Revision ID: 04e525f487f9
Revises: b8e77db6a95c
Create Date: 2024-08-21 17:30:46.169800

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '04e525f487f9'
down_revision = 'b8e77db6a95c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=80), nullable=False))

    # ### end Alembic commands ###
