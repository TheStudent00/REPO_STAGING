// probe 263 -- binary instanceof
function op_263(a, b) {
    return a instanceof b;
}

%PrepareFunctionForOptimization(op_263);
op_263(true, false);
op_263(true, false);
%OptimizeFunctionOnNextCall(op_263);
op_263(true, false);
