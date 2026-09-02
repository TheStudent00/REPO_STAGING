// probe 89 -- binary <<
function op_89(a, b) {
    return a << b;
}

%PrepareFunctionForOptimization(op_89);
op_89(1.0, false);
op_89(1.0, false);
%OptimizeFunctionOnNextCall(op_89);
op_89(1.0, false);
