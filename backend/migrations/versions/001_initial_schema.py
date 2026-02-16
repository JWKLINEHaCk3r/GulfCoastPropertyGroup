"""Initial database migration - Create all tables

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-02-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types
    sa.Enum('new', 'qualified', 'contacted', 'negotiating', 'under_contract', 'closed', 'rejected', 'expired', name='leadstatusenum').create(op.get_bind(), checkfirst=True)
    sa.Enum('single_family', 'multi_family', 'commercial', 'vacant', 'mobile_home', 'other', name='propertytypeenum').create(op.get_bind(), checkfirst=True)
    sa.Enum('pending', 'accepted', 'rejected', 'negotiating', 'signed', 'closed', name='offerstatusenum').create(op.get_bind(), checkfirst=True)
    sa.Enum('open', 'active', 'under_contract', 'closed', 'failed', name='dealstatusenum').create(op.get_bind(), checkfirst=True)
    
    # Create tables
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('subscription_tier', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    op.create_table('leads',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=2), nullable=False),
        sa.Column('zip_code', sa.String(length=10), nullable=False),
        sa.Column('county', sa.String(length=100), nullable=True),
        sa.Column('property_type', sa.String(length=50), nullable=False),
        sa.Column('square_feet', sa.Integer(), nullable=True),
        sa.Column('bedrooms', sa.Integer(), nullable=True),
        sa.Column('bathrooms', sa.Float(), nullable=True),
        sa.Column('year_built', sa.Integer(), nullable=True),
        sa.Column('estimated_after_repair_value', sa.Float(), nullable=True),
        sa.Column('market_value', sa.Float(), nullable=True),
        sa.Column('tax_assessed_value', sa.Float(), nullable=True),
        sa.Column('estimated_repair_cost', sa.Float(), nullable=True),
        sa.Column('estimated_holding_cost', sa.Float(), nullable=True),
        sa.Column('seller_phone', sa.String(length=20), nullable=True),
        sa.Column('seller_email', sa.String(length=255), nullable=True),
        sa.Column('seller_name', sa.String(length=255), nullable=True),
        sa.Column('seller_motivated', sa.Boolean(), nullable=False),
        sa.Column('lead_score', sa.Float(), nullable=False),
        sa.Column('lead_status', sa.String(length=50), nullable=False),
        sa.Column('data_source', sa.String(length=100), nullable=True),
        sa.Column('mls_id', sa.String(length=50), nullable=True),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_contacted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('mls_id'),
        sa.UniqueConstraint('external_id')
    )
    
    op.create_table('offers',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('lead_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('offer_price', sa.Float(), nullable=False),
        sa.Column('after_repair_value', sa.Float(), nullable=False),
        sa.Column('estimated_repair_cost', sa.Float(), nullable=False),
        sa.Column('profit_potential', sa.Float(), nullable=False),
        sa.Column('valuation_method', sa.String(length=50), nullable=True),
        sa.Column('offer_status', sa.String(length=50), nullable=False),
        sa.Column('seller_response', sa.String(length=255), nullable=True),
        sa.Column('negotiation_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('deals',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('lead_id', sa.String(length=36), nullable=True),
        sa.Column('offer_id', sa.String(length=36), nullable=True),
        sa.Column('buyer_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('purchase_price', sa.Float(), nullable=False),
        sa.Column('arv', sa.Float(), nullable=False),
        sa.Column('expected_profit', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['buyer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
        sa.ForeignKeyConstraint(['offer_id'], ['offers.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('tier', sa.String(length=50), nullable=False),
        sa.Column('stripe_subscription_id', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('current_period_start', sa.DateTime(), nullable=False),
        sa.Column('current_period_end', sa.DateTime(), nullable=False),
        sa.Column('cancelled_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('subscription_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('stripe_payment_intent_id', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscriptions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('commissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('deal_id', sa.String(length=36), nullable=True),
        sa.Column('commission_type', sa.String(length=50), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['deal_id'], ['deals.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for performance
    op.create_index('idx_lead_status', 'leads', ['lead_status'])
    op.create_index('idx_lead_score', 'leads', ['lead_score'])
    op.create_index('idx_lead_created', 'leads', ['created_at'])
    op.create_index('idx_offer_status', 'offers', ['offer_status'])
    op.create_index('idx_deal_status', 'deals', ['status'])
    op.create_index('idx_user_email', 'users', ['email'])


def downgrade() -> None:
    # Drop tables
    op.drop_index('idx_user_email', table_name='users')
    op.drop_index('idx_deal_status', table_name='deals')
    op.drop_index('idx_offer_status', table_name='offers')
    op.drop_index('idx_lead_created', table_name='leads')
    op.drop_index('idx_lead_score', table_name='leads')
    op.drop_index('idx_lead_status', table_name='leads')
    
    op.drop_table('commissions')
    op.drop_table('payments')
    op.drop_table('subscriptions')
    op.drop_table('deals')
    op.drop_table('offers')
    op.drop_table('leads')
    op.drop_table('users')
    
    # Drop enum types
    sa.Enum('new', 'qualified', 'contacted', 'negotiating', 'under_contract', 'closed', 'rejected', 'expired', name='leadstatusenum').drop(op.get_bind(), checkfirst=True)
    sa.Enum('single_family', 'multi_family', 'commercial', 'vacant', 'mobile_home', 'other', name='propertytypeenum').drop(op.get_bind(), checkfirst=True)
    sa.Enum('pending', 'accepted', 'rejected', 'negotiating', 'signed', 'closed', name='offerstatusenum').drop(op.get_bind(), checkfirst=True)
    sa.Enum('open', 'active', 'under_contract', 'closed', 'failed', name='dealstatusenum').drop(op.get_bind(), checkfirst=True)
