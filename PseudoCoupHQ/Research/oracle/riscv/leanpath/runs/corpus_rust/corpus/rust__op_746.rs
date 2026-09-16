// probe 746 -- binary ..
#[no_mangle]
pub fn op_746(a: bool, b: u64) -> core::ops::Range<bool> {
    a .. b
}
