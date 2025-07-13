#!/usr/bin/env python3
"""
Credential management for database connections
"""

import os
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

class CredentialManager:
    """Manages database credentials securely"""
    
    def __init__(self, env_file: str = '.env'):
        self.env_file = Path(env_file)
        load_dotenv(self.env_file)
    
    def get_supabase_credentials(self) -> Dict[str, Optional[str]]:
        """Get Supabase credentials from environment"""
        return {
            'url': os.getenv('SUPABASE_URL'),
            'service_role_key': os.getenv('SUPABASE_SERVICE_ROLE_KEY'),
            'anon_key': os.getenv('SUPABASE_ANON_KEY')
        }
    
    def validate_credentials(self) -> bool:
        """Validate that required credentials are present"""
        creds = self.get_supabase_credentials()
        required = ['url', 'service_role_key']
        
        missing = [key for key in required if not creds.get(key)]
        if missing:
            print(f"Missing required credentials: {missing}")
            return False
        
        return True
    
    def create_env_template(self) -> None:
        """Create a template .env file"""
        template = """# Supabase Configuration
SUPABASE_URL=your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key

# Database Configuration
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres

# Import Configuration
CSV_IMPORT_BATCH_SIZE=1000
ENABLE_IMPORT_VALIDATION=true
"""
        
        with open('.env.template', 'w') as f:
            f.write(template)
        
        print("Created .env.template file")

# Global credential manager
credential_manager = CredentialManager()