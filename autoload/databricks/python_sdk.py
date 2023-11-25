
import argparse

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--code')
    args = parser.parse_args()

    print(args.code)

if __name__ == "__main__":
    main()
