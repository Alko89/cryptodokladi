"""add tokens

Revision ID: f8550fbad0ec
Revises: 5a04d5c2a0ce
Create Date: 2018-12-15 16:08:46.684667

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import table, column

from cryptodokladi.models import Token

# revision identifiers, used by Alembic.
revision = 'f8550fbad0ec'
down_revision = '5a04d5c2a0ce'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('token', sa.Column('name', mysql.TEXT(), nullable=False))

    btc = Token(name='Bitcoin' ,token='BTC')

    token = table('token',
        column('name', sa.String),
        column('token', sa.String),
    )

    op.bulk_insert(token,
        [
            {'name': 'Bitcoin', 'token':'BTC' },
            {'name': 'Ethereum', 'token':'ETH' },
            {'name': 'PIVX', 'token':'PIVX' },
            {'name': 'SportiFi', 'token':'SPF' },
            {'name': 'Monero', 'token':'XMR' },
            {'name': 'Dynamic Trading Rights', 'token':'DTR' },
        ]
    )


def downgrade():
    op.drop_column('token', 'name')

    op.execute("DELETE FROM token WHERE token IN ('BTC', 'ETH', 'PIVX', 'SPF', 'XMR', 'DTR')")
