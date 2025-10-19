"""
Payment Provider Model

This module provides database access and business logic for payment providers.
"""

import json
from datetime import datetime
from db.init_db import get_db_connection


class PaymentProvider:
    """Model for managing payment provider data."""
    
    def __init__(self, id=None, provider_key=None, provider_name=None, 
                 config=None, enabled=False, created_at=None, updated_at=None):
        self.id = id
        self.provider_key = provider_key
        self.provider_name = provider_name
        self.config = config if isinstance(config, dict) else {}
        self.enabled = enabled
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self, include_secrets=False):
        """
        Convert model to dictionary.
        
        Args:
            include_secrets: If True, includes full config. If False, masks sensitive values.
            
        Returns:
            dict: Model data as dictionary
        """
        config_data = self.config.copy() if self.config else {}
        
        # Mask sensitive keys if not including secrets
        if not include_secrets and config_data:
            sensitive_keys = ['api_key', 'client_secret', 'api_token', 'secret_key', 
                            'private_key', 'webhook_secret']
            for key in sensitive_keys:
                if key in config_data and config_data[key]:
                    # Show only last 4 characters
                    value = str(config_data[key])
                    if len(value) > 4:
                        config_data[key] = '*' * (len(value) - 4) + value[-4:]
                    else:
                        config_data[key] = '****'
        
        return {
            'id': self.id,
            'provider_key': self.provider_key,
            'provider_name': self.provider_name,
            'config': config_data,
            'enabled': bool(self.enabled),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_db_row(row):
        """Create PaymentProvider instance from database row."""
        if not row:
            return None
        
        config = {}
        if row['config']:
            try:
                config = json.loads(row['config'])
            except json.JSONDecodeError:
                config = {}
        
        return PaymentProvider(
            id=row['id'],
            provider_key=row['provider_key'],
            provider_name=row['provider_name'],
            config=config,
            enabled=bool(row['enabled']),
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    @staticmethod
    def get_all(db_path=None):
        """Get all payment providers."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payment_providers ORDER BY id')
        rows = cursor.fetchall()
        conn.close()
        
        return [PaymentProvider.from_db_row(row) for row in rows]
    
    @staticmethod
    def get_by_id(provider_id, db_path=None):
        """Get payment provider by ID."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payment_providers WHERE id = ?', (provider_id,))
        row = cursor.fetchone()
        conn.close()
        
        return PaymentProvider.from_db_row(row)
    
    @staticmethod
    def get_by_key(provider_key, db_path=None):
        """Get payment provider by provider key."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payment_providers WHERE provider_key = ?', (provider_key,))
        row = cursor.fetchone()
        conn.close()
        
        return PaymentProvider.from_db_row(row)
    
    @staticmethod
    def get_enabled(db_path=None):
        """Get all enabled payment providers."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payment_providers WHERE enabled = 1 ORDER BY id')
        rows = cursor.fetchall()
        conn.close()
        
        return [PaymentProvider.from_db_row(row) for row in rows]
    
    def save(self, db_path=None):
        """Save or update payment provider."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        config_json = json.dumps(self.config) if self.config else '{}'
        
        if self.id:
            # Update existing
            cursor.execute('''
                UPDATE payment_providers 
                SET provider_key = ?, provider_name = ?, config = ?, 
                    enabled = ?, updated_at = ?
                WHERE id = ?
            ''', (self.provider_key, self.provider_name, config_json, 
                  int(self.enabled), now, self.id))
            self.updated_at = now
        else:
            # Insert new
            cursor.execute('''
                INSERT INTO payment_providers (provider_key, provider_name, config, 
                                              enabled, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.provider_key, self.provider_name, config_json, 
                  int(self.enabled), now, now))
            self.id = cursor.lastrowid
            self.created_at = now
            self.updated_at = now
        
        conn.commit()
        conn.close()
        return self
    
    def delete(self, db_path=None):
        """Delete payment provider."""
        if not self.id:
            return False
        
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM payment_providers WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()
        return True
