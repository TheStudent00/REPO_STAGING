// probe 105 -- binary ^
function op_105(a, b) {
    return a ^ b;
}

%PrepareFunctionForOptimization(op_105);
op_105(1.0, 2.0);
op_105(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_105);
op_105(1.0, 2.0);
