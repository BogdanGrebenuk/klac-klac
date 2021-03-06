"""add whitelist table

Revision ID: b1d666d55f79
Revises: 71fa00181562
Create Date: 2021-02-21 00:41:21.425630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1d666d55f79'
down_revision = '71fa00181562'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('whitelist',
    sa.Column('driver_id', sa.Text(), nullable=False),
    sa.Column('passenger_id', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['driver_id'], ['driver.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['passenger_id'], ['passenger.id'], ondelete='CASCADE')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('whitelist')
    # ### end Alembic commands ###
