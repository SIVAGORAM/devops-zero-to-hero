# Day 7 (Part 2): 🐧 Linux Fundamentals

> Trainer: 20+ Years Experienced DevOps Engineer  
> Focus: Real-world usage, production mindset, strong fundamentals

---

## 📌 Directory Management Commands

### 🔹 `mkdir -p` (Create Parent Directories)
```bash
mkdir -p abc/xyz/123
```
- `-p` → Parent option.
- Creates all missing parent directories automatically.
- Used in production to create application, logs, and deployment folders.

### 🔹 `rmdir` (Remove Empty Directory)
```bash
rmdir india/
```
- Removes directory only if empty.
- Rarely used in DevOps due to limitation.

### 🔹 `rm -r` (Recursive Delete)
```bash
rm -r india/
```
- Deletes directory and its contents recursively.
- Use carefully in servers.

### 🔹 `rm -rf` (Force Recursive Delete ⚠️)
```bash
rm -rf india/
```
- `-r` → recursive
- `-f` → force delete (no confirmation)
- Commonly used in automation & cleanup scripts.
- ⚠️ **Dangerous in production if misused.**

---

## 📄 File Management Commands

### 🔹 `touch` (Create Empty File)
```bash
touch 123.txt
```
- Creates an empty file.
- Updates timestamp if file already exists.

### 🔹 `rm` (Delete File)
```bash
rm 123.txt
```
- Permanently deletes file.

### 🔹 `stat` (File Metadata – Very Important)
```bash
stat 123.txt
```
Displays:
- File size
- Permissions
- Created time
- Accessed time
- Modified time

👉 *Used in debugging, auditing, and production issue analysis.*

---

## 📂 Listing Files and Directories (`ls`)

### 🔹 Basic Listing
```bash
ls
```

### 🔹 Long Listing
```bash
ls -l
```
- Shows permissions, owner, size, and timestamp.

### 🔹 Hidden Files
```bash
ls -a
ls -all
```
- Displays hidden files like `.git`, `.env`, `.bashrc`.
- Important for DevOps configurations.

### 🔹 Sorting Files
```bash
ls -lt    # Latest files first
ls -ltr   # Oldest files first
```

### 🔹 File Size (Human Readable)
```bash
ls -lh
```
- Displays sizes in KB, MB, GB.

### 🔹 One File Per Line
```bash
ls -1
```

### 🔹 Shortcut
```bash
ll
```
- Alias for `ls -l` (available on most Linux servers).

---

## 📜 Command History (Productivity Booster)

### 🔹 View Command History
```bash
history
```

### 🔹 Re-execute Commands
```bash
!!      # Run previous command
!582    # Run command number 582
!-13    # Run 13th command from bottom
```
👉 *Heavily used by senior DevOps engineers.*

---

## 📍 Navigation Commands

### 🔹 Present Working Directory
```bash
pwd
```

### 🔹 Change Directory
```bash
cd ../..
```
- Moves two levels up.

---

## 📖 Viewing & Creating File Content

### 🔹 View File Content
```bash
cat 123.txt
```

### 🔹 Create File with Content
```bash
cat > 456.txt
```
- Type content.
- Press `Ctrl + D` to save and exit.

---

## ✍️ vi Editor (Mandatory for DevOps)

### 🔹 Open File
```bash
vi team.txt
```

### 🔹 vi Modes
- **Normal mode** (default)
- **Insert mode** → press `i`
- **Command mode** → press `ESC`

### 🔹 Save & Exit
```bash
:wq!
```
👉 Used to edit:
- Configuration files
- YAML files
- Application & server configs

---

## ⌨️ Keyboard Shortcuts (Speed & Efficiency)

| Shortcut | Description |
|----------|-------------|
| `Ctrl + A` | Move cursor to beginning of line |
| `Ctrl + E` | Move cursor to end of line |
| `Ctrl + U` | Delete before cursor |
| `Ctrl + L` | Clear terminal screen |
| `clear` | Clear terminal |

---

## 🎯 DevOps Best Practice
Linux mastery is about speed, safety, and confidence in production systems.  
These commands are used daily in real DevOps roles.
