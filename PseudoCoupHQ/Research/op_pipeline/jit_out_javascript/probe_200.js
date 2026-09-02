// probe 200 -- binary ==
function op_200(a, b) {
    return a == b;
}

%PrepareFunctionForOptimization(op_200);
op_200(true, false);
op_200(true, false);
%OptimizeFunctionOnNextCall(op_200);
op_200(true, false);
