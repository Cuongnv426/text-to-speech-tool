#!/usr/bin/env python3
"""
Test script to validate the voice detection logic without actually generating audio.
This confirms gender detection works properly.
"""

from config import detect_gender, FEMALE_NAMES, MALE_NAMES

# Test data
test_cases = [
    ('Alice', 'female'),
    ('Bob', 'male'),
    ('Sarah', 'female'),
    ('John', 'male'),
    ('Emma', 'female'),
    ('David', 'male'),
    ('Jessica', 'female'),
    ('James', 'male'),
    ('Charlie', 'neutral'),  # Not in common lists
    ('Diana', 'female'),
    ('Narrator', 'neutral'),  # Not in common lists
]

print("=" * 60)
print("TTS Voice Detection Test Suite")
print("=" * 60)

print(f"\nFemale names database: {len(FEMALE_NAMES)} names")
print(f"Male names database: {len(MALE_NAMES)} names")

print("\n" + "-" * 60)
print("Testing gender detection...")
print("-" * 60)

passed = 0
failed = 0

for name, expected_gender in test_cases:
    detected_gender = detect_gender(name)
    
    # For neutral, accept any non-specific gender
    if expected_gender == 'neutral':
        success = detected_gender == 'neutral'
    else:
        success = detected_gender == expected_gender
    
    status = "✓ PASS" if success else "✗ FAIL"
    
    if success:
        passed += 1
    else:
        failed += 1
    
    print(f"{status} | {name:15} -> Expected: {expected_gender:8} Got: {detected_gender:8}")

print("-" * 60)
print(f"\nResults: {passed} passed, {failed} failed out of {len(test_cases)} tests")

if failed == 0:
    print("\n✅ All tests PASSED! Voice detection logic is working correctly.")
    print("\nNext step: Run the app with:")
    print("  python tts-simple.py")
else:
    print(f"\n⚠️  {failed} test(s) failed. Check config.py")

print("\n" + "=" * 60)
