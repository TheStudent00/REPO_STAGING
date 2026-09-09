def machine_op_0(args):
    return ...

def machine_op_1(args):
    return ...

def machine_op_2(args):
    return ...
    
def machine_op_3(args):
    return ...

def func_0 -> int (a_0: int, b_0: int):
	a_1 = machine_op_0(a_0)
	a_2 = machine_op_1(a_1)
	b_1 = machine_op_2(b_0)
	ret = machine_op_3(a_2, a_1, a_0, b_1, b_0)
	return ret
	
def func_1 -> int (a_0: int, b_0: int):
	a_1 = machine_op_0(a_0)
	a_2 = machine_op_1(a_1)
	b_1 = machine_op_2(b_0)
	ret = machine_op_3(a_2, a_1, b_1)
	return ret
