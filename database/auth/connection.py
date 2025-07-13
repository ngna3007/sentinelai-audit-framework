#!/usr/bin/env python3
"""
Database connection management for Supabase
"""

import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    """Manages database connections to Supabase"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize connection parameters"""
        self._client = None
        self._connection_params = self._load_connection_params()
    
    def _load_connection_params(self) -> dict:
        """Load connection parameters from environment"""
        return {
            'url': os.getenv('SUPABASE_URL'),
            'key': os.getenv('SUPABASE_SERVICE_ROLE_KEY'),
            'anon_key': os.getenv('SUPABASE_ANON_KEY')
        }
    
    def get_client(self) -> Client:
        """Get or create Supabase client"""
        if self._client is None:
            if not self._connection_params['url'] or not self._connection_params['key']:
                raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
            
            self._client = create_client(
                self._connection_params['url'],
                self._connection_params['key']
            )
        
        return self._client
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            client = self.get_client()
            result = client.table('pci_dss_controls').select('id').limit(1).execute()
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

# Global connection instance
db_connection = DatabaseConnection()