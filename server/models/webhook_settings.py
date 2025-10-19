"""
Webhook Settings Model

This module provides database access and business logic for webhook settings.
"""

import json
import secrets
from datetime import datetime
from db.init_db import get_db_connection


class WebhookSettings:
    """Model for managing webhook settings data."""
    
    def __init__(self, id=None, provider_id=None, webhook_url=None, 
                 webhook_secret=None, enabled=False, created_at=None, updated_at=None):
        self.id = id
        self.provider_id = provider_id
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret
        self.enabled = enabled
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self, include_secrets=False):
        """
        Convert model to dictionary.
        
        Args:
            include_secrets: If True, includes full webhook secret. If False, masks it.
            
        Returns:
            dict: Model data as dictionary
        """
        webhook_secret = self.webhook_secret
        
        # Mask webhook secret if not including secrets
        if not include_secrets and webhook_secret:
            value = str(webhook_secret)
            if len(value) > 8:
                webhook_secret = value[:4] + '*' * (len(value) - 8) + value[-4:]
            else:
                webhook_secret = '****'
        
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'webhook_url': self.webhook_url,
            'webhook_secret': webhook_secret,
            'enabled': bool(self.enabled),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_db_row(row):
        """Create WebhookSettings instance from database row."""
        if not row:
            return None
        
        return WebhookSettings(
            id=row['id'],
            provider_id=row['provider_id'],
            webhook_url=row['webhook_url'],
            webhook_secret=row['webhook_secret'],
            enabled=bool(row['enabled']),
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    @staticmethod
    def generate_secret():
        """Generate a secure webhook secret."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def get_all(db_path=None):
        """Get all webhook settings."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM webhook_settings ORDER BY id')
        rows = cursor.fetchall()
        conn.close()
        
        return [WebhookSettings.from_db_row(row) for row in rows]
    
    @staticmethod
    def get_by_id(webhook_id, db_path=None):
        """Get webhook settings by ID."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM webhook_settings WHERE id = ?', (webhook_id,))
        row = cursor.fetchone()
        conn.close()
        
        return WebhookSettings.from_db_row(row)
    
    @staticmethod
    def get_by_provider(provider_id, db_path=None):
        """Get all webhook settings for a provider."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM webhook_settings WHERE provider_id = ? ORDER BY id', 
                      (provider_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [WebhookSettings.from_db_row(row) for row in rows]
    
    def save(self, db_path=None):
        """Save or update webhook settings."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        if self.id:
            # Update existing
            cursor.execute('''
                UPDATE webhook_settings 
                SET provider_id = ?, webhook_url = ?, webhook_secret = ?, 
                    enabled = ?, updated_at = ?
                WHERE id = ?
            ''', (self.provider_id, self.webhook_url, self.webhook_secret, 
                  int(self.enabled), now, self.id))
            self.updated_at = now
        else:
            # Insert new
            cursor.execute('''
                INSERT INTO webhook_settings (provider_id, webhook_url, webhook_secret, 
                                             enabled, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.provider_id, self.webhook_url, self.webhook_secret, 
                  int(self.enabled), now, now))
            self.id = cursor.lastrowid
            self.created_at = now
            self.updated_at = now
        
        conn.commit()
        conn.close()
        return self
    
    def delete(self, db_path=None):
        """Delete webhook settings."""
        if not self.id:
            return False
        
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM webhook_settings WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()
        return True
