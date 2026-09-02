// probe 2 -- unary !
function op_2(a) {
    return !a;
}

%PrepareFunctionForOptimization(op_2);
op_2(true);
op_2(true);
%OptimizeFunctionOnNextCall(op_2);
op_2(true);
