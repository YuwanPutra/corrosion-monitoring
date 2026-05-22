import pytest
import sys
import os

# Add the root directory to sys.path so we can import logic_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic_engine import calculate_life, get_status_action

def test_calculate_life_c3():
    # C3 rate is ~37um/y, thickness 85um, 0% corrosion
    life = calculate_life("C3", 0)
    assert round(life, 1) == 2.3 # (85/37)

def test_calculate_life_c3_50_percent():
    # C3 rate 37um, 50% corrosion reduces functional life
    life = calculate_life("C3", 50)
    assert round(life, 1) == 1.1 # (85/37) * 0.5

def test_status_aman():
    status, color, action = get_status_action(30)
    assert status == "Aman"
    assert color == "text-success"

def test_status_kritis():
    status, color, action = get_status_action(85)
    assert status == "Kritis"
    assert color == "text-danger"

def test_corrosion_ai_simulation():
    from logic_engine import CorrosionAI
    import os
    
    # Create a dummy image for testing
    from PIL import Image
    dummy_img_path = "test_dummy.png"
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(dummy_img_path)
    
    ai = CorrosionAI()
    result = ai.analyze_image(dummy_img_path)
    assert result == 45.0
    
    # Clean up
    if os.path.exists(dummy_img_path):
        os.remove(dummy_img_path)

if __name__ == "__main__":
    # Simple test runner
    test_calculate_life_c3()
    test_calculate_life_c3_50_percent()
    test_status_aman()
    test_status_kritis()
    test_corrosion_ai_simulation()
    print("All tests passed!")
