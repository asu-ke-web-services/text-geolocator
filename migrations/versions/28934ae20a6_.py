"""empty message

Revision ID: 28934ae20a6
Revises: None
Create Date: 2014-11-25 07:16:07.554441

"""

# revision identifiers, used by Alembic.
revision = '28934ae20a6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('featureclass', sa.String(length=80), nullable=False),
    sa.Column('featurecode', sa.String(length=80), nullable=False),
    sa.Column('code', sa.String(length=80), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('geonameid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('countrycode', sa.String(length=80), nullable=False),
    sa.Column('featureclass', sa.String(length=80), nullable=False),
    sa.Column('featurecode', sa.String(length=80), nullable=False),
    sa.Column('featuretype', sa.String(length=80), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('initial_weight', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('spatial_ref_sys')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('srid', name=u'spatial_ref_sys_pkey')
    )
    # pretty sure that these were a mistake. the workflow should be upgrade then import data
    #op.drop_table('location')
    #op.drop_table('feature')
    ### end Alembic commands ###
