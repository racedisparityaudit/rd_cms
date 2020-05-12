"""empty message

Revision ID: f8f8b80de743
Revises: 719c68424583
Create Date: 2018-02-22 11:10:18.669722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f8f8b80de743"
down_revision = "719c68424583"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("page", sa.Column("internal_reference", sa.String(), nullable=True))

    op.execute(
        """
        UPDATE page SET internal_reference = guid WHERE page_type = 'measure';
    """
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("page", "internal_reference")
    # ### end Alembic commands ###
