
import sys
from schema import parser as schema_parser


if __name__ == '__main__':
    stdin_content = sys.stdin.read()

    result = schema_parser.parse(stdin_content)

