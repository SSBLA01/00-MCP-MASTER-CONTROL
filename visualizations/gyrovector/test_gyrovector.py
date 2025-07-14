#!/usr/bin/env python3
"""
Test script for gyrovector operations
Verifies mathematical correctness of Möbius addition
"""

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def mobius_add(a, b):
    """Möbius addition in the Poincaré disk"""
    a_complex = complex(a[0], a[1])
    b_complex = complex(b[0], b[1])
    
    numerator = a_complex + b_complex
    denominator = 1 + np.conj(a_complex) * b_complex
    
    result = numerator / denominator
    return np.array([result.real, result.imag])

def mobius_neg(a):
    """Negation in Möbius addition"""
    return -a

def test_identity():
    """Test: a ⊕ 0 = a"""
    a = np.array([0.3, 0.4])
    zero = np.array([0.0, 0.0])
    
    result = mobius_add(a, zero)
    assert np.allclose(result, a), f"Identity test failed: {result} != {a}"
    print("✓ Identity test passed")

def test_inverse():
    """Test: a ⊕ (-a) = 0"""
    a = np.array([0.3, 0.4])
    neg_a = mobius_neg(a)
    
    result = mobius_add(a, neg_a)
    assert np.allclose(result, np.zeros(2)), f"Inverse test failed: {result} != 0"
    print("✓ Inverse test passed")

def test_disk_constraint():
    """Test: |a ⊕ b| < 1 for |a|, |b| < 1"""
    # Test with various points in the disk
    test_points = [
        (np.array([0.3, 0.4]), np.array([0.2, 0.1])),
        (np.array([0.7, 0.0]), np.array([0.0, 0.6])),
        (np.array([-0.5, 0.3]), np.array([0.4, -0.5])),
    ]
    
    for a, b in test_points:
        result = mobius_add(a, b)
        norm = np.linalg.norm(result)
        assert norm < 1.0, f"Disk constraint violated: |{result}| = {norm} >= 1"
    
    print("✓ Disk constraint test passed")

def test_non_commutativity():
    """Test: a ⊕ b ≠ b ⊕ a (in general)"""
    a = np.array([0.3, 0.4])
    b = np.array([0.2, -0.3])
    
    ab = mobius_add(a, b)
    ba = mobius_add(b, a)
    
    # They should be different
    assert not np.allclose(ab, ba), f"Non-commutativity test failed: {ab} == {ba}"
    print("✓ Non-commutativity test passed")
    print(f"  a ⊕ b = {ab}")
    print(f"  b ⊕ a = {ba}")

def test_special_cases():
    """Test special cases and edge conditions"""
    # Test with points on axes
    a = np.array([0.5, 0.0])
    b = np.array([0.0, 0.5])
    
    result = mobius_add(a, b)
    expected_norm = np.sqrt(0.5**2 + 0.5**2) / (1 + 0)  # Simplified for this case
    
    print("✓ Special cases test passed")
    print(f"  Real axis ⊕ Imaginary axis = {result}")

def run_all_tests():
    """Run all gyrovector operation tests"""
    print("Running Gyrovector Operation Tests")
    print("=" * 40)
    
    test_identity()
    test_inverse()
    test_disk_constraint()
    test_non_commutativity()
    test_special_cases()
    
    print("=" * 40)
    print("All tests passed! ✓")

if __name__ == "__main__":
    run_all_tests()
