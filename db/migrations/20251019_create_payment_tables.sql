-- Migration: Create payment provider and webhook settings tables
-- Created: 2025-10-19
-- Description: This migration creates tables to store payment provider configurations
--              and webhook settings for multi-provider payment support

-- ============================================================================
-- Table: payment_providers
-- Description: Stores configuration for different payment providers
-- ============================================================================
CREATE TABLE IF NOT EXISTS payment_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_key TEXT NOT NULL UNIQUE,  -- e.g., 'stripe', 'paypal', 'wise', 'crypto'
    provider_name TEXT NOT NULL,        -- Display name
    config TEXT,                         -- JSON configuration (API keys, settings)
    enabled INTEGER DEFAULT 0,           -- 0 = disabled, 1 = enabled
    created_at TEXT NOT NULL,            -- ISO 8601 timestamp
    updated_at TEXT NOT NULL             -- ISO 8601 timestamp
);

-- Index for faster lookups by provider_key
CREATE INDEX IF NOT EXISTS idx_provider_key ON payment_providers(provider_key);

-- Index for enabled providers
CREATE INDEX IF NOT EXISTS idx_provider_enabled ON payment_providers(enabled);

-- ============================================================================
-- Table: webhook_settings
-- Description: Stores webhook configuration for each payment provider
-- ============================================================================
CREATE TABLE IF NOT EXISTS webhook_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id INTEGER NOT NULL,        -- Foreign key to payment_providers
    webhook_url TEXT,                    -- URL to receive webhooks
    webhook_secret TEXT,                 -- Secret for webhook signature verification
    enabled INTEGER DEFAULT 0,           -- 0 = disabled, 1 = enabled
    created_at TEXT NOT NULL,            -- ISO 8601 timestamp
    updated_at TEXT NOT NULL,            -- ISO 8601 timestamp
    FOREIGN KEY (provider_id) REFERENCES payment_providers(id) ON DELETE CASCADE
);

-- Index for faster lookups by provider_id
CREATE INDEX IF NOT EXISTS idx_webhook_provider ON webhook_settings(provider_id);

-- Index for enabled webhooks
CREATE INDEX IF NOT EXISTS idx_webhook_enabled ON webhook_settings(enabled);

-- ============================================================================
-- Sample seed data (for testing/development)
-- ============================================================================
-- Note: These are example entries with placeholder configurations
-- In production, configure these through the admin UI

-- Stripe provider (disabled by default)
INSERT OR IGNORE INTO payment_providers (id, provider_key, provider_name, config, enabled, created_at, updated_at)
VALUES (
    1,
    'stripe',
    'Stripe',
    '{"api_key": "", "test_mode": true}',
    0,
    datetime('now'),
    datetime('now')
);

-- PayPal provider (disabled by default)
INSERT OR IGNORE INTO payment_providers (id, provider_key, provider_name, config, enabled, created_at, updated_at)
VALUES (
    2,
    'paypal',
    'PayPal',
    '{"client_id": "", "client_secret": "", "test_mode": true}',
    0,
    datetime('now'),
    datetime('now')
);

-- Wise provider (disabled by default)
INSERT OR IGNORE INTO payment_providers (id, provider_key, provider_name, config, enabled, created_at, updated_at)
VALUES (
    3,
    'wise',
    'Wise',
    '{"api_token": "", "test_mode": true}',
    0,
    datetime('now'),
    datetime('now')
);

-- Crypto provider (disabled by default)
INSERT OR IGNORE INTO payment_providers (id, provider_key, provider_name, config, enabled, created_at, updated_at)
VALUES (
    4,
    'crypto',
    'Cryptocurrency',
    '{"btc_address": "", "eth_address": "", "test_mode": true}',
    0,
    datetime('now'),
    datetime('now')
);
