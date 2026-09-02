// probe 98 -- binary &
function op_98(a, b) {
    return a & b;
}

%PrepareFunctionForOptimization(op_98);
op_98(1.0, false);
op_98(1.0, false);
%OptimizeFunctionOnNextCall(op_98);
op_98(1.0, false);
