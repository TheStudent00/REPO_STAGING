// probe 66 -- binary >>
function op_66(a, b) {
    return a >> b;
}

%PrepareFunctionForOptimization(op_66);
op_66(1.0, 2.0);
op_66(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_66);
op_66(1.0, 2.0);
