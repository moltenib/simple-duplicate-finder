# Simple Duplicate Finder

## Introduction

This program can find and display files that share one of these features:

- A SHA-1 hash;
- An Adler-32 checksum;
- A modification date, or
- A file name.

Choosing SHA-1 and Adler-32 will open all files in the file system under the chosen directory, altering their access dates, but checking the modification time or file name will only use a file's metadata, which is much faster to retrieve. Other considerations:

- SHA-1 was originally intended as a cryptographic hashing algorithm and is the only method that should always and only return duplicates. It is also the slowest of all methods.
- Adler-32 was made for data compression rather than hashing, and it is particularly not reliable with small files.
- A modification date shared by two or more files is no guarantee that the files are the same. For instance, they could have been decompressed at the same time.
- If two files share the name, it is all that is meant. This option does not check for anything else.

## Controls

- Double click: opens a file.
- Delete key: deletes a file. By default, there is a confirmation dialog.
- The tree allows multiple selection, with _Shift + click_ or _Ctrl + click._

### Coming soon

- Context menu on right click with the options:
  - _Open the containing directory_ (with one file only);
  - _Rename_ (id.);
  - _Swap file names_ (with two files only);
  - _Move..._ (one to multiple files);
  - _Delete selected_ (one to multiple files);
  - _Keep the oldest_ (with two to multiple files),
  - _Bulk rename..._ (id.)

## Installation

### Linux

This program will run, provided that all dependencies are installed (e.g. PyGObject), in this way:

```shell
git clone # paste the URL to this repository
cd simple-duplicate-finder
make translations # for German, Italian, Spanish and Portuguese
src/main.pyw
```

####### Arch Linux
The latest Git version can be installed with the AUR package `simple-duplicate-finder-git`.

### Windows

An [executable file](https://github.com/moltenib/repo/raw/refs/heads/master/dist/simple-duplicate-finder.exe) is included for convenience. It was made with PyInstaller and may take a few seconds to start.

## Notes

This program was meant as a GUI alternative to the Unix command below, which is actually faster, as a `sort` command is only run once, but the list of files is not shown until it finishes running (unlike the tree view that is updated with each file that is found).

`find . -type f -exec shasum {} \; | sort | uniq -w 40 -D`

A very similar output can be achieved by saving the tree view on this program as a CSV file, with the button on the bottom right.
