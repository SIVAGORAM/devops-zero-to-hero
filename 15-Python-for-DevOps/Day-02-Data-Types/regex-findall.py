import re

text = "The quick brown fox jumps over the lazy brown dog"
pattern = r"brown"

# Find all occurrences of the pattern
result = re.findall(pattern, text)
print("Findall result:", result)
