### **Part 1 – unittest (15 points)**

**A. string_utils.py Implementation (5 points)**

* (2 pts) `reverse_string(s)` implemented correctly
* (2 pts) `is_palindrome(s)` implemented correctly
* (1 pt) Handles invalid input (e.g., non-string) appropriately

**B. unittest Test File (test_string_utils.py) (10 points)**

* (2 pts) Correct test class inheriting from `unittest.TestCase`
* (3 pts) Tests for both functions (reverse + palindrome)
* (2 pts) Includes edge cases (empty string, single character, etc.)
* (2 pts) Includes invalid input / exception tests
* (1 pt) Tests are well-organized and readable

--- 

### **Part 2 – pytest (15 points)**

* (3 pts) pytest file (`test_string_utils_pytest.py`) created correctly
* (3 pts) Test functions written using `assert`
* (4 pts) Uses `@pytest.mark.parametrize` correctly
* (3 pts) Tests for exceptions using `pytest.raises()`
* (2 pts) All tests run successfully and pass

--- 

### **Part 3 – doctest (8 points)**

* (4 pts) Doctests correctly embedded in both functions
* (2 pts) Includes multiple examples (normal + edge cases)
* (2 pts) Doctests run successfully without errors

--- 

### **Code Quality & Execution (2 points)**

* (1 pt) Code is clean, readable, and well-structured
* (1 pt) All files run without errors and produce expected results

--- 

### **Bonus (Optional +2 points)**

* (+2 pts) Uses pytest fixtures correctly

--- 
**Total: 40 points (+2 bonus)**