// probe 271 -- binary in
function op_271(a, b) {
    return a in b;
}

%PrepareFunctionForOptimization(op_271);
op_271(true, 2.0);
op_271(true, 2.0);
%OptimizeFunctionOnNextCall(op_271);
op_271(true, 2.0);
