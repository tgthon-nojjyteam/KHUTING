from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '074ace77ff68'
down_revision = '27b13be4f542'
branch_labels = None
depends_on = None

def upgrade():
    # Check if the column already exists before adding it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('fcuser')]
    if 'matching' not in columns:
        op.add_column('fcuser', sa.Column('matching', sa.Boolean(), nullable=True))
    if 'requested' not in columns:
        op.add_column('fcuser', sa.Column('requested', sa.Boolean(), nullable=True))

def downgrade():
    op.drop_column('fcuser', 'matching')
    op.drop_column('fcuser', 'requested')
