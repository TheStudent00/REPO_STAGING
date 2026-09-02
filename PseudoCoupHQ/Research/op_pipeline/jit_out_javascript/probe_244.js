// probe 244 -- binary >
function op_244(a, b) {
    return a > b;
}

%PrepareFunctionForOptimization(op_244);
op_244(true, 2.0);
op_244(true, 2.0);
%OptimizeFunctionOnNextCall(op_244);
op_244(true, 2.0);
