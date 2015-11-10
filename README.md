# Globrun

This is a small python script to do the most common usecase (for me) of `find | xargs`: Simple glob search and execute
a command useing a placeholder and 1 file per execution.

The minimal python version for this tool is 3.5 since I use a few of the new methods that
break backward compatability (Hey this is a project for fun!).

## Installation

Clone this git repository to your favorite location for such repositories (/opt in my example) and add a shell alias to prevent globbing.

```bash
# make the script executable
chmod +x /opt/globrun/globrun.py

# zsh
alias globrun="noglob /opt/globrun/globrun.py"

# bash/sh/ksh
alias globrun='set -f;globrun';globrun(){ /opt/globrun/globrun.py "$@";set +f;}
```

Please note that this script depends on Python 3.5 or higher

## Usage

The commandline is:

```bash
globrun --preview --verbose --failfast expression -- command-template
```

**--preview/--dry-run**  
Don't execute the commands, only run the file search and preview the commands that would be executed

**--verbose**  
By default this tool only displays the generated command and the command output. If this flag is set you will get:

- The matched filename
- The generated command based on your template
- Display the exit code also when commands succeed
- Your expression and command template after it has passed through your shell escaping

**--failfast**  
Exit as soon as one of the commands fails.

**expression**  
The glob pattern to find the files. This uses the python3.5 glob.glob(recursive=True) syntax:

`*` match everything  
`?` match a single character  
`[abc]` match a character that is a, b or c  
`[1-5]` matches 1,2,3,4 or 5  
`[!abc]` match a character that is not a,b or c

It is also possible to use `**` for recursion like `zsh` and `fish` do. If you use `*` then every file in the directory
will be matched. If you use `**/*` then every file in the directory and subdirectories will be matched.

If your glob pattern ends with `/` then you will match directories instead of files.

**command**  
This is the command template that will be used. This is passed through the `string.format` function in python so you can use
everything in the [Format Specification Mini-Language](https://docs.python.org/3.5/library/string.html#format-specification-mini-language)

The variables that you can use:

- `{file}` The file path and name: `dir1/dir2/filename.txt`
- `{name}` The file path without extension: `dir1/dir2/filename`
- `{ext}` The file extension without dot: `txt`
- `{filename}` The file name with extension: `filename.txt`
- `{dir}` The directory containing the file: `dir1/dir2`
- `{path}` An instance of [pathlib.Path](https://docs.python.org/3/library/pathlib.html) from the `{file}`

## Output summary

One of the nice features of this script is that it generates a summary after completing the batch. For example the summary after converting
some music with `ffmpeg`:

```
Batch completed
  Success: 4
  Failed:  1
  Mean execution time: 0:00:05.368356
  Standard deviation:  0:00:02.999654
  Min/Max time:        0:00:00.037264 / 0:00:07.270456
```

And without failures:

```
Batch completed
  Success: 5
  Failed:  0
  Mean execution time: 0:00:06.912867
  Standard deviation:  0:00:00.740558
  Min/Max time:        0:00:06.384255 / 0:00:08.013860
```

## Examples

The obligatory echo example:

```
$ globrun * -- echo {name}
```

Listing all directories:

```
$ globrun */**/ -- echo {file}
```

Convert some files with ffmpeg (The reason I build this tool).

```
$ globrun --failfast */**/*.wav -- ffmpeg -i "{file}" -ab 320k "{name}.mp3"
```

Examples demonstrating the path variable

```bash
$ globrun * -- echo {path.name} # Prints the filename without directory
$ globrun * -- echo {path.parents[0]} # Prints a/b/c for a/b/c/d.txt
$ globrun * -- echo {path.parents[1]} # Prints a/b for a/b/c/d.txt
```
