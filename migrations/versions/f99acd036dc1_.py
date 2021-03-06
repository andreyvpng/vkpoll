"""empty message

Revision ID: f99acd036dc1
Revises: 41485b039997
Create Date: 2018-03-16 17:22:22.266349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f99acd036dc1'
down_revision = '41485b039997'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('choice_of_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('choice_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['choice_id'], ['choice.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('choice_of_user')
    # ### end Alembic commands ###
