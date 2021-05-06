# Bash commands

## Outputing text to file
- using `tee` allows multiline text to be output cleanly
```bash
# Rather than using 
echo "Hello Bob" >> file1.txt

# do 
tee file1.yaml <<END
git:
  file: "name"
person1:
  name: bob
  age: 49
END
# it outputs both to stdout & to a file
```
