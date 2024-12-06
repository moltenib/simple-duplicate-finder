# Simple Duplicate Finder

## Before running this program

This program can find and display files that share one of these features:

- A SHA-1 hash;
- An Adler-32 checksum;
- A modification date, or
- A file name.

Choosing SHA-1 and Adler-32 will open all files in the file system under the chosen directory, altering their access dates, but checking the modification time or file name will only use the file's metadata, which is much faster to retrieve. Other considerations:

- SHA-1 was originally intended as a cryptographic hashing algorithm and is the only method that should always and only return duplicates. It is also the slowest.
- Adler-32 was made for block parity calculation rather than hashing, and is particularly not reliable with small files.
- A modification date shared by two or more files is no guarantee that the files are the same. For instance, they could have been decompressed at the same time.
- If two files share the name, it is all that is meant. This option does not check for anything else.

## Installation

### Linux

This program will run, provided that all dependencies are installed (e.g. PyGObject), as follows:

```shell
git clone # paste the URL to this repository
cd simple-duplicate-finder/src
./main.pyw
```

### Windows

An [executable file](https://github.com/moltenib/simple-duplicate-finder/raw/refs/heads/master/dist/simple-duplicate-finder.exe) is included for convenience. It was made with PyInstaller and may take a few seconds to start.

## Notes

This program was meant as a replacement for the Linux or Unix command below, which is actually faster, as the `sort` command is only run once, but the list of files is not shown until it finishes running.

`find . -type f -exec shasum {} \; | sort | uniq -w 32`

A very similar output can be achieved by exporting the tree view on this program as a CSV file, with the bottom-right button.
