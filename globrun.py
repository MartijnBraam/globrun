#!/usr/bin/env python3
import argparse
import glob
import os
import subprocess
from datetime import timedelta
import time
import statistics
from pathlib import Path

parser = argparse.ArgumentParser(description="Glob and run all in one! the replacement for find|xargs")

parser.add_argument('--preview', '--dry-run', help="Don't execute the commands, only print", action="store_true",
                    default=False)
parser.add_argument('--verbose', '-v', help="Give more output while running", action="store_true", default=False)
parser.add_argument('--failfast', help="Fail if one started process exits with a failure")
parser.add_argument('expression', help="A simple glob expression")
parser.add_argument('command', help="The command to run", nargs=argparse.REMAINDER)

args = parser.parse_args()
expression = args.expression
commmand = " ".join(args.command)

if args.verbose:
    print("Glob expression: {}".format(expression))
    print("Command template: {}".format(commmand))
    if args.preview:
        print("Running in preview/dry-run mode")
    print()

success = 0
fail = 0
total = 0
times = []

for file in glob.glob(expression, recursive=True):
    directory = os.path.dirname(file)
    filename = os.path.basename(file)
    parts = file.split('.')
    name = ".".join(parts[:-1])
    ext = parts[-1]
    path = Path(file)

    generated_command = commmand.format(file=file, name=name, dir=directory, filename=filename, ext=ext, path=path)

    if args.verbose:
        print("-----")
        print("Matched file: {}".format(file))
        print("Generated command: {}".format(generated_command))
    else:
        print(file)
    total += 1

    if not args.preview:
        time_start = time.time()
        result = subprocess.run(generated_command, shell=True)
        if result.returncode == 0:
            success += 1
            if args.verbose:
                print("Command exited successfully")
        else:
            fail += 1
            print("Command failed! exit status: {}".format(result.returncode))
            if args.failfast:
                print("Exiting early because of --failfast")
                exit(1)
        time_end = time.time()
        times.append(time_end - time_start)

print('------')
print()
if args.preview:
    print("The command will be executed {} times.".format(total))
else:
    print("Batch completed")
    print("  Success: {}".format(success))
    print("  Failed:  {}".format(fail))

    mean_seconds = statistics.mean(times)
    standard_deviation = statistics.stdev(times)
    print("  Mean execution time: {}".format(timedelta(seconds=mean_seconds)))
    print("  Standard deviation:  {}".format(timedelta(seconds=standard_deviation)))
    print("  Min/Max time:        {} / {}".format(timedelta(seconds=min(times)), timedelta(seconds=max(times))))
