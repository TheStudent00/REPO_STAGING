// probe 29 -- unary &raw const
#[no_mangle]
pub fn op_29(a: bool) -> bool {
    &raw const a
}
