// probe 35 -- unary &raw mut
#[no_mangle]
pub fn op_35(a: bool) -> bool {
    &raw mut a
}
