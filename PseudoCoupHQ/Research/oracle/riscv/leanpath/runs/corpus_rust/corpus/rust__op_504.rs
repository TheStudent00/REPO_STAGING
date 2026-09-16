// probe 504 -- binary >>
#[no_mangle]
pub fn op_504(a: i64, b: i32) -> <i64 as core::ops::Shr<i32>>::Output {
    a >> b
}
