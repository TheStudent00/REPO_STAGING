// probe 100 -- binary &
function op_100(a, b) {
    return a & b;
}

%PrepareFunctionForOptimization(op_100);
op_100(true, 2.0);
op_100(true, 2.0);
%OptimizeFunctionOnNextCall(op_100);
op_100(true, 2.0);
