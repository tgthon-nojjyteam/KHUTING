"""Rename userid to username

Revision ID: 27b13be4f542
Revises: f287111cfeec
Create Date: 2024-08-15 12:26:06.575896

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '27b13be4f542'
down_revision = 'f287111cfeec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('new_table')
    with op.batch_alter_table('fcuser', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=80), nullable=False))
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=120),
               nullable=False)
        batch_op.alter_column('email_verified',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=80),
               nullable=False)
        batch_op.drop_index('userid')
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.drop_column('userid')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fcuser', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userid', mysql.VARCHAR(length=80), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('userid', ['userid'], unique=True)
        batch_op.alter_column('email_verified',
               existing_type=sa.String(length=80),
               type_=mysql.VARCHAR(length=45),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=45),
               nullable=True)
        batch_op.drop_column('username')

    op.create_table('new_table',
    sa.Column('idnew_table', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('idnew_table'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
