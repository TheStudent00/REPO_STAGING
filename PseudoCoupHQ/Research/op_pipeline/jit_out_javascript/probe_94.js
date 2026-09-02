// probe 94 -- binary &
function op_94(a, b) {
    return a & b;
}

%PrepareFunctionForOptimization(op_94);
op_94(1.0, 2.0);
op_94(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_94);
op_94(1.0, 2.0);
