"""migrate1

Revision ID: d315a6bcb908
Revises: e655888bb43f
Create Date: 2022-02-24 19:45:09.553216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd315a6bcb908'
down_revision = 'e655888bb43f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('goal1_id', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'goal1_id')
    # ### end Alembic commands ###