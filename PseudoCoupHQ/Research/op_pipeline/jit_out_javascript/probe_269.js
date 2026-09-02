// probe 269 -- binary in
function op_269(a, b) {
    return a in b;
}

%PrepareFunctionForOptimization(op_269);
op_269(1.0, false);
op_269(1.0, false);
%OptimizeFunctionOnNextCall(op_269);
op_269(1.0, false);
