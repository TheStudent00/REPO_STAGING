// probe 191 -- binary <=
function op_191(a, b) {
    return a <= b;
}

%PrepareFunctionForOptimization(op_191);
op_191(true, false);
op_191(true, false);
%OptimizeFunctionOnNextCall(op_191);
op_191(true, false);
