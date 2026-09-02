// probe 47 -- unary !
function op_47(a) {
    return a!;
}

%PrepareFunctionForOptimization(op_47);
op_47(true);
op_47(true);
%OptimizeFunctionOnNextCall(op_47);
op_47(true);
