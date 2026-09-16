// probe 13 -- unary !
#[no_mangle]
pub fn op_13(a: i64) -> <i64 as core::ops::Not>::Output {
    !a
}

// probe 152 -- binary &
#[no_mangle]
pub fn op_152(a: u64, b: u64) -> <u64 as core::ops::BitAnd<u64>>::Output {
    a & b
}


#[no_mangle]
pub extern "C" fn emu_ZBB_RTYPE__ANDN(a: u64, b: u64) -> u64 {
    ((op_152((a) as u64, (((op_13((b) as i64)) as u64)) as u64)) as u64)
}
