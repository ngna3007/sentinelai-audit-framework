#!/usr/bin/env python3
"""
Supabase client wrapper with error handling and retries
"""

import time
from typing import Dict, Any, Optional
from supabase import Client
from .connection import db_connection
from .credentials import credential_manager

class SupabaseClientWrapper:
    """Wrapper around Supabase client with additional functionality"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self._ensure_credentials()
    
    def _ensure_credentials(self):
        """Ensure credentials are valid before creating client"""
        if not credential_manager.validate_credentials():
            raise ValueError("Invalid or missing Supabase credentials")
    
    def get_client(self) -> Client:
        """Get Supabase client with connection management"""
        return db_connection.get_client()
    
    def execute_with_retry(self, operation, max_retries: int = 3, delay: float = 1.0):
        """Execute operation with retry logic"""
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
    
    def test_connection(self) -> bool:
        """Test database connection"""
        return db_connection.test_connection()
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information"""
        return db_connection.get_connection_info()

# Global instance - lazy loaded
supabase_client = None

def get_supabase_client():
    """Get or create the global Supabase client instance"""
    global supabase_client
    if supabase_client is None:
        supabase_client = SupabaseClientWrapper()
    return supabase_client
