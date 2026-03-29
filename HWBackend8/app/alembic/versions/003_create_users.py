from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"  


def upgrade():
    op.create_table(
        "purchases",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("flower_id", sa.Integer, sa.ForeignKey("flowers.id")),
    )


def downgrade():
    op.drop_table("purchases")