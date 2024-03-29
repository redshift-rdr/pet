"""bang

Revision ID: a3100c0b0cf0
Revises: 
Create Date: 2022-10-02 20:14:53.419816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3100c0b0cf0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('engagement',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('client', sa.String(length=36), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('start', sa.Date(), nullable=True),
    sa.Column('end', sa.Date(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('category', sa.String(length=36), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_engagement_title'), 'engagement', ['title'], unique=False)
    op.create_table('engagement_template',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('client', sa.String(length=36), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('engagement_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['engagement_id'], ['engagement.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_engagement_template_title'), 'engagement_template', ['title'], unique=True)
    op.create_table('tasklist',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('engagement_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['engagement_id'], ['engagement.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_tasklist_title'), 'tasklist', ['title'], unique=False)
    op.create_table('task',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('tasklist_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['tasklist_id'], ['tasklist.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_task_title'), 'task', ['title'], unique=False)
    op.create_table('tasklist_template',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('engagementtemplate_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['engagementtemplate_id'], ['engagement_template.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_tasklist_template_title'), 'tasklist_template', ['title'], unique=True)
    op.create_table('task_template',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('tasklisttemplate_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['tasklisttemplate_id'], ['tasklist_template.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_task_template_title'), 'task_template', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_template_title'), table_name='task_template')
    op.drop_table('task_template')
    op.drop_index(op.f('ix_tasklist_template_title'), table_name='tasklist_template')
    op.drop_table('tasklist_template')
    op.drop_index(op.f('ix_task_title'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_tasklist_title'), table_name='tasklist')
    op.drop_table('tasklist')
    op.drop_index(op.f('ix_engagement_template_title'), table_name='engagement_template')
    op.drop_table('engagement_template')
    op.drop_index(op.f('ix_engagement_title'), table_name='engagement')
    op.drop_table('engagement')
    # ### end Alembic commands ###
