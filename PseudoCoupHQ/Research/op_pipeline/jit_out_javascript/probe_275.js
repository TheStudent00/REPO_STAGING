// probe 275 -- binary as
function op_275(a, b) {
    return a as b;
}

%PrepareFunctionForOptimization(op_275);
op_275(1.0, false);
op_275(1.0, false);
%OptimizeFunctionOnNextCall(op_275);
op_275(1.0, false);
