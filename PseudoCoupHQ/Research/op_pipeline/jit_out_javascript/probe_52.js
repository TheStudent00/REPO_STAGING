// probe 52 -- binary &&
function op_52(a, b) {
    return a && b;
}

%PrepareFunctionForOptimization(op_52);
op_52(1.0, 2.0);
op_52(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_52);
op_52(1.0, 2.0);
