// probe 211 -- binary !=
function op_211(a, b) {
    return a != b;
}

%PrepareFunctionForOptimization(op_211);
op_211(1.0, 2.0);
op_211(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_211);
op_211(1.0, 2.0);
