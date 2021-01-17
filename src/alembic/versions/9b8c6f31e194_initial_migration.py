"""Initial migration

Revision ID: 9b8c6f31e194
Revises: 
Create Date: 2021-01-14 15:42:21.345314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b8c6f31e194'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "products",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_url', sa.String(200), nullable=False),
        sa.Column('product_id', sa.Integer, nullable=False),
        sa.Column('product_image_url', sa.String(200)),
        sa.Column('product_title', sa.String(200), nullable=False),
        sa.Column('product_category', sa.String(50)),
        sa.Column('product_price', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('product_description', sa.Text),
        sa.Column('name_and_address', sa.Text),
        sa.Column('return_address', sa.Text),
        sa.Column('net_contents', sa.String(100)),
        sa.Column('reviews', sa.JSON),
        sa.Column('ubnps', sa.JSON),
    )


def downgrade():
    op.drop_table("products")
