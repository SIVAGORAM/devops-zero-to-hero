# Python Day 22: Logging in Python

Welcome to **Day 22**! 
If your automation script runs at 3:00 AM and fails, how do you know what went wrong? `print()` statements disappear the moment the terminal closes. 

Professional DevOps engineers use the built-in `logging` module to track exactly what a script is doing, when it did it, and save the traceback if it crashes.

---

## 1. `print()` vs `logging`
Why do we use logging instead of print?
1. **Persistence:** Logs can be saved to files, sent to AWS CloudWatch, or shipped to Datadog.
2. **Context:** Logs automatically include timestamps (`%(asctime)s`), file names, and severity levels.
3. **Filtering:** You can easily turn off `INFO` logs in production but keep `ERROR` logs active.

---

## 2. The 5 Logging Levels
| Level | Use Case in DevOps |
| :--- | :--- |
| `DEBUG` | Deep diagnostic information. (e.g., *Connected to DB on port 5432*) |
| `INFO` | Standard operational events. (e.g., *Starting Docker deployment*) |
| `WARNING` | Something unexpected, but script can continue. (e.g., *Disk usage > 80%*) |
| `ERROR` | A specific operation failed. (e.g., *Failed to restart nginx*) |
| `CRITICAL`| Total system failure. (e.g., *Production database is unreachable*) |

---

## 3. Basic Configuration
For small scripts, you can configure logging globally in one line:

```python
import logging

logging.basicConfig(
    filename="automation.log",       # Remove this line to print to Terminal instead
    level=logging.INFO,              # Show INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Deployment script started.")
```

---

## 4. The DevOps Secret: `logging.exception()`
If a script crashes, you don't just want an error message—you want the **Traceback** so you know exactly which line of code broke. 
Always use `logging.exception()` inside your `except` blocks!

```python
import logging

try:
    result = 10 / 0
except Exception:
    # This automatically captures and logs the entire Traceback!
    logging.exception("A critical calculation failed during deployment.")
```

---

## 5. Security: Never Log Secrets
Logs are often shipped to centralized servers (like Splunk or ELK) where dozens of developers can read them. 

> [!CAUTION]
> **Never log sensitive data!**
> Do not log passwords, AWS Secret Keys, API Tokens, or SSH Keys.
> **Bad:** `logging.info(f"Using AWS Key: {aws_secret}")`
> **Good:** `logging.info("AWS Authentication successful.")`

---

## 6. Advanced Architecture: Loggers, Handlers, and Rotation
In a massive DevOps pipeline, you might want `INFO` logs printing to the Console, but `DEBUG` logs saving to a file. 

Furthermore, if your script runs forever, `application.log` could grow to 50GB and crash your server! We solve this with **Handlers** and **Log Rotation**.

```python
import logging
from logging.handlers import RotatingFileHandler

# 1. Create a dedicated Logger for this file (rather than global root)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 2. Create a Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 3. Create a Console Handler (For the terminal)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 4. Create a Rotating File Handler (Prevents huge log files!)
# Max size 1MB. Keep 3 backup files (app.log.1, app.log.2)
file_handler = RotatingFileHandler("app.log", maxBytes=1024*1024, backupCount=3)
file_handler.setFormatter(formatter)

# 5. Attach handlers to Logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("Advanced logging initialized!")
```

---

## 7. Advanced DevOps: Structured JSON Logging
In modern cloud environments, nobody reads text files anymore. Logs are shipped to **Datadog, Splunk, or Elasticsearch (ELK)**. These systems cannot easily parse `2026-09-12 - INFO - Started`. They require **Structured JSON Logs**.

While you can write a custom Formatter, most DevOps engineers install the `python-json-logger` library:

```python
# pip install python-json-logger
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
handler = logging.StreamHandler()

# Tell Python to format the logs as JSON objects!
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Deployment successful", extra={"app": "nginx", "env": "prod"})
# Output: {"asctime": "2026-09-12", "levelname": "INFO", "message": "Deployment successful", "app": "nginx", "env": "prod"}
```

---

## 8. Advanced DevOps: Linux Syslog Integration
Instead of writing logs to custom files, sometimes you want your Python script to act exactly like a native Linux service and write its logs directly to `/var/log/syslog`.

```python
import logging
from logging.handlers import SysLogHandler

logger = logging.getLogger()
# Send logs directly to the Linux Syslog daemon (works on Ubuntu/Debian)
syslog_handler = SysLogHandler(address='/dev/log')

logger.addHandler(syslog_handler)
logger.info("Python automation script triggered!")
```

---

## 🧑‍💻 Practice Exercises
We have created `day22_advanced_logging.py` in this folder. 
It demonstrates a professional DevOps Logging architecture. It configures a dual-handler system (Terminal + Rotating File), performs a mock application deployment, logs variables securely, and perfectly handles a simulated failure using `logging.exception()`!
