// probe 241 -- binary >
function op_241(a, b) {
    return a > b;
}

%PrepareFunctionForOptimization(op_241);
op_241(1.0, 2.0);
op_241(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_241);
op_241(1.0, 2.0);
