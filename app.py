import argparse
import os
import sys
from pandas import DataFrame
from Beat.TempoEstimator import TempoEstimator
from Key.KeyAnalyst import KeyAnalyst
from Library.LibraryHandler import LibraryHandler

class ANSI:
    GREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    END = '\033[0m'

def display_files(files):
    file_df = DataFrame([file.split('.') for file in files], columns=["Filename", "Extension"])
    print(file_df)

def validate(filename: str, handler: LibraryHandler) -> bool:
    return handler.exists_in_library(filename) and handler.validate_file_type(filename)

def display_help():
    print("="*50)
    print("Composer: A Musical Analysis Tool")
    print("="*50)
    print("Usage:")
    print("-k/--key    <file_name.ext>    Perform key estimation.")
    print("-t/--tempo  <file_name.ext>    Perform tempo estimation (BPM).")
    print("-d/--delete <file_name.ext>    Delete an audio file from the library.")
    print("-l/--list                      List all available files in the library.")
    print("-a/--add <path>                Add an audio file to the library.")
    print("-s/--set <path>                Set the audio library path.")
    print("-h/--help                      Display this help message.")
    print("="*50)

def main():
    library_handler = LibraryHandler()
    tempo_estimator = TempoEstimator()
    key_analyst = KeyAnalyst()
    parser = argparse.ArgumentParser(description="Composer - A musical analysis tool.", add_help=False)
    parser.add_argument("-h","--help", action="store_true")
    parser.add_argument("-k", "--key", type=str, metavar="filename")
    parser.add_argument("-t", "--tempo", type=str, metavar="filename")
    parser.add_argument("-l", "--list", action="store_true")
    parser.add_argument("-a", "--add", type=str,  metavar="filepath")
    parser.add_argument("-d", "--delete", type=str,  metavar="filename")
    parser.add_argument("-s", "--set", type=str,  metavar="filepath")

    args = parser.parse_args()

    if args.help:
        display_help()

    if args.list:
        files = library_handler.get_library_contents()
        display_files(files)

    if args.add:
        status = library_handler.add_to_library(args.add)
        if not status:
            print(f'Error adding file to library.', file=sys.stderr)
        else:
            filename = os.path.basename(args.add)
            print(f'Successfully added {filename} to library')

    if args.delete:
        status = library_handler.delete_from_library(args.delete)
        if not status:
            print(f'Error removing file from library.', file=sys.stderr)
        else:
            print(f'Successfully removed {args.delete} from library.')

    if args.tempo:
        if not validate(args.tempo, library_handler):
            print(f'{ANSI.RED}Invalid file.{ANSI.END}')
            raise SystemExit
        path = os.path.join(library_handler.get_library_path(), args.tempo)
        print("Estimating tempo...")
        bpm, _ = tempo_estimator.predict_bpm(path)
        print(f'Tempo: {bpm} BPM.')

    if args.key:
        if not validate(args.key, library_handler):
            print(f'{ANSI.RED}Invalid file.{ANSI.END}')
            raise SystemExit
        path = os.path.join(library_handler.get_library_path(), args.key)
        print("Estimating key...")
        key, confidence = key_analyst.predict_key(path)
        print(f'Key signature: {key}')
        print(ANSI.RED if confidence < 33 else (ANSI.YELLOW if confidence < 66 else ANSI.GREEN),end="")
        print(f'Confidence: {round(confidence)}%{ANSI.END}')

    if args.set:
        status = library_handler.set_library_path(args.set)
        if not status:
            print("Error setting library path.", file=sys.stderr)
        else:
            print(f'Successfully placed library at {args.set}')

if __name__ == "__main__":
    main()