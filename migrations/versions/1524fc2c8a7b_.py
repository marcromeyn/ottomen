"""empty message

Revision ID: 1524fc2c8a7b
Revises: 1092164ea298
Create Date: 2015-09-06 13:44:21.245789

"""

# revision identifiers, used by Alembic.
revision = '1524fc2c8a7b'
down_revision = '1092164ea298'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_email'), 'accounts', ['email'], unique=True)
    op.add_column(u'answer', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column(u'answer', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.add_column(u'experiment', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column(u'experiment', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.add_column(u'label', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column(u'label', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.add_column(u'question', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column(u'question', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.add_column(u'session', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column(u'session', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.add_column(u'session', sa.Column('turk_id', sa.String(), nullable=True))
    op.drop_column(u'session', 'worker_id')
    op.add_column(u'task', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column(u'task', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.add_column(u'worker', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column(u'worker', sa.Column('modified_at', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'worker', 'modified_at')
    op.drop_column(u'worker', 'created_at')
    op.drop_column(u'task', 'modified_at')
    op.drop_column(u'task', 'created_at')
    op.add_column(u'session', sa.Column('worker_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column(u'session', 'turk_id')
    op.drop_column(u'session', 'modified_at')
    op.drop_column(u'session', 'created_at')
    op.drop_column(u'question', 'modified_at')
    op.drop_column(u'question', 'created_at')
    op.drop_column(u'label', 'modified_at')
    op.drop_column(u'label', 'created_at')
    op.drop_column(u'experiment', 'modified_at')
    op.drop_column(u'experiment', 'created_at')
    op.drop_column(u'answer', 'modified_at')
    op.drop_column(u'answer', 'created_at')
    op.drop_index(op.f('ix_accounts_email'), table_name='accounts')
    op.drop_table('accounts')
    ### end Alembic commands ###
