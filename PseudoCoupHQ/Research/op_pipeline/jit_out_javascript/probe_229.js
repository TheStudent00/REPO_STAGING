// probe 229 -- binary >=
function op_229(a, b) {
    return a >= b;
}

%PrepareFunctionForOptimization(op_229);
op_229(1.0, 2.0);
op_229(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_229);
op_229(1.0, 2.0);
