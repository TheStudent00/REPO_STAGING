// probe 288 -- binary satisfies
function op_288(a, b) {
    return a satisfies b;
}

%PrepareFunctionForOptimization(op_288);
op_288(true, 2.0);
op_288(true, 2.0);
%OptimizeFunctionOnNextCall(op_288);
op_288(true, 2.0);
