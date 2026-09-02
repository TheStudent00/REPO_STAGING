// probe 84 -- binary <<
function op_84(a, b) {
    return a << b;
}

%PrepareFunctionForOptimization(op_84);
op_84(1.0, 2.0);
op_84(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_84);
op_84(1.0, 2.0);
