# cli.py
from analyzer import analyze
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("password", nargs="?", help="Password to analyze")
parser.add_argument("--json", action="store_true", help="Output JSON")
args = parser.parse_args()

pw = args.password or input("Enter password: ")
result = analyze(pw)

if args.json:
    print(json.dumps(result, indent=2))
else:
    print(f"Password: {result['password']}")
    print(f"Entropy (bits): {result['entropy_bits']}")
    print(f"Score: {result['score']} / 100  ({result['category']})")
    if result['suggestions']:
        print("Suggestions:")
        for s in result['suggestions']:
            print(" -", s)
