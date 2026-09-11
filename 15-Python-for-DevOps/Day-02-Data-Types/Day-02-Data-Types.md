# Python Day 02: Data Types, Strings & Regex for DevOps

Welcome to **Day 02**! 
Today, we focus on how Python stores data, manipulates text (Strings), performs math (Numbers), and extracts specific information from massive log files using Regular Expressions (Regex).

---

## 1. Data Types
In Python, a data type defines what kind of value a variable can store and what operations can be performed on that value.

### Common Python Data Types
| Data Type | Description | Example |
| :--- | :--- | :--- |
| **int** | Whole numbers | `x = 10` |
| **float** | Decimal numbers | `x = 10.5` |
| **complex** | Complex numbers | `x = 2 + 3j` |
| **str** | Text/string | `x = "DevOps"` |
| **list** | Ordered, mutable collection | `x = [1, 2, 3]` |
| **tuple** | Ordered, immutable collection | `x = (1, 2, 3)` |
| **dict** | Key-value pairs | `x = {"name": "Siva"}` |
| **set** | Unordered unique values | `x = {1, 2, 3}` |
| **frozenset** | Immutable set | `x = frozenset([1, 2, 3])` |
| **bool** | True or False | `x = True` |
| **bytes** | Immutable binary data | `x = b"Hello"` |
| **bytearray** | Mutable binary data | `x = bytearray(b"Hello")` |
| **NoneType** | Represents no value | `x = None` |

> [!TIP]
> **Check the Data Type:** Use the `type()` function to verify what kind of data you are working with. 
> ```python
> x = 10
> print(type(x))  # Output: <class 'int'>
> ```

### DevOps Highlight: Lists & Dictionaries
While we will dive deeper into these later, as a DevOps engineer, you will use **Lists** to store collections of servers/IPs, and **Dictionaries** to parse JSON responses from Cloud APIs:
```python
# A List of servers to deploy to
servers = ["web-01", "web-02", "db-01"]

# A Dictionary representing a server configuration (similar to JSON)
server_config = {
    "hostname": "web-01",
    "ip_address": "192.168.1.10",
    "status": "running"
}
print(f"Connecting to {server_config['hostname']} at {server_config['ip_address']}...")
```

---

## 2. Strings
A string is a sequence of characters. 
**Important:** Strings are *immutable*, meaning you cannot directly modify an existing string. Any "modification" creates a brand new string.

### String Creation & Indexing
```python
name = "Siva"
course = 'DevOps'
message = """This is a 
multiline string"""

text = "Python"
# Indexing starts from 0
print(text[0])  # P
print(text[5])  # n
```

### Essential String Methods for DevOps
DevOps engineers constantly manipulate strings to clean up CLI outputs, parse file paths, and format Slack alerts.

1. **F-Strings (Formatting)**: The most modern and readable way to inject variables into strings. Used constantly for generating dynamic URLs and shell commands.
   ```python
   server = "aws-us-east-1"
   port = 8080
   print(f"Connecting to {server} on port {port}...")
   ```
2. **Concatenation (`+`)**: Combine strings together.
3. **Length (`len()`)**: Count characters in a string.
4. **Upper/Lower (`upper()`, `lower()`)**: Standardize text casing.
5. **Replace (`replace()`)**: Swap specific substrings.
6. **Split (`split()`)**: Divide a string into a List (extremely useful for parsing command outputs!).
7. **Strip (`strip()`)**: Remove leading/trailing whitespaces (useful for cleaning up `stdout` from Linux commands).
8. **Substring Check (`in`)**: Check if a word exists in a line of text (useful for finding "ERROR" in logs).

---

## 3. Numeric Data Types
Python mainly uses `int` (whole numbers) and `float` (decimals).

### Operations
- **Addition/Subtraction/Multiplication/Division**: `+`, `-`, `*`, `/`
- **Integer (Floor) Division**: `//` (Returns the quotient without the remainder).
- **Modulus (Remainder)**: `%` (Returns just the remainder).
- **Absolute Value**: `abs()` (Converts negative to positive).
- **Rounding**: `round(3.1415, 2)` (Rounds to specified decimal places).

### DevOps Gotcha: Type Casting Environment Variables
In DevOps, you often read configuration variables from the Operating System environment. **Environment variables are always strings!** If you need to do math (like multiplying a timeout), you must cast it to an `int` or `float` first.
```python
import os
os.environ["TIMEOUT"] = "30"  # This is a string!

# BAD: print(os.environ.get("TIMEOUT") * 2) --> Prints "3030"
# GOOD: 
timeout = int(os.environ.get("TIMEOUT"))
print(timeout * 2)  # Prints 60
```

---

## 4. Regular Expressions (Regex) 🔍
Regular expressions are arguably the **most important text-processing tool** for a DevOps engineer.
You use the `re` module in Python to find patterns.

> [!TIP]
> **Raw Strings (`r""`):** You will notice we always prefix regex patterns with an `r` (e.g., `r"\bIP\b"`). This tells Python to treat backslashes as literal characters rather than escape characters (like `\n`). Always use Raw Strings for Regex to prevent weird bugs!

**Real-world DevOps Use Cases:**
- Searching through millions of lines of logs for IPs.
- Extracting specific error codes.
- Validating email formats or server names.

### Important Regex Symbols
| Symbol | Meaning | Example |
| :---: | :--- | :--- |
| `.` | Any character | `a.b` matches `acb` |
| `*` | Zero or more occurrences | `a*` matches ``, `a`, `aaa` |
| `+` | One or more occurrences | `a+` matches `a`, `aaa` (not empty) |
| `?` | Zero or one occurrence | `a?` matches `` or `a` |
| `[]`| Character class | `[a-z]` matches any lowercase letter |
| `^` | Beginning of string | `^ERROR` matches lines *starting* with ERROR |
| `$` | End of string | `failed$` matches lines *ending* with failed |

### Core `re` Functions
1. **`re.match()`**: Checks for a match ONLY at the **beginning** of the string.
2. **`re.search()`**: Searches for a match **anywhere** in the string.
3. **`re.findall()`**: Finds **all** occurrences of a pattern and returns them as a List.
4. **`re.sub()`**: Finds a pattern and **replaces** it with new text.
5. **`re.split()`**: **Splits** the text based on a regex pattern.

---

## 5. Summary & Practice
As a DevOps engineer, you will frequently combine Linux commands, Python logic, and Regex:

**1. Detecting Errors in Logs:**
```python
import re
log = "INFO Server started\nERROR Connection failed on port 8080"

if re.search(r"^ERROR", log, re.MULTILINE):
    print("Alert: Found an error in the logs!")
```

**2. Extracting IP Addresses (Advanced DevOps Regex):**
```python
import re
log_line = "Failed password for root from 192.168.1.55 port 22 ssh2"
# Regex pattern for a standard IPv4 address
ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

found_ips = re.findall(ip_pattern, log_line)
print(f"Malicious IP detected: {found_ips[0]}")
```

### 🧑‍💻 Practice Files
We have created 14 distinct Python scripts in this folder for you to run and analyze. Do not just memorize them—understand *why* they work!
- `string-concat.py`
- `string-len.py`
- `string-lowercase.py`
- `string-replace.py`
- `string-split.py`
- `string-strip.py`
- `string-substring.py`
- `int.py`
- `float.py`
- `regex-match.py`
- `regex-search.py`
- `regex-findall.py`
- `regex-replace.py`
- `regex-split.py`
