// probe 97 -- binary &
function op_97(a, b) {
    return a & b;
}

%PrepareFunctionForOptimization(op_97);
op_97(1.0, 2.0);
op_97(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_97);
op_97(1.0, 2.0);
