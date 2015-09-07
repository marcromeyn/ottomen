"""empty message

Revision ID: 1092164ea298
Revises: 4bfdc4a415b5
Create Date: 2015-08-31 11:48:48.534435

"""

# revision identifiers, used by Alembic.
revision = '1092164ea298'
down_revision = '4bfdc4a415b5'

from alembic import op
import sqlalchemy as sa
import ottomen.algorithm.globals as globals


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'experiment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=True, default=False),
        sa.Column('accuracy', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'label',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'worker',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tw_pos', sa.Float(), nullable=True, default=globals.WORKER_TW_POS),
        sa.Column('tw_neg', sa.Float(), nullable=True, default=globals.WORKER_CLASS_NEG),
        sa.Column('class_pos', sa.Integer(), nullable=True, default=globals.WORKER_CLASS_POS),
        sa.Column('class_neg', sa.Integer(), nullable=True, default=globals.WORKER_CLASS_NEG),
        sa.Column('banned', sa.Boolean(), nullable=True, default=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'answer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('question_id', sa.Integer(), nullable=True),
        sa.Column('worker_id', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.ForeignKeyConstraint(['worker_id'], ['worker.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'experiment_question',
        sa.Column('experiment_id', sa.Integer(), nullable=True),
        sa.Column('question_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['experiment_id'], ['experiment.id'], ),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], )
    )

    op.create_table(
        'task',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('experiment_id', sa.Integer(), nullable=True),
        sa.Column('batch_size', sa.Integer(), nullable=True, default=globals.TASK_BATCH_SIZE),
        sa.Column('nr_of_batches', sa.Integer(), nullable=True, default=globals.TASK_NR_OF_BATCHES),
        sa.Column('size', sa.Integer(), nullable=True, default=globals.TASK_SIZE),
        sa.Column('initial_consensus', sa.Integer(), nullable=True, default=globals.TASK_INITIAL_CONSENSUS),
        sa.Column('returning_consensus', sa.Integer(), nullable=True, default=globals.TASK_RETURNING_CONSENSUS),
        sa.Column('minimum_mt_score', sa.Float(), nullable=True, default=globals.TASK_MINIMUM_MT_SCORE),
        sa.Column('minimum_mt_submissions', sa.Integer(), nullable=True, default=globals.TASK_MINIMUM_MT_SUBMISSIONS),
        sa.Column('reward', sa.Float(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['experiment_id'], ['experiment.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'validation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=True),
        sa.Column('experiment_id', sa.Integer(), nullable=True),
        sa.Column('label', sa.Boolean(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['experiment_id'], ['experiment.id'], ),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'answer_label',
        sa.Column('answer_id', sa.Integer(), nullable=True),
        sa.Column('label_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['answer_id'], ['answer.id'], ),
        sa.ForeignKeyConstraint(['label_id'], ['label.id'], )
    )

    op.create_table(
        'session',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('worker_id', sa.String(), nullable=True),
        sa.Column('task_id', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
        sa.ForeignKeyConstraint(['worker_id'], ['worker.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('validation_label',
        sa.Column('validation_id', sa.Integer(), nullable=True),
        sa.Column('label_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['label_id'], ['label.id'], ),
        sa.ForeignKeyConstraint(['validation_id'], ['validation.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('validation_label')
    op.drop_table('session')
    op.drop_table('answer_label')
    op.drop_table('validation')
    op.drop_table('task')
    op.drop_table('experiment_question')
    op.drop_table('answer')
    op.drop_table('worker')
    op.drop_table('label')
    op.drop_table('experiment')
    ### end Alembic commands ###