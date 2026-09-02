// probe 72 -- binary >>
function op_72(a, b) {
    return a >> b;
}

%PrepareFunctionForOptimization(op_72);
op_72(true, 2.0);
op_72(true, 2.0);
%OptimizeFunctionOnNextCall(op_72);
op_72(true, 2.0);
