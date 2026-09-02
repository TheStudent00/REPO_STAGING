// probe 276 -- binary as
function op_276(a, b) {
    return a as b;
}

%PrepareFunctionForOptimization(op_276);
op_276(1.0, 2.0);
op_276(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_276);
op_276(1.0, 2.0);
