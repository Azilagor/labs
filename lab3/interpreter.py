from robot import Robot


def interpret(ast, robot):
    prog_type, functions = ast
    for func in functions:
        name, param, body = func[1], func[2], func[3]
        if name == "main":
            run_block(body, {}, robot)

def run_block(statements, env, robot):
    for stmt in statements:
        if stmt[0] == 'var_assign':
            var, value = stmt[1], stmt[2]
            env[var] = value
            print(f"Create variable {var} = {value}")
        elif stmt[0] == 'assign':
            var, value = stmt[1], stmt[2]
            if var in env:
                env[var] = value
                print(f"Set {var} = {value}")
            else:
                print(f"Variable {var} not declared, auto-create {var} = {value}")
                env[var] = value
        elif stmt[0] == 'forward':
            steps = stmt[1]
            robot.move_forward(steps)
        else:
            print(f"Unknown statement: {stmt}")
