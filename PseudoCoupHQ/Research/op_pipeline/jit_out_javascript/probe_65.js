// probe 65 -- binary ||
function op_65(a, b) {
    return a || b;
}

%PrepareFunctionForOptimization(op_65);
op_65(true, false);
op_65(true, false);
%OptimizeFunctionOnNextCall(op_65);
op_65(true, false);
