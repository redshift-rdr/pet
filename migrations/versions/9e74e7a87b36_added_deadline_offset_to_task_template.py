"""added deadline offset to task template

Revision ID: 9e74e7a87b36
Revises: bd6ae9f8499c
Create Date: 2022-10-16 11:10:33.469477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e74e7a87b36'
down_revision = 'bd6ae9f8499c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_template', sa.Column('offset', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_template', 'offset')
    # ### end Alembic commands ###
