# Simple Duplicate Finder

## Introduction

This program can find and display files that share one of these features:

- A SHA-1 hash;
- An Adler-32 checksum;
- A modification date, or
- A file name.

Choosing SHA-1 and Adler-32 will open all files in the file system under the chosen directory, altering their access dates, but checking the modification time or file name will only use a file's metadata, which is much faster to retrieve. Other considerations:

- SHA-1 was originally intended as a cryptographic hashing algorithm and is the only method that should always and only return duplicates. It is also the slowest.
- Adler-32 was made for parity calculation rather than hashing, and is particularly not reliable with small files.
- A modification date shared by two or more files is no guarantee that the files are the same. For instance, they could have been decompressed at the same time.
- If two files share the name, it is all that is meant. This option does not check for anything else.

## Controls

- Double click: opens a file.
- Delete key: deletes a file. By default, there is a confirmation dialog.
- The tree allows multiple selection, with _Shift + click_ or _Ctrl + click._

### Coming soon

- Context menu on right click with the following options:
  - Open the containing directory (with one file only)
  - Rename (id.)
  - Swap file names (with two files only)
  - Delete selected (one to multiple files)
  - Keep the oldest (with two to multiple files)
  - Bulk rename (id.)

## Installation

### Linux

This program will run, provided that all dependencies are installed (e.g. PyGObject), in this way:

```shell
git clone # paste the URL to this repository
cd simple-duplicate-finder/src
make translations # for German, Italian, Spanish and Portuguese
./main.pyw
```

### Windows

An [executable file](https://github.com/moltenib/repo/raw/refs/heads/master/simple-duplicate-finder/dist/simple-duplicate-finder.exe) is included for convenience. It was made with PyInstaller and may take a few seconds to start.

## Notes

This program was meant as a GUI alternative to the Linux or Unix command below, which is actually faster, as a `sort` command is only run once, but the list of files is not shown until it finishes running (unlike the tree view that is updated with each file that is found).

`find . -type f -exec shasum {} \; | sort | uniq -w 40 -D`

A very similar output can be achieved by saving the tree view on this program as a CSV file, with the button on the bottom right.
