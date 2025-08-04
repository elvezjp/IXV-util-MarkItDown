import os
import re
import base64
from typing import Dict, Tuple


def extract_and_save_images(markdown_content: str, output_file_path: str) -> str:
    """
    Extract base64 images from markdown content and save them as files.
    
    Args:
        markdown_content: Markdown content containing base64 images
        output_file_path: Path to the output markdown file
        
    Returns:
        Modified markdown content with image links replaced
    """
    # Create images directory
    base_name = os.path.splitext(os.path.basename(output_file_path))[0]
    images_dir = os.path.join(os.path.dirname(output_file_path), f"{base_name}_images")
    
    # Pattern to match markdown images with data URI
    pattern = r'!\[([^\]]*)\]\(data:([^;]+);base64,([^)]+)\)'
    
    image_counter = 1
    
    def replace_image(match):
        nonlocal image_counter
        
        alt_text = match.group(1)
        mime_type = match.group(2)
        base64_data = match.group(3)
        
        # Determine file extension from MIME type
        extension = _get_extension_from_mime_type(mime_type)
        
        # Generate unique filename
        filename = f"image{image_counter}{extension}"
        image_counter += 1
        
        # Ensure images directory exists
        if not os.path.exists(images_dir):
            os.makedirs(images_dir, exist_ok=True)
        
        # Save image file
        image_path = os.path.join(images_dir, filename)
        try:
            with open(image_path, 'wb') as f:
                f.write(base64.b64decode(base64_data))
        except Exception as e:
            print(f"Warning: Failed to save image {filename}: {e}")
            # Return original data URI if saving fails
            return match.group(0)
        
        # Return relative path link
        relative_image_path = os.path.join(f"{base_name}_images", filename)
        return f"![{alt_text}]({relative_image_path})"
    
    # Replace all base64 images with file links
    modified_content = re.sub(pattern, replace_image, markdown_content)
    
    return modified_content


def _get_extension_from_mime_type(mime_type: str) -> str:
    """
    Get file extension from MIME type.
    
    Args:
        mime_type: MIME type string (e.g., 'image/png')
        
    Returns:
        File extension with dot (e.g., '.png')
    """
    mime_to_ext = {
        'image/png': '.png',
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/gif': '.gif',
        'image/bmp': '.bmp',
        'image/webp': '.webp',
        'image/svg+xml': '.svg',
        'image/tiff': '.tiff',
        'image/x-icon': '.ico',
    }
    
    return mime_to_ext.get(mime_type.lower(), '.png')


def count_base64_images(markdown_content: str) -> int:
    """
    Count the number of base64 images in markdown content.
    
    Args:
        markdown_content: Markdown content to analyze
        
    Returns:
        Number of base64 images found
    """
    pattern = r'!\[([^\]]*)\]\(data:([^;]+);base64,([^)]+)\)'
    return len(re.findall(pattern, markdown_content))