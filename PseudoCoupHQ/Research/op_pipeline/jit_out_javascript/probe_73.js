// probe 73 -- binary >>
function op_73(a, b) {
    return a >> b;
}

%PrepareFunctionForOptimization(op_73);
op_73(true, 2.0);
op_73(true, 2.0);
%OptimizeFunctionOnNextCall(op_73);
op_73(true, 2.0);
