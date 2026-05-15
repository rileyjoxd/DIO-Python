import sqlalchemy as sa
from APIcode import metadata

posts = sa.Table('posts',metadata,
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('title', sa.String(150), nullable=False, unique=True),
                 sa.Column('content', sa.String, nullable=False),
                 sa.Column('published_at', sa.DateTime, nullable=True),
                 sa.Column('publised', sa.Boolean, default=False),
                 )
