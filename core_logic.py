import os
import shutil
from pathlib import Path

# Comprehensive file categories with more extensions
CATEGORIES = {
    "Images": ['.jpeg', '.jpg', '.png', '.gif', '.svg', '.bmp', '.ico', '.tiff', '.webp', '.psd'],
    "Documents": ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx', '.ppt', '.odt', '.rtf', '.csv'],
    "Videos": ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.m4v', '.3gp', '.mts'],
    "Audio": ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.wma', '.ogg', '.aiff', '.opus'],
    "Archives": ['.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.xz', '.iso'],
    "Code": ['.py', '.js', '.ts', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.rs', '.json', '.xml', '.yaml', '.yml'],
    "Executables": ['.exe', '.bat', '.sh', '.msi', '.app', '.deb', '.apk'],
    "Compressed": ['.zip', '.rar', '.7z', '.gz', '.tar', '.bz2'],
    "Data": ['.sql', '.db', '.sqlite', '.xml', '.json', '.csv'],
    "Spreadsheets": ['.xlsx', '.xls', '.csv', '.ods'],
    "Presentations": ['.pptx', '.ppt', '.odp']
}

def get_unique_filename(directory, filename):
    """Generate a unique filename if file already exists in destination."""
    file_path = os.path.join(directory, filename)
    
    if not os.path.exists(file_path):
        return filename
    
    # Split filename and extension
    name, ext = os.path.splitext(filename)
    counter = 1
    
    while os.path.exists(os.path.join(directory, f"{name}_{counter}{ext}")):
        counter += 1
    
    return f"{name}_{counter}{ext}"

def get_file_category(file_ext):
    """Determine file category based on extension."""
    file_ext = file_ext.lower()
    
    for category, extensions in CATEGORIES.items():
        if file_ext in extensions:
            return category
    
    return "Others"

def organize_directory(target_path):
    """
    Organize files in the target directory into categorized folders.
    
    Args:
        target_path: Absolute path to the directory to organize
        
    Returns:
        Dictionary with status and message
    """
    # Ensure standard path formatting
    target_path = os.path.abspath(target_path)
    
    # Validate directory
    if not os.path.exists(target_path):
        return {"status": "error", "message": "❌ Directory does not exist. Please check the path."}
    
    if not os.path.isdir(target_path):
        return {"status": "error", "message": "❌ Path is not a directory."}
    
    files_moved = 0
    files_skipped = 0
    categories_created = set()
    errors_log = []
    
    try:
        # Get all files in the directory
        items = os.listdir(target_path)
        
        if not items:
            return {"status": "error", "message": "📁 Directory is empty. Nothing to organize."}
        
        for filename in items:
            file_path = os.path.join(target_path, filename)
            
            # Skip if it's a directory or hidden file
            if os.path.isdir(file_path) or filename.startswith('.'):
                files_skipped += 1
                continue
            
            try:
                # Get file extension
                file_ext = os.path.splitext(filename)[1].lower()
                
                # Skip files without extension
                if not file_ext:
                    files_skipped += 1
                    continue
                
                # Determine category
                category = get_file_category(file_ext)
                
                # Create category folder if it doesn't exist
                category_path = os.path.join(target_path, category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path, exist_ok=True)
                    categories_created.add(category)
                
                # Handle duplicate filenames
                unique_filename = get_unique_filename(category_path, filename)
                destination = os.path.join(category_path, unique_filename)
                
                # Move the file
                shutil.move(file_path, destination)
                files_moved += 1
                
            except PermissionError:
                errors_log.append(f"Permission denied: {filename}")
                files_skipped += 1
            except Exception as e:
                errors_log.append(f"{filename}: {str(e)}")
                files_skipped += 1
        
        # Build success message
        message = f"✅ Successfully organized {files_moved} files!"
        
        if categories_created:
            message += f"\n📂 Created {len(categories_created)} categories: {', '.join(sorted(categories_created))}"
        
        if files_skipped > 0:
            message += f"\n⏭️ Skipped {files_skipped} items (folders/hidden files)"
        
        if errors_log:
            message += f"\n⚠️ Errors: {'; '.join(errors_log[:3])}"
            if len(errors_log) > 3:
                message += f"... and {len(errors_log) - 3} more"
        
        return {
            "status": "success",
            "message": message,
            "files_moved": files_moved,
            "files_skipped": files_skipped,
            "categories_created": list(categories_created)
        }
        
    except PermissionError:
        return {"status": "error", "message": "❌ Permission denied. You don't have access to this directory."}
    except Exception as e:
        return {"status": "error", "message": f"❌ An error occurred: {str(e)}"}
