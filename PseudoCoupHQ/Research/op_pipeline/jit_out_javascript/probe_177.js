// probe 177 -- binary <
function op_177(a, b) {
    return a < b;
}

%PrepareFunctionForOptimization(op_177);
op_177(1.0, 2.0);
op_177(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_177);
op_177(1.0, 2.0);
