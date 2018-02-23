"""empty message

Revision ID: e26c6226843e
Revises: 8bb7c36e3089
Create Date: 2018-02-23 16:25:24.028616

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e26c6226843e'
down_revision = '8bb7c36e3089'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('phone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant_phone',
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('phone_id', sa.Integer(), nullable=False),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['phone_id'], ['phone.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('participant_id', 'phone_id')
    )
    op.drop_column('participant', 'phones')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant', sa.Column('phones', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_table('participant_phone')
    op.drop_table('phone')
    # ### end Alembic commands ###
