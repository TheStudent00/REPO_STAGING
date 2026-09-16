// probe 13 -- unary !
#[no_mangle]
pub fn op_13(a: i64) -> <i64 as core::ops::Not>::Output {
    !a
}


#[no_mangle]
pub extern "C" fn emu_C_NOT__one(a: u64) -> u64 {
    ((op_13((a) as i64)) as u64)
}
