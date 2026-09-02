// probe 278 -- binary as
function op_278(a, b) {
    return a as b;
}

%PrepareFunctionForOptimization(op_278);
op_278(1.0, false);
op_278(1.0, false);
%OptimizeFunctionOnNextCall(op_278);
op_278(1.0, false);
