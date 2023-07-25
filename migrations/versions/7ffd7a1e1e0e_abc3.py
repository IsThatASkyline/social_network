"""abc3

Revision ID: 7ffd7a1e1e0e
Revises: b92e4d4778f5
Create Date: 2023-07-24 19:14:47.373654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ffd7a1e1e0e'
down_revision = 'b92e4d4778f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_dislikes_post_id_fkey', 'posts_dislikes', type_='foreignkey')
    op.create_foreign_key(None, 'posts_dislikes', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts_dislikes', type_='foreignkey')
    op.create_foreign_key('posts_dislikes_post_id_fkey', 'posts_dislikes', 'posts', ['post_id'], ['id'])
    # ### end Alembic commands ###
