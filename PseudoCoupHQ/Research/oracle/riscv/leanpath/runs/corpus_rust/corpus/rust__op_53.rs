// probe 53 -- unary ?
#[no_mangle]
pub fn op_53(a: bool) -> bool {
    a?
}
