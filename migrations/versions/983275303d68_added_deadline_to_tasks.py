"""added deadline to tasks

Revision ID: 983275303d68
Revises: a3100c0b0cf0
Create Date: 2022-10-08 09:48:37.117445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '983275303d68'
down_revision = 'a3100c0b0cf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('deadline', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'deadline')
    # ### end Alembic commands ###
