// probe 224 -- binary ^
#[no_mangle]
pub fn op_224(a: u64, b: u64) -> <u64 as core::ops::BitXor<u64>>::Output {
    a ^ b
}

// probe 13 -- unary !
#[no_mangle]
pub fn op_13(a: i64) -> <i64 as core::ops::Not>::Output {
    !a
}


#[no_mangle]
pub extern "C" fn emu_ZBB_RTYPE__XNOR(a: u64, b: u64) -> u64 {
    ((op_13((((op_224((a) as u64, (b) as u64)) as u64)) as i64)) as u64)
}
