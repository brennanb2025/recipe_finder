"""initial migration

Revision ID: e30103521104
Revises: 
Create Date: 2022-03-29 00:08:20.137794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e30103521104'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Chef',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_Chef'))
    )
    op.create_table('Ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('num_use', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_Ingredient'))
    )
    op.create_table('Tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('num_use', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_Tag'))
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_User'))
    )
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_User_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_User_timestamp'), ['timestamp'], unique=False)

    op.create_table('Recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=8192), nullable=True),
    sa.Column('num_votes', sa.Integer(), nullable=True),
    sa.Column('creator', sa.Integer(), nullable=True),
    sa.Column('num_ingredients', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator'], ['Chef.id'], name=op.f('fk_Recipe_creator_Chef')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_Recipe'))
    )
    op.create_table('Vote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('voteType', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], name=op.f('fk_Vote_user_id_User')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_Vote'))
    )
    op.create_table('RecipeIngredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('ingredient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['Ingredient.id'], name=op.f('fk_RecipeIngredient_ingredient_id_Ingredient')),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], name=op.f('fk_RecipeIngredient_recipe_id_Recipe')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_RecipeIngredient'))
    )
    op.create_table('RecipeTag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], name=op.f('fk_RecipeTag_recipe_id_Recipe')),
    sa.ForeignKeyConstraint(['tag_id'], ['Tag.id'], name=op.f('fk_RecipeTag_tag_id_Tag')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_RecipeTag'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('RecipeTag')
    op.drop_table('RecipeIngredient')
    op.drop_table('Vote')
    op.drop_table('Recipe')
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_User_timestamp'))
        batch_op.drop_index(batch_op.f('ix_User_email'))

    op.drop_table('User')
    op.drop_table('Tag')
    op.drop_table('Ingredient')
    op.drop_table('Chef')
    # ### end Alembic commands ###