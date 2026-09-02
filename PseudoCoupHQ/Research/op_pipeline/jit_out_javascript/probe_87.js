// probe 87 -- binary <<
function op_87(a, b) {
    return a << b;
}

%PrepareFunctionForOptimization(op_87);
op_87(1.0, 2.0);
op_87(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_87);
op_87(1.0, 2.0);
