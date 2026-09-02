// probe 258 -- binary instanceof
function op_258(a, b) {
    return a instanceof b;
}

%PrepareFunctionForOptimization(op_258);
op_258(1.0, 2.0);
op_258(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_258);
op_258(1.0, 2.0);
