// probe 279 -- binary as
function op_279(a, b) {
    return a as b;
}

%PrepareFunctionForOptimization(op_279);
op_279(true, 2.0);
op_279(true, 2.0);
%OptimizeFunctionOnNextCall(op_279);
op_279(true, 2.0);
