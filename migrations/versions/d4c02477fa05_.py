"""empty message

Revision ID: d4c02477fa05
Revises: 
Create Date: 2021-04-22 00:46:21.515462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4c02477fa05'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_rank')
    op.add_column('game', sa.Column('season', sa.String(length=20), nullable=True))
    op.alter_column('news', 'description',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('news', 'tag',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('news', 'tag',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
    op.alter_column('news', 'description',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.drop_column('game', 'season')
    op.create_table('team_rank',
    sa.Column('win', sa.VARCHAR(length=3), autoincrement=False, nullable=True),
    sa.Column('lose', sa.VARCHAR(length=3), autoincrement=False, nullable=True),
    sa.Column('average', sa.VARCHAR(length=7), autoincrement=False, nullable=True),
    sa.Column('team', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('game', sa.VARCHAR(length=3), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('team', name='team_rank_pkey')
    )
    # ### end Alembic commands ###