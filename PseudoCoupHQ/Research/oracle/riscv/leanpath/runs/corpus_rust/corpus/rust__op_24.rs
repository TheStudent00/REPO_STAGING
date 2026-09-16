// probe 24 -- unary &raw const
#[no_mangle]
pub fn op_24(a: i32) -> i32 {
    &raw const a
}
