// probe 277 -- binary as
function op_277(a, b) {
    return a as b;
}

%PrepareFunctionForOptimization(op_277);
op_277(1.0, 2.0);
op_277(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_277);
op_277(1.0, 2.0);
