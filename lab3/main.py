from parser import parser
from interpreter import interpret
from robot import Robot, FIELD
import pprint


def main():
    with open("program.txt") as f:
        code = f.read()
    result = parser.parse(code)
    print("Parse tree (AST):")
    pprint.pprint(result, width=120, compact=False)
    print("\n--- Program output ---")


    robot = Robot(FIELD, x=0, y=1)
    print(f"Start: {robot}")
    print("\n--- Program output ---")
    if result is None:
        print("Parsing failed due to syntax error. Exiting.")
        exit()
    interpret(result, robot)
    print("\nFinish: " + str(robot))

if __name__ == '__main__':
    main()
