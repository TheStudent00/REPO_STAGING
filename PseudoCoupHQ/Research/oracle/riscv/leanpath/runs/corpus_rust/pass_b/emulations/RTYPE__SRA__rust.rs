// probe 505 -- binary >>
#[no_mangle]
pub fn op_505(a: i64, b: i64) -> <i64 as core::ops::Shr<i64>>::Output {
    a >> b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__SRA(a: u64, b: u64) -> u64 {
    ((op_505((a) as i64, (b) as i64)) as u64)
}
