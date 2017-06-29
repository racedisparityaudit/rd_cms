"""empty message

Revision ID: fd5178b68fe6
Revises: 334faaf60a3d
Create Date: 2017-06-26 14:44:18.464089

"""
import hashlib
import time

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from slugify import slugify
from sqlalchemy.orm import Session
from application.cms.models import DbPage, DbDimension

revision = 'fd5178b68fe6'
down_revision = '334faaf60a3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_dimension', sa.Column('chart', sa.Text(), nullable=True))
    op.add_column('db_dimension', sa.Column('table', sa.Text(), nullable=True))
    # ### end Alembic commands ###

    ### DATA MIGRATION
    session = Session(bind=op.get_bind())
    for page in DbPage.query.all():
        print(page.title)
        dimensions = page.page_dict().get('dimensions', [])

        for dimension in dimensions:
            hash = hashlib.sha1()
            hash.update("{}{}".format(str(time.time()), slugify(dimension['title'])).encode('utf-8'))
            guid = hash.hexdigest()[:10]

            db_dimension = DbDimension(guid=guid,
                                       measure=page.guid,
                                       title=dimension['title'],
                                       time_period=dimension['time_period'],
                                       summary=dimension['summary'],
                                       suppression_rules=dimension['suppression_rules'],
                                       disclosure_control=dimension['disclosure_control'],
                                       type_of_statistic=dimension['type_of_statistic'],
                                       location=dimension['location'],
                                       source=dimension['source'])
            if dimension.get('chart'):
                db_dimension.chart = dimension['chart']
            if dimension.get('chart_source_data'):
                db_dimension.chart_source_data = dimension['chart_source_data']
            if dimension.get('table'):
                db_dimension.table = dimension['table']
            if dimension.get('table_source_data'):
                db_dimension.table_source_data = dimension['table_source_data']

            session.add(db_dimension)
        session.commit()





def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('db_dimension', 'table')
    op.drop_column('db_dimension', 'chart')
    # ### end Alembic commands ###
