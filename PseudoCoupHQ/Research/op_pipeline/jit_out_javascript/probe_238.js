// probe 238 -- binary >
function op_238(a, b) {
    return a > b;
}

%PrepareFunctionForOptimization(op_238);
op_238(1.0, 2.0);
op_238(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_238);
op_238(1.0, 2.0);
