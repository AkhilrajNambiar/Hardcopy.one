"""empty message

Revision ID: 6cf75eef979a
Revises: 
Create Date: 2021-07-22 13:43:41.045502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cf75eef979a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('profile_pic', sa.String(length=60), nullable=False),
    sa.Column('address', sa.Text(), nullable=False),
    sa.Column('contactnumber', sa.Text(), nullable=False),
    sa.Column('total_donations', sa.Integer(), nullable=True),
    sa.Column('pickup', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('pickup'),
    sa.UniqueConstraint('username')
    )
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_name', sa.String(length=60), nullable=False),
    sa.Column('author_name', sa.String(length=60), nullable=False),
    sa.Column('genre', sa.String(length=60), nullable=False),
    sa.Column('sub_genre', sa.String(length=60), nullable=True),
    sa.Column('book_front', sa.String(length=60), nullable=False),
    sa.Column('book_back', sa.String(length=60), nullable=False),
    sa.Column('book_top', sa.String(length=60), nullable=False),
    sa.Column('book_bottom', sa.String(length=60), nullable=False),
    sa.Column('book_right', sa.String(length=60), nullable=False),
    sa.Column('book_left', sa.String(length=60), nullable=False),
    sa.Column('length', sa.Integer(), nullable=False),
    sa.Column('breadth', sa.Integer(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('extras', sa.Text(), nullable=True),
    sa.Column('ordered_by', sa.Integer(), nullable=True),
    sa.Column('donated_by', sa.Integer(), nullable=False),
    sa.Column('votes_for_content', sa.Float(), nullable=True),
    sa.Column('total_content_rating', sa.Float(), nullable=True),
    sa.Column('votes_for_condition', sa.Float(), nullable=True),
    sa.Column('total_condition_rating', sa.Float(), nullable=True),
    sa.Column('content_rating', sa.Float(), nullable=True),
    sa.Column('condition_rating', sa.Float(), nullable=True),
    sa.Column('shipment_id', sa.String(length=10), nullable=True),
    sa.Column('shipment_status', sa.String(length=60), nullable=True),
    sa.Column('order_id', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['donated_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['ordered_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pending_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_name', sa.String(length=60), nullable=False),
    sa.Column('author_name', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('star_values',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('five_star_content', sa.Integer(), nullable=True),
    sa.Column('four_star_content', sa.Integer(), nullable=True),
    sa.Column('three_star_content', sa.Integer(), nullable=True),
    sa.Column('two_star_content', sa.Integer(), nullable=True),
    sa.Column('one_star_content', sa.Integer(), nullable=True),
    sa.Column('five_star_condition', sa.Integer(), nullable=True),
    sa.Column('four_star_condition', sa.Integer(), nullable=True),
    sa.Column('three_star_condition', sa.Integer(), nullable=True),
    sa.Column('two_star_condition', sa.Integer(), nullable=True),
    sa.Column('one_star_condition', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('donor_id', sa.Integer(), nullable=False),
    sa.Column('rater_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['donor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['rater_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('star_values')
    op.drop_table('cart')
    op.drop_table('pending_requests')
    op.drop_table('book')
    op.drop_table('user')
    # ### end Alembic commands ###
