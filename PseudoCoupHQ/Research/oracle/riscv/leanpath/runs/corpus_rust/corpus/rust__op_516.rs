// probe 516 -- binary >>
#[no_mangle]
pub fn op_516(a: f32, b: i32) -> <f32 as core::ops::Shr<i32>>::Output {
    a >> b
}
