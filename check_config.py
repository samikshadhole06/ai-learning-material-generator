"""
Configuration checker to verify all settings are correct.
"""

import os
import sys

def check_configuration():
    """Check all configuration settings."""
    
    print("🔍 Checking Configuration...\n")
    
    issues = []
    
    # Check .env file
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        issues.append(".env file missing")
    else:
        print("✅ .env file exists")
        
        # Check API key
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("❌ GEMINI_API_KEY not set in .env")
            issues.append("GEMINI_API_KEY not configured")
        elif api_key == "your_gemini_api_key_here":
            print("⚠️  GEMINI_API_KEY still has placeholder value")
            print("   Get your key from: https://aistudio.google.com/app/apikey")
            issues.append("GEMINI_API_KEY not replaced with actual key")
        elif not api_key.startswith("AIza"):
            print("⚠️  GEMINI_API_KEY format looks incorrect")
            print("   Keys typically start with 'AIza'")
            issues.append("GEMINI_API_KEY may be invalid")
        else:
            print(f"✅ GEMINI_API_KEY is set ({api_key[:10]}...)")
    
    print()
    
    # Check config.py
    try:
        import config
        print("✅ config.py loaded successfully")
        
        if hasattr(config, 'EMBEDDING_MODEL'):
            print(f"✅ EMBEDDING_MODEL: {config.EMBEDDING_MODEL}")
        
        if hasattr(config, 'CHUNK_SIZE'):
            print(f"✅ CHUNK_SIZE: {config.CHUNK_SIZE}")
        
        if hasattr(config, 'CHUNK_OVERLAP'):
            print(f"✅ CHUNK_OVERLAP: {config.CHUNK_OVERLAP}")
        
        if hasattr(config, 'TOP_K'):
            print(f"✅ TOP_K: {config.TOP_K}")
            
        if hasattr(config, 'GEMINI_MODEL'):
            print(f"✅ GEMINI_MODEL: {config.GEMINI_MODEL}")
            
    except Exception as e:
        print(f"❌ Error loading config.py: {str(e)}")
        issues.append(f"config.py error: {str(e)}")
    
    print()
    
    # Check data directory
    if not os.path.exists('data'):
        print("⚠️  data/ directory not found (will be created when needed)")
    else:
        print("✅ data/ directory exists")
    
    print()
    
    # Summary
    if issues:
        print("=" * 60)
        print("⚠️  Configuration Issues Found:")
        print("=" * 60)
        for issue in issues:
            print(f"  • {issue}")
        print()
        print("Please fix these issues before running the application.")
        return False
    else:
        print("=" * 60)
        print("✅ Configuration looks good!")
        print("=" * 60)
        print("\nYou can now run:")
        print("  streamlit run app.py")
        return True


if __name__ == "__main__":
    success = check_configuration()
    sys.exit(0 if success else 1)
