// probe 92 -- binary <<
function op_92(a, b) {
    return a << b;
}

%PrepareFunctionForOptimization(op_92);
op_92(true, false);
op_92(true, false);
%OptimizeFunctionOnNextCall(op_92);
op_92(true, false);
