from alembic import op
import sqlalchemy as sa

revision = "0001_create_courses"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "courses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
    )

def downgrade() -> None:
    op.drop_table("courses")
