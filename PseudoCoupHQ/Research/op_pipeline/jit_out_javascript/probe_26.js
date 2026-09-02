// probe 26 -- unary --
function op_26(a) {
    return --a;
}

%PrepareFunctionForOptimization(op_26);
op_26(true);
op_26(true);
%OptimizeFunctionOnNextCall(op_26);
op_26(true);
