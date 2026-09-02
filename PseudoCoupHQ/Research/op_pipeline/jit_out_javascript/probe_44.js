// probe 44 -- unary --
function op_44(a) {
    return a--;
}

%PrepareFunctionForOptimization(op_44);
op_44(true);
op_44(true);
%OptimizeFunctionOnNextCall(op_44);
op_44(true);
