// probe 112 -- binary |
function op_112(a, b) {
    return a | b;
}

%PrepareFunctionForOptimization(op_112);
op_112(1.0, 2.0);
op_112(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_112);
op_112(1.0, 2.0);
