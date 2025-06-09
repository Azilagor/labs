from parser import parser
from interpreter import interpret
from robot import Robot, FIELD


def main():
    with open("program.txt") as f:
        code = f.read()
    result = parser.parse(code)
    print("Parse tree (AST):")
    print(result)
    print("\n--- Program output ---")


    robot = Robot(FIELD, x=0, y=1)
    print(f"Start: {robot}")
    print("\n--- Program output ---")
    interpret(result, robot)
    print("\nFinish: " + str(robot))

if __name__ == '__main__':
    main()
