// probe 43 -- unary --
function op_43(a) {
    return a--;
}

%PrepareFunctionForOptimization(op_43);
op_43(1.0);
op_43(1.0);
%OptimizeFunctionOnNextCall(op_43);
op_43(1.0);
