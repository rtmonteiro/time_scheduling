from scheduling.reader.reader import read_file
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        return
    file_path = sys.argv[1]
    schedule = read_file(file_path)
    print(schedule)


if __name__ == "__main__":
    main()
