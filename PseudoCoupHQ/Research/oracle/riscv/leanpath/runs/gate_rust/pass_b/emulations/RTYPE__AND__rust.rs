// probe 145 -- binary &
#[no_mangle]
pub fn op_145(a: i64, b: i64) -> <i64 as core::ops::BitAnd<i64>>::Output {
    a & b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__AND(a: u64, b: u64) -> u64 {
    ((op_145((a) as i64, (b) as i64)) as u64)
}
