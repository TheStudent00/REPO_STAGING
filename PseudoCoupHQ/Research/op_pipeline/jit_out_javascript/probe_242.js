// probe 242 -- binary >
function op_242(a, b) {
    return a > b;
}

%PrepareFunctionForOptimization(op_242);
op_242(1.0, false);
op_242(1.0, false);
%OptimizeFunctionOnNextCall(op_242);
op_242(1.0, false);
