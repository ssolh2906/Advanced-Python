# Advanced-Python

## 01 Parsing
Regex 
<details>
<summary>Regex wild cards</summary>

| Character | Name              | What it matches                        |
|:----------|:------------------|:---------------------------------------|
| `.`       | **Dot**           | Any single character except a newline. |
| `*`       | **Star**          | 0 or more of the previous character.   |
| `+`       | **Plus**          | 1 or more of the previous character.   |
| `?`       | **Question Mark** | 0 or 1 of the previous character.      |
| `\d`      | **Digit**         | Any number (0-9).                      |
| `\w`      | **Word**          | Letters, numbers, and underscores.     |
| `\s`      | **Whitespace**    | Spaces, tabs, and line breaks.         |
| `^`       | **Caret**         | Beginning of a string.                 |
| `$`       | **Dollar**        | End of a string.                       |
</details>

## 02 comprehensions, lambda
Comprehension
```
nulist = [expression(i) for i in oldlist if filter(i)]
```
Lambda as a key
```
sorted_list = sorted(old_list, key=lambda x: x.attribute)
```



