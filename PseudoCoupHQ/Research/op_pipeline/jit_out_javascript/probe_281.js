// probe 281 -- binary as
function op_281(a, b) {
    return a as b;
}

%PrepareFunctionForOptimization(op_281);
op_281(true, false);
op_281(true, false);
%OptimizeFunctionOnNextCall(op_281);
op_281(true, false);
