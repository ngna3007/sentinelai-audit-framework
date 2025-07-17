import os
import shutil
import glob

def cleanup_folders():
    """Clean up requirement and evidence folders using pure Python"""
    
    print("🧹 Starting folder cleanup...")
    
    deleted_files = []
    
    try:
        # Clean requirement/ folder
        if os.path.exists("requirement"):
            req_files = glob.glob("requirement/*")
            for file_path in req_files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted_files.append(f"{file_path}/ (directory)")
            
            print(f"✅ Cleaned requirement/ folder ({len([f for f in req_files if os.path.exists(f) == False])} items deleted)")
        else:
            print("📁 requirement/ folder doesn't exist")
        
        # Clean evidence/ folder
        if os.path.exists("evidence"):
            ev_files = glob.glob("evidence/*")
            for file_path in ev_files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted_files.append(f"{file_path}/ (directory)")
            
            print(f"✅ Cleaned evidence/ folder ({len([f for f in ev_files if os.path.exists(f) == False])} items deleted)")
        else:
            print("📁 evidence/ folder doesn't exist")
        
        # Create directories if they don't exist
        os.makedirs("requirement", exist_ok=True)
        os.makedirs("evidence", exist_ok=True)
        
        print(f"📋 Total files/folders deleted: {len(deleted_files)}")
        if deleted_files:
            print("🗑️ Deleted items:")
            for item in deleted_files:
                print(f"   - {item}")
        
        return {
            "success": True,
            "deleted_count": len(deleted_files),
            "deleted_files": deleted_files
        }
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "deleted_count": len(deleted_files)
        }
        
def main():
    print("🗑️ Cleanup Test\n")
    
    result = cleanup_folders()
    
    if result["success"]:
        print(f"\n✅ Cleanup successful!")
        print(f"📊 Files deleted: {result['deleted_count']}")
    else:
        print(f"\n❌ Cleanup failed: {result.get('error', 'Unknown error')}")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)