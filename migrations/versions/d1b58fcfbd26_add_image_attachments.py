"""add image attachments

Revision ID: d1b58fcfbd26
Revises: 32263b7ab47e
Create Date: 2020-11-06 14:10:21.127050

"""
import depot
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd1b58fcfbd26'
down_revision = '32263b7ab47e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image_attachment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('photo', depot.fields.sqlalchemy.UploadedFileField(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image_attachment')
    # ### end Alembic commands ###
