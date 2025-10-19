"""
License client for UVDM application.
Handles license verification with the homeserver.
"""

import requests
import json
import os
import platform
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class LicenseClient:
    """Client for verifying licenses with the UVDM homeserver."""
    
    def __init__(self, server_url: Optional[str] = None, cache_file: Optional[str] = None):
        """
        Initialize the license client.
        
        Args:
            server_url: URL of the license server (default: from env or localhost)
            cache_file: Path to cache file for offline validation
        """
        self.server_url = server_url or os.environ.get(
            'UVDM_LICENSE_SERVER', 
            'http://localhost:5000'
        )
        self.cache_file = cache_file or os.path.join('data', 'license_cache.json')
        self.machine_id = self._get_machine_id()
        self.timeout = 10  # seconds
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
    
    def _get_machine_id(self) -> str:
        """
        Generate a unique machine identifier.
        
        Returns:
            Machine ID string
        """
        # Combine multiple system identifiers for uniqueness
        system = platform.system()
        node = platform.node()
        machine = platform.machine()
        processor = platform.processor()
        
        # Create a hash of system information
        machine_info = f"{system}-{node}-{machine}-{processor}"
        machine_id = hashlib.sha256(machine_info.encode()).hexdigest()
        
        return machine_id
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load cached license information."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_cache(self, data: Dict[str, Any]) -> None:
        """Save license information to cache."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Failed to save license cache: {e}")
    
    def verify_license(self, license_key: str, offline_mode: bool = False) -> Dict[str, Any]:
        """
        Verify a license key with the server.
        
        Args:
            license_key: The license key to verify
            offline_mode: If True, only check cached data
            
        Returns:
            Dictionary with verification result
        """
        # Try online verification first
        if not offline_mode:
            try:
                response = requests.post(
                    f"{self.server_url}/api/license/verify",
                    json={
                        'license_key': license_key,
                        'machine_id': self.machine_id
                    },
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    result['verified_at'] = datetime.now().isoformat()
                    result['license_key'] = license_key
                    
                    # Cache the result
                    self._save_cache(result)
                    
                    return result
                else:
                    # Server returned error
                    error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                    return {
                        'valid': False,
                        'error': error_data.get('error', f'Server error: {response.status_code}'),
                        'offline': False
                    }
                    
            except requests.exceptions.RequestException as e:
                # Network error, fall back to cache
                print(f"License verification failed: {e}")
                offline_mode = True
        
        # Offline mode or fallback to cache
        if offline_mode:
            cache = self._load_cache()
            
            if cache.get('license_key') == license_key:
                # Check if cached data is recent (within 7 days)
                try:
                    verified_at = datetime.fromisoformat(cache.get('verified_at', ''))
                    age_days = (datetime.now() - verified_at).days
                    
                    if age_days <= 7:
                        cache['offline'] = True
                        cache['cache_age_days'] = age_days
                        return cache
                except (ValueError, TypeError):
                    pass
            
            return {
                'valid': False,
                'error': 'No valid cached license found',
                'offline': True
            }
    
    def activate_license(self, license_key: str) -> Dict[str, Any]:
        """
        Activate a license key for this machine.
        
        Args:
            license_key: The license key to activate
            
        Returns:
            Dictionary with activation result
        """
        try:
            response = requests.post(
                f"{self.server_url}/api/license/activate",
                json={
                    'license_key': license_key,
                    'machine_id': self.machine_id
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Save to cache if successful
                if result.get('success'):
                    cache_data = {
                        'valid': True,
                        'license_key': license_key,
                        'verified_at': datetime.now().isoformat(),
                        'license_type': result.get('license_type'),
                        'expiry_date': result.get('expiry_date')
                    }
                    self._save_cache(cache_data)
                
                return result
            else:
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                return {
                    'success': False,
                    'error': error_data.get('error', f'Server error: {response.status_code}')
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
    
    def deactivate_license(self, license_key: str) -> Dict[str, Any]:
        """
        Deactivate a license key.
        
        Args:
            license_key: The license key to deactivate
            
        Returns:
            Dictionary with deactivation result
        """
        try:
            response = requests.post(
                f"{self.server_url}/api/license/deactivate",
                json={
                    'license_key': license_key,
                    'machine_id': self.machine_id
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Clear cache if successful
                if result.get('success'):
                    if os.path.exists(self.cache_file):
                        os.remove(self.cache_file)
                
                return result
            else:
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                return {
                    'success': False,
                    'error': error_data.get('error', f'Server error: {response.status_code}')
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
    
    def check_server_status(self) -> bool:
        """
        Check if the license server is reachable.
        
        Returns:
            True if server is reachable, False otherwise
        """
        try:
            response = requests.get(
                self.server_url,
                timeout=self.timeout
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
