"""Initial migration

Revision ID: a6a5850286bf
Revises: 
Create Date: 2024-07-28 02:43:41.514772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6a5850286bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fcuser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('department', sa.String(length=120), nullable=False),
    sa.Column('student_id', sa.String(length=10), nullable=False),
    sa.Column('mbti', sa.String(length=4), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('userid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fcuser')
    # ### end Alembic commands ###
