# Doku2MD - DokuWiki to MarkDown Converter

## About

I wrote this utility to help me migrate my DokuWiki content to MarkDown.

## Supported patterns

Best way to see what's supported and how is to look at [syntax.md](syntax.md), which is the official [DokuWiki Syntax](https://www.dokuwiki.org/wiki:syntax) file converted to MarkDown using this utility.

### The following elements are fully supported

- Headers (all levels)
- Italic
- Bold
- Monospaced
- Strikethrough
- Code Blocks
- Lists
- Line breaks (make sure your editor doesn't trim white spaces)
- Removal of excess space character (2+ are left in place for MD newline)
- Removal of excess `\n` characters (to be more compliant with MarkDown)

### Partially supported

- Links (only basic internal/external formats such as `[[https://example.com|Example]]` and `[[https://example.com]]`
- Underline (MarkDown doesn't have underline format so I chose bold instead)
- Images (mostly untested)
- Tables - only basic tables without colspan/rowspan
- Footnotes (not well tested, just basic `[^1]`)

### Unsupported

- Everything not listed above

## Usage

1. Requires Python 3 (tested on Py 3.11 but it should work ok on older releases too)
2. Obtain all `.txt` from your DokuWiki web directory (typically in `pages` subdir)
3. Run `doku2md` to convert either one file or all TXT files in a directory structure 

```bash
# Single file
./doku2md.py -f your_text_file.txt

# All files in pages/
./doku2md.py -d dokuwiki/pages
```

### More options

```text
 ./doku2md.py -h
usage: doku2md.py [-h] (-f FILE | -d DIRECTORY) [-l LANG] [-T]

Convert Dokuwiki to Markdown.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File to convert.
  -d DIRECTORY, --directory DIRECTORY
                        Directory of files to convert.
  -l LANG, --lang LANG  Codeblocks will be labeled with this Language (eg. shell).
  -T, --timestamps      Keep textual timestamps in documents. (Default is to remove timestamps)
```

**--lang**

Creates code blocks typed with a shell of your choice.
Eg.  

````text
```bash  
cd /home  
```
````

## Contributions

- Contributions are welcome
- Please update unit testing as necessary
- Don't modify `syntax.txt` file
- As a part of your submission, regenerate `syntax.md` using `./doku2md.py -f syntax.txt`
