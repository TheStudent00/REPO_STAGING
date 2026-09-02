// probe 70 -- binary >>
function op_70(a, b) {
    return a >> b;
}

%PrepareFunctionForOptimization(op_70);
op_70(1.0, 2.0);
op_70(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_70);
op_70(1.0, 2.0);
