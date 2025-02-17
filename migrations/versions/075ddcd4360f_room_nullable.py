"""room nullable

Revision ID: 075ddcd4360f
Revises: 169780d77807
Create Date: 2024-08-25 19:50:16.742382

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '075ddcd4360f'
down_revision = '169780d77807'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_message', schema=None) as batch_op:
        batch_op.alter_column('room',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_message', schema=None) as batch_op:
        batch_op.alter_column('room',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###
