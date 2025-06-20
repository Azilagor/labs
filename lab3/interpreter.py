from robot import Robot

def interpret(ast, robot):
    prog_type, functions = ast
    func_map = {f[1]: f for f in functions}
    call_stack = []
    # Для main — передаем 0 как параметр
    call_function('main', 0, func_map, call_stack, robot)

def call_function(name, arg, func_map, call_stack, robot):
    func = func_map[name]
    _, _, param_name, body = func
    env = {param_name: arg}
    call_stack.append(env)
    result = run_block(body, env, robot, func_map, call_stack)
    call_stack.pop()
    return result

def run_block(statements, env, robot, func_map, call_stack):
    idx = 0
    while idx < len(statements):
        stmt = statements[idx]
        if stmt[0] == 'var_decl':
            var = stmt[1]
            if len(stmt) == 2:
                env[var] = None
                print(f"Create variable {var} (scalar)")
            else:
                size = stmt[2]
                env[var] = [None] * size
                print(f"Create array {var} of size {size}")
        elif stmt[0] == 'assign':
            var, value_expr = stmt[1], stmt[2]
            value = eval_expr(value_expr, env, func_map, call_stack, robot)
            env[var] = value
            print(f"Set {var} = {value}")
        elif stmt[0] == 'assign_index':
            var, idx_expr, value_expr = stmt[1], stmt[2], stmt[3]
            arr = env.get(var, [])
            idx_val = eval_expr(idx_expr, env, func_map, call_stack, robot)
            value = eval_expr(value_expr, env, func_map, call_stack, robot)
            if not isinstance(arr, list):
                arr = []
            while len(arr) <= idx_val:
                arr.append(None)
            arr[idx_val] = value
            env[var] = arr
            print(f"Set {var}({idx_val}) = {value}")
        elif stmt[0] == 'forward':
            steps = eval_expr(stmt[1], env, func_map, call_stack, robot)
            robot.move_forward(steps)
        elif stmt[0] == 'backward':
            steps = eval_expr(stmt[1], env, func_map, call_stack, robot)
            robot.move_backward(steps)
        elif stmt[0] == 'if':
            cond = stmt[1]
            if_block = stmt[2]
            else_chain = stmt[3]  
            # основная ветка
            if eval_condition(cond, env, func_map, call_stack, robot):
                result = run_block(if_block, env, robot, func_map, call_stack)
                if result is not None:
                    return result
            else:
                for branch in else_chain:
                    if branch[0] == 'elif':
                        branch_cond = branch[1]
                        branch_block = branch[2]
                        if eval_condition(branch_cond, env, func_map, call_stack, robot):
                            result = run_block(branch_block, env, robot, func_map, call_stack)
                            if result is not None:
                                return result
                            break
                    elif branch[0] == 'else':
                        branch_block = branch[1]
                        result = run_block(branch_block, env, robot, func_map, call_stack)
                        if result is not None:
                            return result
                        break
        elif stmt[0] == 'while':
            cond = stmt[1]
            body = stmt[2]
            finish_block = stmt[3]
            while True:
                res = eval_condition(cond, env, func_map, call_stack, robot)
                if res is True:
                    run_block(body, env, robot, func_map, call_stack)
                elif res is False:
                    if finish_block:
                        run_block(finish_block, env, robot, func_map, call_stack)
                    break
                else:
                    break
        elif stmt[0] == 'call':
            func_name = stmt[1]
            arg_val = eval_expr(stmt[2], env, func_map, call_stack, robot)
            call_function(func_name, arg_val, func_map, call_stack, robot)
        elif stmt[0] == 'return':
            value = None
            if stmt[1] is not None:
                value = eval_expr(stmt[1], env, func_map, call_stack, robot)
            return value
        else:
            print(f"Unknown statement: {stmt}")
        idx += 1
    return None

def eval_condition(cond, env, func_map, call_stack, robot):
    if cond[0] == 'lt':
        return eval_expr(cond[1], env, func_map, call_stack, robot) < eval_expr(cond[2], env, func_map, call_stack, robot)
    if cond[0] == 'gt':
        return eval_expr(cond[1], env, func_map, call_stack, robot) > eval_expr(cond[2], env, func_map, call_stack, robot)
    if cond[0] == 'eq':
        return eval_expr(cond[1], env, func_map, call_stack, robot) == eval_expr(cond[2], env, func_map, call_stack, robot)
    return False

def eval_expr(expr, env, func_map=None, call_stack=None, robot=None):
    if isinstance(expr, tuple):
        op = expr[0]
        if op == 'var_ref':
            var = expr[1]
            return env.get(var, 'UNDEF')
        elif op == 'var_ref_index':
            var, idx_expr = expr[1], expr[2]
            idx = eval_expr(idx_expr, env, func_map, call_stack, robot)
            arr = env.get(var, [])
            if not isinstance(arr, list):
                return 'UNDEF'
            try:
                return arr[idx]
            except (IndexError, TypeError):
                return 'UNDEF'
        elif op == 'plus':
            return eval_expr(expr[1], env, func_map, call_stack, robot) + eval_expr(expr[2], env, func_map, call_stack, robot)
        elif op == 'minus':
            return eval_expr(expr[1], env, func_map, call_stack, robot) - eval_expr(expr[2], env, func_map, call_stack, robot)
        elif op == 'uminus':
            return -eval_expr(expr[1], env, func_map, call_stack, robot)
        elif op == 'xor':
            return int(bool(eval_expr(expr[1], env, func_map, call_stack, robot))) ^ int(bool(eval_expr(expr[2], env, func_map, call_stack, robot)))
        elif op == 'sum':
            var = expr[1]
            arr = env.get(var, [])
            if not isinstance(arr, list):
                return 'UNDEF'
            return sum(x if isinstance(x, (int, float)) and x is not None else 0 for x in arr)
        elif op == 'mul':
            return eval_expr(expr[1], env, func_map, call_stack, robot) * eval_expr(expr[2], env, func_map, call_stack, robot)
        elif op == 'div':
            return eval_expr(expr[1], env, func_map, call_stack, robot) // eval_expr(expr[2], env, func_map, call_stack, robot)
        elif op == 'lt':
            return eval_expr(expr[1], env, func_map, call_stack, robot) < eval_expr(expr[2], env, func_map, call_stack, robot)
        elif op == 'gt':
            return eval_expr(expr[1], env, func_map, call_stack, robot) > eval_expr(expr[2], env, func_map, call_stack, robot)
        elif op == 'eq':
            return eval_expr(expr[1], env, func_map, call_stack, robot) == eval_expr(expr[2], env, func_map, call_stack, robot)
        elif op == 'call_expr':
            func_name = expr[1]
            arg_val = eval_expr(expr[2], env, func_map, call_stack, robot)
            return call_function(func_name, arg_val, func_map, call_stack, robot)
        else:
            print(f"Unknown expression node: {expr}")
            return 'UNDEF'
    else:
        return expr

