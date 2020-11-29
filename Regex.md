## Capture groups `()`

Regex: ```Hello (\d+) bob```  will match ```1234``` for Text: ```Hello 1234 bob```

## Character Classes `[]`

To check for a group of characters, as a single character, then use `[]`, e.g.

`Jo[ha]n` will match either `Joan` or `John`

`Hello (Jo[ha]n), how are you` will match `Joan` for `Hello Joan, how are you`

## Non-capturing group `(?:)`

Similar to character classes, but used to group a bunch of letters / character classes into a group.

e.g. `(?:H[ae]l+o) (.+) how are you` will match `Bob` for both:
  - Halo Bob how are you
  - Hello Bob how are you
  
#### When its useful
  
Useful when character classes aren't good enough, or you can't include in character class.

`[^a-zA-Z]([0-9]+)s(?:[^a-zA-Z]|$)`, the end matches either a non- alpha letter OR the end of line.

e.g. capture the numbers `15`

- `Google AU: Dogue 15s`
- `Bobs House 15s`

