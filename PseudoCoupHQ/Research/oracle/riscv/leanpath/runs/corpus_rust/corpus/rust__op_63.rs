// probe 63 -- unary .await
#[no_mangle]
pub fn op_63(a: f32) -> f32 {
    a.await
}
