// probe 475 -- binary <<
#[no_mangle]
pub fn op_475(a: u64, b: i64) -> <u64 as core::ops::Shl<i64>>::Output {
    a << b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__SLL(a: u64, b: u64) -> u64 {
    ((op_475((a) as u64, (b) as i64)) as u64)
}
