// probe 101 -- binary &
function op_101(a, b) {
    return a & b;
}

%PrepareFunctionForOptimization(op_101);
op_101(true, false);
op_101(true, false);
%OptimizeFunctionOnNextCall(op_101);
op_101(true, false);
