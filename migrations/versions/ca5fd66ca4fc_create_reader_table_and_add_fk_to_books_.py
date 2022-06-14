"""create reader table and add fk to books table

Revision ID: ca5fd66ca4fc
Revises: 55bbb9c311a8
Create Date: 2022-06-14 11:20:29.280796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca5fd66ca4fc'
down_revision = '55bbb9c311a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('readers',
    sa.Column('pk', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('pk')
    )
    op.add_column('books', sa.Column('reader_pk', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'books', 'readers', ['reader_pk'], ['pk'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'reader_pk')
    op.drop_table('readers')
    # ### end Alembic commands ###