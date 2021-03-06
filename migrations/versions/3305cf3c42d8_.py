"""empty message

Revision ID: 3305cf3c42d8
Revises: 41efae71b0d5
Create Date: 2015-09-17 18:49:51.040529

"""

# revision identifiers, used by Alembic.
revision = '3305cf3c42d8'
down_revision = '41efae71b0d5'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('experiment', 'accuracy',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('experiment', 'accuracy',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    ### end Alembic commands ###
