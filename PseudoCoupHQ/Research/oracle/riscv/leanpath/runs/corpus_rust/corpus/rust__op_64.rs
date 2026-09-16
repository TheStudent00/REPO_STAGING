// probe 64 -- unary .await
#[no_mangle]
pub fn op_64(a: f64) -> f64 {
    a.await
}
