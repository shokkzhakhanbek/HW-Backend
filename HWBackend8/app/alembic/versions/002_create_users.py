from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"  


def upgrade():
    op.create_table(
        "flowers",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String),
        sa.Column("count", sa.Integer),
        sa.Column("cost", sa.Float),
    )


def downgrade():
    op.drop_table("flowers")