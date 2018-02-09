"""empty message

Revision ID: 7ae8ac17bb1a
Revises: f1b61a0b383b
Create Date: 2018-02-09 15:46:22.308594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ae8ac17bb1a'
down_revision = 'f1b61a0b383b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'name')
    # ### end Alembic commands ###