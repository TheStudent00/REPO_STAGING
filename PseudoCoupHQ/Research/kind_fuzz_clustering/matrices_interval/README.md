# interval matrices (the tensor)

One CSV per `language.operator`.  One row per (operator, lhs holder, rhs holder, interval spec); the 32 samples live INSIDE the row as three semicolon-separated vectors of equal length.  Columns: `probe_id`, `lhs_holder`, `rhs_holder`, `interval_id`, `n_samples`, `lhs_canon_vector`, `rhs_canon_vector`, `output_canon_vector`, `n_values`, `n_declines`.

Canon rules are the v2 rules unchanged.  A slot with no value carries `REFUSE`, `RAISE:<kind>` or `ABORT`; nothing is padded and no slot is ever empty.

The edge-value matrices in `../matrices/` are untouched -- interval sampling is IN ADDITION to the edge classes, never a replacement.

## ladders

- `f_b32`: 32 samples, 0.0 .. -1.2169445762191002e+32
- `f_b64`: 32 samples, 0.0 .. -9.00902019456564e+256
- `w_big128`: 32 samples, -170141183460469231731687303715884105728 .. -316254960208631187394611693017586250
- `w_s128`: 32 samples, -170141183460469231731687303715884105728 .. -316254960208631187394611693017586250
- `w_s32`: 32 samples, -2147483648 .. -462768134
- `w_s64`: 32 samples, -9223372036854775808 .. -407619307041649444
- `w_u64`: 32 samples, 0 .. 3995560058794633904
