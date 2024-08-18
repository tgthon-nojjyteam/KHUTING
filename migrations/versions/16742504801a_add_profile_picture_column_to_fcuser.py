from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '16742504801a'
down_revision = '074ace77ff68'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    # Check if 'profile_picture' column exists before adding it
    if not column_exists(conn, 'fcuser', 'profile_picture'):
        with op.batch_alter_table('fcuser', schema=None) as batch_op:
            batch_op.add_column(sa.Column('profile_picture', sa.String(length=50), nullable=True))

def downgrade():
    # 1. Add a temporary column with the new size
    with op.batch_alter_table('fcuser', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email_temp', sa.String(length=120), nullable=False))

    # 2. Copy data from the old column to the new column
    conn = op.get_bind()
    conn.execute("UPDATE fcuser SET email_temp = email")

    # 3. Drop the old column
    with op.batch_alter_table('fcuser', schema=None) as batch_op:
        batch_op.drop_column('email')

    # 4. Rename the new column to the original column name
    with op.batch_alter_table('fcuser', schema=None) as batch_op:
        batch_op.rename_column('email_temp', 'email')

    # 5. Drop the 'profile_picture' column
    with op.batch_alter_table('fcuser', schema=None) as batch_op:
        batch_op.drop_column('profile_picture')



def column_exists(connection, table_name, column_name):
    query = sa.text(f"SHOW COLUMNS FROM `{table_name}` LIKE :column_name")
    result = connection.execute(query, {'column_name': column_name})
    return result.fetchone() is not None

