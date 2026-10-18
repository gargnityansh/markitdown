# markitdown
Convert any file to .md

## Usage

Convert one or more files:

```bash
python markitdown.py /path/to/file
```

Convert all files in a directory recursively:

```bash
python markitdown.py /path/to/directory
```

This creates a Markdown file next to each input file using `<original-name>.md`.

## Pull request automation

When files are added or updated in a pull request, the repository workflow automatically runs `markitdown.py` on the changed files and commits the generated `.md` files back to the same PR branch.
