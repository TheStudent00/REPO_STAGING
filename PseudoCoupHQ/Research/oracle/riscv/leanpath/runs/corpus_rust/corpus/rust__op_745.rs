// probe 745 -- binary ..
#[no_mangle]
pub fn op_745(a: bool, b: i64) -> core::ops::Range<bool> {
    a .. b
}
