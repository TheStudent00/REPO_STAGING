// probe 259 -- binary instanceof
function op_259(a, b) {
    return a instanceof b;
}

%PrepareFunctionForOptimization(op_259);
op_259(1.0, 2.0);
op_259(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_259);
op_259(1.0, 2.0);
