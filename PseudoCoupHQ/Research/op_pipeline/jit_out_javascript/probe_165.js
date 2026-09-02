// probe 165 -- binary **
function op_165(a, b) {
    return a ** b;
}

%PrepareFunctionForOptimization(op_165);
op_165(1.0, 2.0);
op_165(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_165);
op_165(1.0, 2.0);
