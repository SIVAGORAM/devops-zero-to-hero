# Python Day 06: Operators for DevOps

Welcome to **Day 06**! Today, we dive into **Operators**. Operators are the special symbols or keywords that allow us to perform calculations, comparisons, and logic.

For a DevOps engineer, operators are the core of decision-making. We use them to verify disk space (`> 80`), check if an environment is authorized (`== "prod"`), or validate if an IP address exists in a list (`in banned_ips`).

---

## 1. Arithmetic Operators
Used to perform standard mathematical calculations.

| Operator | Name | Example | Output | DevOps Use Case |
| :---: | :--- | :--- | :--- | :--- |
| `+` | Addition | `5 + 3` | `8` | Adding up total memory across nodes. |
| `-` | Subtraction | `10 - 4` | `6` | Calculating remaining disk space. |
| `*` | Multiplication | `5 * 4` | `20` | Scaling timeouts or backoff intervals. |
| `/` | Division | `10 / 4` | `2.5` | Calculating percentage of CPU used. |
| `//` | Floor Division | `10 // 3` | `3` | Dividing servers equally into shards. |
| `%` | Modulus (Remainder)| `10 % 3` | `1` | Checking if a number is even/odd (e.g. `n % 2 == 0`). |
| `**`| Exponentiation | `2 ** 3` | `8` | Exponential backoff logic for API retries. |

---

## 2. Relational / Comparison Operators
Used to compare two values. They **always** return a Boolean (`True` or `False`).

| Operator | Meaning | Example | Output |
| :---: | :--- | :--- | :--- |
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `10 != 7` | `True` |
| `>` | Greater than | `10 > 5` | `True` |
| `<` | Less than | `5 < 10` | `True` |
| `>=` | Greater than or equal | `10 >= 10` | `True` |
| `<=` | Less than or equal | `5 <= 10` | `True` |

> [!CAUTION]
> **Important DevOps Distinction:** `==` vs `=`
> - `=` is for **Assignment** (e.g., `port = 80`)
> - `==` is for **Comparison** (e.g., `if port == 80:`)
> Confusing these is the #1 syntax error for freshers!

---

## 3. Logical Operators
Used to combine multiple Boolean conditions together.

| Operator | Rule | Example |
| :---: | :--- | :--- |
| **`and`** | BOTH sides must be True. | `if cpu > 80 and ram > 80:` |
| **`or`** | AT LEAST ONE side must be True. | `if env == "dev" or env == "test":` |
| **`not`** | Reverses the Boolean. | `if not server_is_online:` |

> [!TIP]
> **DevOps Secret: Short-Circuit Evaluation**
> Python is smart. If you write `if is_connected and run_backup():`, Python evaluates `is_connected` first. If the server is NOT connected (False), Python immediately stops checking and **never** runs `run_backup()`. This saves API calls and prevents your script from crashing!

---

## 4. Identity & Membership Operators

### Identity (`is` / `is not`)
Identity operators check if two variables point to the **exact same object in memory**, not just if they hold the same value.
- **Rule of Thumb:** Use `is` when comparing to `None` (e.g., `if ip_address is None:`). For comparing numbers or strings, use `==`.

### Membership (`in` / `not in`)
Membership operators check if a value exists inside a collection (like a List or a String).
```python
allowed_users = ["admin", "root", "devops"]

# Checking Lists
print("root" in allowed_users) # True

# Checking Strings
log = "ERROR: Disk full"
print("ERROR" in log) # True
```

---

## 5. Assignment Operators
Used to update a variable's value quickly without writing it out twice.

| Operator | Example | Equivalent To |
| :---: | :--- | :--- |
| `=` | `x = 10` | N/A |
| `+=` | `x += 5` | `x = x + 5` |
| `-=` | `x -= 3` | `x = x - 3` |
| `*=` | `x *= 2` | `x = x * 2` |

---

## 6. Bitwise Operators & Precedence

### Bitwise Operators
Bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`) manipulate individual bits (0s and 1s) of integer values. 
*(Note: As a DevOps engineer, you will rarely use these unless you are performing advanced networking subnet calculations).*

### Operator Precedence (Order of Operations)
Python evaluates math exactly like you learned in school (PEMDAS).
1. `()` Parentheses
2. `**` Exponentiation
3. `*`, `/`, `//`, `%` Multiplication/Division
4. `+`, `-` Addition/Subtraction

> [!TIP]
> **Best Practice:** If you have a complex equation, always wrap it in parentheses to force the order and make it easier to read! (e.g., `(5 + 3) * 2` instead of `5 + 3 * 2`).

---

## 7. Real-World DevOps Use Cases

### Server Health Check (Using Logical `or` & Relational `>`)
```python
cpu_usage = 85
memory_usage = 60

if cpu_usage > 80 or memory_usage > 80:
    print("WARNING: Server requires attention!")
else:
    print("Server is healthy.")
```

### Deployment Validation (Using Logical `and` & Relational `==`)
```python
environment = "production"
version = 10

if environment == "production" and version >= 10:
    print("Deployment Approved for Production")
else:
    print("Deployment Not Approved")
```

### The DevOps One-Liner: The Ternary Operator
DevOps engineers love writing clean code. Instead of writing a full 4-line `if/else` block just to assign a variable, we use the **Ternary Operator**:

**Syntax:** `[Value_If_True] if [Condition] else [Value_If_False]`

```python
disk_usage = 85

# Instead of doing this:
# if disk_usage > 80:
#     status = "CRITICAL"
# else:
#     status = "OK"

# Do this:
status = "CRITICAL" if disk_usage > 80 else "OK"
print(status)
```
This is perfect for quickly formatting Slack alert messages or status codes in your scripts!

---

## 🧑‍💻 Practice Exercises
We have created a script called `day06_operators.py` in this folder that combines all these operators into a single executable test. Run it locally to see how all the math, comparisons, and logic execute!
