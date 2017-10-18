"""empty message

Revision ID: 1be0f1ffc951
Revises: 86182b75d7b3
Create Date: 2017-10-16 10:23:59.607691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1be0f1ffc951'
down_revision = '86182b75d7b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_page', sa.Column('created_by', sa.String(length=255), nullable=True))
    op.add_column('db_page', sa.Column('last_updated_by', sa.String(length=255), nullable=True))
    op.add_column('db_page', sa.Column('published_by', sa.String(length=255), nullable=True))
    op.add_column('db_page', sa.Column('unpublished_by', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('db_page', 'unpublished_by')
    op.drop_column('db_page', 'published_by')
    op.drop_column('db_page', 'last_updated_by')
    op.drop_column('db_page', 'created_by')
    # ### end Alembic commands ###
