// probe 201 -- binary ===
function op_201(a, b) {
    return a === b;
}

%PrepareFunctionForOptimization(op_201);
op_201(1.0, 2.0);
op_201(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_201);
op_201(1.0, 2.0);
