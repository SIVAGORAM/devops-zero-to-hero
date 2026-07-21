# Shell Scripting Cheat Sheet

A quick-reference guide for Bash Shell Scripting concepts covered in DevOps Day 8 and Day 9.

## 1. Basic Structure
```bash
#!/bin/bash
# This is a comment
echo "Hello, World!"
```

## 2. Variables
```bash
# Declaration (NO spaces around =)
NAME="Siva"
AGE=25

# Usage
echo "My name is $NAME and I am $AGE years old."
```

## 3. Command Substitution
```bash
# Save output of a command to a variable
CURRENT_DATE=$(date)
echo "Today is $CURRENT_DATE"
```

## 4. Conditional Statements (`if/elif/else`)
```bash
a=10
b=20

# Number comparison: -eq, -ne, -lt, -le, -gt, -ge
if [ $a -gt $b ]; then
    echo "A is greater"
elif [ $a -eq $b ]; then
    echo "They are equal"
else
    echo "B is greater"
fi

# String comparison: ==, !=, -z (empty string)
if [ "$NAME" == "Siva" ]; then
    echo "Match!"
fi
```

## 5. Loops
### `for` loop
```bash
# Range
for i in {1..5}; do
    echo "Number: $i"
done

# Loop through files
for file in *.txt; do
    echo "Processing $file"
done
```

## 6. Debugging & Safety Flags
```bash
set -x          # Enable debug mode (prints commands as they execute)
set -e          # Exit script immediately if a command fails
set -o pipefail # Entire pipeline fails if any command in the pipeline fails
```

## 7. Command Line Arguments
```bash
$0   # Name of the script
$1   # First argument
$2   # Second argument
$@   # All arguments as a single string
$#   # Number of arguments passed
```

## 8. Process & Text Filtering
```bash
ps -ef | grep "nginx"              # Find specific running processes
awk -F" " '{print $2}' file.txt    # Print the 2nd column of a file
df -h                              # Disk space
free -g                            # RAM usage
```

## 9. File I/O Redirection
```bash
> output.log   # Overwrites file
>> output.log  # Appends to file
```

## 10. Traps (Signal Handling)
```bash
# Execute cleanup command before exit on Ctrl+C (SIGINT)
trap 'echo "Cleaning up..."; rm -rf /tmp/tempfiles' SIGINT
```
