# Day 7 (Part 2): ðŸ§ Linux Fundamentals

> Trainer: 20+ Years Experienced DevOps Engineer  
> Focus: Real-world usage, production mindset, strong fundamentals

---

## ðŸ“Œ Directory Management Commands

### ðŸ”¹ `mkdir -p` (Create Parent Directories)
```bash
mkdir -p abc/xyz/123
```
- `-p` â†’ Parent option.
- Creates all missing parent directories automatically.
- Used in production to create application, logs, and deployment folders.

### ðŸ”¹ `rmdir` (Remove Empty Directory)
```bash
rmdir india/
```
- Removes directory only if empty.
- Rarely used in DevOps due to limitation.

### ðŸ”¹ `rm -r` (Recursive Delete)
```bash
rm -r india/
```
- Deletes directory and its contents recursively.
- Use carefully in servers.

### ðŸ”¹ `rm -rf` (Force Recursive Delete âš ï¸)
```bash
rm -rf india/
```
- `-r` â†’ recursive
- `-f` â†’ force delete (no confirmation)
- Commonly used in automation & cleanup scripts.
- âš ï¸ **Dangerous in production if misused.**

---

## ðŸ“„ File Management Commands

### ðŸ”¹ `touch` (Create Empty File)
```bash
touch 123.txt
```
- Creates an empty file.
- Updates timestamp if file already exists.

### ðŸ”¹ `rm` (Delete File)
```bash
rm 123.txt
```
- Permanently deletes file.

### ðŸ”¹ `stat` (File Metadata â€“ Very Important)
```bash
stat 123.txt
```
Displays:
- File size
- Permissions
- Created time
- Accessed time
- Modified time

ðŸ‘‰ *Used in debugging, auditing, and production issue analysis.*

---

## ðŸ“‚ Listing Files and Directories (`ls`)

### ðŸ”¹ Basic Listing
```bash
ls
```

### ðŸ”¹ Long Listing
```bash
ls -l
```
- Shows permissions, owner, size, and timestamp.

### ðŸ”¹ Hidden Files
```bash
ls -a
ls -all
```
- Displays hidden files like `.git`, `.env`, `.bashrc`.
- Important for DevOps configurations.

### ðŸ”¹ Sorting Files
```bash
ls -lt    # Latest files first
ls -ltr   # Oldest files first
```

### ðŸ”¹ File Size (Human Readable)
```bash
ls -lh
```
- Displays sizes in KB, MB, GB.

### ðŸ”¹ One File Per Line
```bash
ls -1
```

### ðŸ”¹ Shortcut
```bash
ll
```
- Alias for `ls -l` (available on most Linux servers).

---

## ðŸ“œ Command History (Productivity Booster)

### ðŸ”¹ View Command History
```bash
history
```

### ðŸ”¹ Re-execute Commands
```bash
!!      # Run previous command
!582    # Run command number 582
!-13    # Run 13th command from bottom
```
ðŸ‘‰ *Heavily used by senior DevOps engineers.*

---

## ðŸ“ Navigation Commands

### ðŸ”¹ Present Working Directory
```bash
pwd
```

### ðŸ”¹ Change Directory
```bash
cd ../..
```
- Moves two levels up.

---

## ðŸ“– Viewing & Creating File Content

### ðŸ”¹ View File Content
```bash
cat 123.txt
```

### ðŸ”¹ Create File with Content
```bash
cat > 456.txt
```
- Type content.
- Press `Ctrl + D` to save and exit.

---

## âœï¸ vi Editor (Mandatory for DevOps)

### ðŸ”¹ Open File
```bash
vi team.txt
```

### ðŸ”¹ vi Modes
- **Normal mode** (default)
- **Insert mode** â†’ press `i`
- **Command mode** â†’ press `ESC`

### ðŸ”¹ Save & Exit
```bash
:wq!
```
ðŸ‘‰ Used to edit:
- Configuration files
- YAML files
- Application & server configs

---

## âŒ¨ï¸ Keyboard Shortcuts (Speed & Efficiency)

| Shortcut | Description |
|----------|-------------|
| `Ctrl + A` | Move cursor to beginning of line |
| `Ctrl + E` | Move cursor to end of line |
| `Ctrl + U` | Delete before cursor |
| `Ctrl + L` | Clear terminal screen |
| `clear` | Clear terminal |

---

## ðŸŽ¯ DevOps Best Practice
Linux mastery is about speed, safety, and confidence in production systems.  
These commands are used daily in real DevOps roles.

---
**[⬅️ Previous: Day 7 (Part 1) - Linux Foundations](./Day-07-Part-1-Linux-Foundations.md)** | **[➡️ Next: Day 7 (Part 3) - Linux Commands](./Day-07-Part-3-Linux-Commands.md)**

