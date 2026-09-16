// probe 13 -- unary !
#[no_mangle]
pub fn op_13(a: i64) -> <i64 as core::ops::Not>::Output {
    !a
}

// probe 188 -- binary |
#[no_mangle]
pub fn op_188(a: u64, b: u64) -> <u64 as core::ops::BitOr<u64>>::Output {
    a | b
}


#[no_mangle]
pub extern "C" fn emu_ZBB_RTYPE__ORN(a: u64, b: u64) -> u64 {
    ((op_188((a) as u64, (((op_13((b) as i64)) as u64)) as u64)) as u64)
}
