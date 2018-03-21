"""empty message

Revision ID: 1b9f69ec2019
Revises: 001635503b12
Create Date: 2018-03-20 10:41:12.458635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b9f69ec2019'
down_revision = '001635503b12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('base_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('role_permission', sa.Column('base_permission_id', sa.Integer(), nullable=False))
    op.drop_constraint('role_permission_deployment_id_fkey', 'role_permission', type_='foreignkey')
    op.create_foreign_key(None, 'role_permission', 'base_permission', ['base_permission_id'], ['id'])
    op.drop_column('role_permission', 'description')
    op.drop_column('role_permission', 'deployment_id')
    op.drop_column('role_permission', 'perm_name')
    op.add_column('role_resource_permission', sa.Column('base_permission_id', sa.Integer(), nullable=False))
    op.drop_constraint('role_resource_permission_deployment_id_fkey', 'role_resource_permission', type_='foreignkey')
    op.create_foreign_key(None, 'role_resource_permission', 'base_permission', ['base_permission_id'], ['id'])
    op.drop_column('role_resource_permission', 'description')
    op.drop_column('role_resource_permission', 'deployment_id')
    op.drop_column('role_resource_permission', 'perm_name')
    op.add_column('user_permission', sa.Column('base_permission_id', sa.Integer(), nullable=False))
    op.drop_constraint('user_permission_deployment_id_fkey', 'user_permission', type_='foreignkey')
    op.create_foreign_key(None, 'user_permission', 'base_permission', ['base_permission_id'], ['id'])
    op.drop_column('user_permission', 'description')
    op.drop_column('user_permission', 'deployment_id')
    op.drop_column('user_permission', 'perm_name')
    op.add_column('user_resource_permission', sa.Column('base_permission_id', sa.Integer(), nullable=False))
    op.drop_constraint('user_resource_permission_deployment_id_fkey', 'user_resource_permission', type_='foreignkey')
    op.create_foreign_key(None, 'user_resource_permission', 'base_permission', ['base_permission_id'], ['id'])
    op.drop_column('user_resource_permission', 'description')
    op.drop_column('user_resource_permission', 'deployment_id')
    op.drop_column('user_resource_permission', 'perm_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_resource_permission', sa.Column('perm_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('user_resource_permission', sa.Column('deployment_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('user_resource_permission', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user_resource_permission', type_='foreignkey')
    op.create_foreign_key('user_resource_permission_deployment_id_fkey', 'user_resource_permission', 'deployment', ['deployment_id'], ['id'], ondelete='CASCADE')
    op.drop_column('user_resource_permission', 'base_permission_id')
    op.add_column('user_permission', sa.Column('perm_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('user_permission', sa.Column('deployment_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('user_permission', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user_permission', type_='foreignkey')
    op.create_foreign_key('user_permission_deployment_id_fkey', 'user_permission', 'deployment', ['deployment_id'], ['id'], ondelete='CASCADE')
    op.drop_column('user_permission', 'base_permission_id')
    op.add_column('role_resource_permission', sa.Column('perm_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('role_resource_permission', sa.Column('deployment_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('role_resource_permission', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'role_resource_permission', type_='foreignkey')
    op.create_foreign_key('role_resource_permission_deployment_id_fkey', 'role_resource_permission', 'deployment', ['deployment_id'], ['id'], ondelete='CASCADE')
    op.drop_column('role_resource_permission', 'base_permission_id')
    op.add_column('role_permission', sa.Column('perm_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('role_permission', sa.Column('deployment_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('role_permission', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'role_permission', type_='foreignkey')
    op.create_foreign_key('role_permission_deployment_id_fkey', 'role_permission', 'deployment', ['deployment_id'], ['id'], ondelete='CASCADE')
    op.drop_column('role_permission', 'base_permission_id')
    op.drop_table('base_permission')
    # ### end Alembic commands ###