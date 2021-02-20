"""add blacklist table

Revision ID: c1b22b15e85d
Revises: aecb7668239b
Create Date: 2021-02-20 19:37:11.832330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1b22b15e85d'
down_revision = 'aecb7668239b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist',
    sa.Column('ban_driver_id', sa.Text(), nullable=False),
    sa.Column('passenger_id', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['ban_driver_id'], ['driver.id'], ),
    sa.ForeignKeyConstraint(['passenger_id'], ['passenger.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist')
    # ### end Alembic commands ###