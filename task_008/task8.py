#1: Create 3 simple unit tests for Task_2 (modify your code to have 3 different methods in Task_2 solving if needed).
#2. Create testng.xml which should execute your test class. Execute this file
#3. Add a Data provider for each test.
#4. Create a test with parameters loaded from testng.xml.

#---------------------------
# testng is java framework, so for python i'll use pytest
# pytest is kinda similar to testng and provides similar functionality
# pip install pytest
# to launch test : pytest -v

import pytest
from task2_mod import StringOperations

# data providers
length_test_data = [
     ('AT Course 2024', 14),
     ('Testing', 7)
]

substring_test_data = [
    ('AT Course 2024', 3, 9, 'Course'),
    ('Python Testing', 0, 6, 'Python')
]

index_test_data = [
    ("AT Course 2024", "Course", 3),
    ("Python Testing", "Testing", 7)
]

# tests with parameters loaded from pytest.ini (similar to testng.xml)
@pytest.mark.parametrize("input_text,expected", length_test_data)
def test_get_length(input_text, expected):
    result = StringOperations.get_length(input_text)
    assert result == expected

@pytest.mark.parametrize("input_text,start,end,expected", substring_test_data)
def test_get_substring(input_text, start, end, expected):
    result = StringOperations.get_substring(input_text, start, end)
    assert result == expected

@pytest.mark.parametrize("input_text,substring,expected", index_test_data)
def test_find_index(input_text, substring, expected):
    result = StringOperations.find_index(input_text, substring)
    assert result == expected
