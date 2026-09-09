"""Initial evidence-first tracker schema."""
from alembic import op
from app.db.base import Base
import app.models.core  # noqa
revision='0001_initial'; down_revision=None; branch_labels=None; depends_on=None
def upgrade(): Base.metadata.create_all(op.get_bind())
def downgrade(): Base.metadata.drop_all(op.get_bind())
