// probe 88 -- binary <<
function op_88(a, b) {
    return a << b;
}

%PrepareFunctionForOptimization(op_88);
op_88(1.0, 2.0);
op_88(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_88);
op_88(1.0, 2.0);
