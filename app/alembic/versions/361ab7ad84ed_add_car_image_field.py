"""add car_image field

Revision ID: 361ab7ad84ed
Revises: c1b22b15e85d
Create Date: 2021-02-20 21:19:08.840814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '361ab7ad84ed'
down_revision = 'c1b22b15e85d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('driver', sa.Column('car_image', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('driver', 'car_image')
    # ### end Alembic commands ###
