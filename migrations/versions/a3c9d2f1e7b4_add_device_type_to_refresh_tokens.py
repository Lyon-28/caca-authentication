"""add cascade delete on user fks and create email_change_requests table

Revision ID: cascade001
Revises: a3c9d2f1e7b4
Create Date: 2026-08-22

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'cascade001'
down_revision = 'a3c9d2f1e7b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- 1. Ubah FK jadi CASCADE / SET NULL ---
    op.drop_constraint("refresh_tokens_user_id_fkey", "refresh_tokens", type_="foreignkey")
    op.create_foreign_key("refresh_tokens_user_id_fkey", "refresh_tokens", "users", ["user_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("oauth_accounts_user_id_fkey", "oauth_accounts", type_="foreignkey")
    op.create_foreign_key("oauth_accounts_user_id_fkey", "oauth_accounts", "users", ["user_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("user_roles_user_id_fkey", "user_roles", type_="foreignkey")
    op.create_foreign_key("user_roles_user_id_fkey", "user_roles", "users", ["user_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("user_preferences_user_id_fkey", "user_preferences", type_="foreignkey")
    op.create_foreign_key("user_preferences_user_id_fkey", "user_preferences", "users", ["user_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("activity_logs_user_id_fkey", "activity_logs", type_="foreignkey")
    op.create_foreign_key("activity_logs_user_id_fkey", "activity_logs", "users", ["user_id"], ["id"], ondelete="SET NULL")

    op.drop_constraint("terms_acceptances_user_id_fkey", "terms_acceptances", type_="foreignkey")
    op.create_foreign_key("terms_acceptances_user_id_fkey", "terms_acceptances", "users", ["user_id"], ["id"], ondelete="CASCADE")

    # --- 2. Buat tabel email_change_requests yang belum pernah ada ---
    op.create_table(
        'email_change_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('old_email', sa.String(length=255), nullable=False),
        sa.Column('new_email', sa.String(length=255), nullable=False),
        sa.Column('old_email_token', sa.String(length=255), nullable=False, unique=True),
        sa.Column('new_email_token', sa.String(length=255), nullable=False, unique=True),
        sa.Column('old_email_confirmed', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('new_email_confirmed', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_email_change_requests_user_id', 'email_change_requests', ['user_id'])
    op.create_index('ix_email_change_requests_old_email_token', 'email_change_requests', ['old_email_token'])
    op.create_index('ix_email_change_requests_new_email_token', 'email_change_requests', ['new_email_token'])


def downgrade() -> None:
    op.drop_table('email_change_requests')

    op.drop_constraint("refresh_tokens_user_id_fkey", "refresh_tokens", type_="foreignkey")
    op.create_foreign_key("refresh_tokens_user_id_fkey", "refresh_tokens", "users", ["user_id"], ["id"])

    op.drop_constraint("oauth_accounts_user_id_fkey", "oauth_accounts", type_="foreignkey")
    op.create_foreign_key("oauth_accounts_user_id_fkey", "oauth_accounts", "users", ["user_id"], ["id"])

    op.drop_constraint("user_roles_user_id_fkey", "user_roles", type_="foreignkey")
    op.create_foreign_key("user_roles_user_id_fkey", "user_roles", "users", ["user_id"], ["id"])

    op.drop_constraint("user_preferences_user_id_fkey", "user_preferences", type_="foreignkey")
    op.create_foreign_key("user_preferences_user_id_fkey", "user_preferences", "users", ["user_id"], ["id"])

    op.drop_constraint("activity_logs_user_id_fkey", "activity_logs", type_="foreignkey")
    op.create_foreign_key("activity_logs_user_id_fkey", "activity_logs", "users", ["user_id"], ["id"])

    op.drop_constraint("terms_acceptances_user_id_fkey", "terms_acceptances", type_="foreignkey")
    op.create_foreign_key("terms_acceptances_user_id_fkey", "terms_acceptances", "users", ["user_id"], ["id"])
