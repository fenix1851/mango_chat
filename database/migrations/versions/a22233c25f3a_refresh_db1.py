"""refresh db1

Revision ID: a22233c25f3a
Revises: 3527f96c7326
Create Date: 2023-02-01 00:17:21.255611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a22233c25f3a'
down_revision = '3527f96c7326'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'refresh_token')
    op.drop_column('user', 'description')
    op.drop_column('user', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('refresh_token', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
