// probe 90 -- binary <<
function op_90(a, b) {
    return a << b;
}

%PrepareFunctionForOptimization(op_90);
op_90(true, 2.0);
op_90(true, 2.0);
%OptimizeFunctionOnNextCall(op_90);
op_90(true, 2.0);
