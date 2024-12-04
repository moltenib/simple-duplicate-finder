# Simple Duplicate Finder

## Before running this program

This program is intended to find and display files that share one of these features:

- A SHA-1 hash;
- An Adler-32 checksum;
- A modification date, or
- A file name.

Choosing SHA-1 and Adler-32 will open all files in the file system under the chosen directory, altering their access dates, but checking the modification time or file name will only use the file's metadata, which is much faster to retrieve.

- SHA-1 was originally intended as a cryptographic hashing algorithm and is the only method that is almost guaranteed to return a reliable result. It is also the slowest.
- Adler-32 was intended for block parity calculation rather than hashing, and is particularly not reliable for small files.
- A modification date shared by two or more files is no guarantee that the files are the same. For instance, they could have been decompressed at the same time.
- If two files share the name, it means just that. This option does not check for anything else.

## Installation

### Linux

This program will run, provided that all dependencies are installed (e.g. PyGObject), as follows:

```shell
git clone # paste the URL to this repository
cd simple-duplicate-finder/src
./main.pyw
```

### Windows

An [executable](https://github.com/moltenib/simple-duplicate-finder/tree/master/dist) file is included for convenience. It was made with PyInstaller and may take a few seconds to start.
