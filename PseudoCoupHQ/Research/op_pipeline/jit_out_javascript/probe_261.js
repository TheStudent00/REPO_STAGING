// probe 261 -- binary instanceof
function op_261(a, b) {
    return a instanceof b;
}

%PrepareFunctionForOptimization(op_261);
op_261(true, 2.0);
op_261(true, 2.0);
%OptimizeFunctionOnNextCall(op_261);
op_261(true, 2.0);
