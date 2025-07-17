#!/usr/bin/env python3
"""Test script for Docling VLM Engine with picture annotation."""

import sys
from pathlib import Path
from logging import basicConfig, INFO
from time import time

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from processors.pdf_converter.engines.docling_vlm_engine import DoclingVLMEngine

def test_docling_vlm_engine():
    """Test the enhanced Docling VLM engine with picture annotation."""
    
    # Configure logging
    basicConfig(level=INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    print("🧪 Testing Docling VLM Engine with Picture Annotation")
    print("=" * 60)
    
    # Check if VLM is available
    print(f"📚 Docling Available: {DoclingVLMEngine.is_available()}")
    print(f"🤖 VLM Available: {DoclingVLMEngine.is_vlm_available()}")
    
    if not DoclingVLMEngine.is_available():
        print("❌ Docling not available. Please install with: pip install 'docling[vlm]'")
        return False
    
    # Test PDF path (using existing test document)
    test_pdf = Path("../shared_data/documents/pdf/PCI-DSS-v4_0_1.pdf")
    
    if not test_pdf.exists():
        print(f"❌ Test PDF not found: {test_pdf}")
        print("Please ensure you have a test PDF file available.")
        return False
    
    try:
        # Test different VLM configurations
        test_configs = [
            {
                "name": "Basic VLM with Granite Vision",
                "config": {
                    "enable_picture_description": True,
                    "vision_model": "granite_vision",
                    "enable_ocr": True,
                    "enable_table_structure": True
                }
            },
            {
                "name": "VLM with SmolVLM",
                "config": {
                    "enable_picture_description": True,
                    "vision_model": "smolvlm",
                    "enable_ocr": True,
                    "enable_table_structure": True
                }
            },
            {
                "name": "VLM with Custom Prompt",
                "config": {
                    "enable_picture_description": True,
                    "vision_model": "granite_vision",
                    "picture_description_prompt": "Describe this image focusing on security compliance elements, diagrams, and technical details that would be relevant for cybersecurity documentation.",
                    "enable_ocr": True,
                    "enable_table_structure": True
                }
            }
        ]
        
        for test_config in test_configs:
            print(f"\n🔧 Testing: {test_config['name']}")
            print("-" * 40)
            
            try:
                # Initialize engine
                engine = DoclingVLMEngine(**test_config['config'])
                
                # Test conversion
                start_time = time()
                result = engine.convert(test_pdf)
                conversion_time = time() - start_time
                
                print(f"✅ Conversion completed in {conversion_time:.2f}s")
                print(f"📄 Content length: {len(result):,} characters")
                
                # Validate quality
                quality = engine.validate_quality(result)
                print(f"📊 Quality: {quality['quality_assessment']}")
                print(f"🖼️ Image descriptions: {quality.get('image_descriptions', 0)}")
                print(f"🤖 VLM descriptions: {quality.get('has_vlm_descriptions', False)}")
                
                # Generate metadata
                metadata = engine.generate_metadata(test_pdf, result)
                print(f"🔧 VLM features: {metadata.get('vlm_enhancements', {}).get('automated_image_annotation', False)}")
                
                # Check for VLM-specific content
                if "**Image" in result:
                    print("🎉 VLM-generated image descriptions found!")
                    image_count = result.count("**Image")
                    print(f"📷 Total images with descriptions: {image_count}")
                else:
                    print("ℹ️ No VLM image descriptions found (document may not contain images)")
                
            except Exception as e:
                print(f"❌ Test failed: {e}")
                continue
        
        print("\n🎉 All tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        return False

def test_single_image():
    """Test processing a single image file."""
    
    print("\n🖼️ Testing Single Image Processing")
    print("=" * 40)
    
    # You can test with any image file
    test_image_path = Path("test_image.jpg")  # Replace with actual image path
    
    if not test_image_path.exists():
        print(f"ℹ️ Test image not found: {test_image_path}")
        print("Skipping single image test.")
        return True
    
    try:
        engine = DoclingVLMEngine(
            enable_picture_description=True,
            vision_model="granite_vision"
        )
        
        if not engine.supports_image_description:
            print("❌ Image description not supported")
            return False
        
        # Convert single image
        result = engine.convert_image_only(test_image_path)
        
        print(f"✅ Image processed successfully")
        print(f"📝 Description: {result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Single image test failed: {e}")
        return False

def main():
    """Main test function."""
    
    print("🚀 Docling VLM Engine Test Suite")
    print("=" * 80)
    
    # Test engine availability
    success = test_docling_vlm_engine()
    
    # Test single image processing
    if success:
        test_single_image()
    
    print("\n" + "=" * 80)
    print("🏁 Testing completed!")

if __name__ == "__main__":
    main()