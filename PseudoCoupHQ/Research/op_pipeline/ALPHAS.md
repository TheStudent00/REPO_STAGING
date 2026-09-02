# THE ALPHAS — the 275 level-0 components

Mined from the erased forms of 1,731 units (c, cpp, go, rust,
swift) by component_mine.py. An alpha is a component that
recurs in two or more units and contains no smaller recurring
component. `a` and `b` are the two arguments, `answer` the
result, `uN`/`kN` temps and constants, `_` a discarded slot.
Sorted by how many units carry it.

| id | units | languages | steps |
|---|---|---|---|
| K0000 | 219 | c, cpp, go, rust, swift | `u0 = xor(_,_)` |
| K0001 | 201 | c, cpp, go, swift | `u0 = setne(_)` |
| K0002 | 143 | c, cpp, rust, swift | `_ = cmp(b,a)` |
| K0003 | 143 | c, cpp, go, rust, swift | `_ = test(b,b)` |
| K0004 | 138 | c, cpp | `u0 = or(u1,u2)` |
| K0005 | 126 | c, cpp, swift | `_ = test(a,a)` |
| K0006 | 124 | c, cpp, go | `u0 = setp(_)` |
| K0007 | 116 | c, cpp, rust, swift | `answer = and(_,u0)` |
| K0008 | 77 | c, cpp, swift | `u0 = movslq(a,_)` |
| K0009 | 77 | c, cpp, swift | `u0 = movslq(b,_)` |
| K0010 | 73 | c, cpp, go, swift | `_ = cmp(a,b)` |
| K0011 | 73 | c, cpp | `u0 = cvtsi2ss(b,_)` |
| K0012 | 69 | c | `answer = movzbl(u0,_)` |
| K0013 | 69 | c, cpp | `u0 = cvtsi2ss(a,_)` |
| K0014 | 65 | c, cpp | `u0 = cvtsi2sd(a,_)` |
| K0015 | 65 | c, cpp | `u0 = cvtsi2sd(b,_)` |
| K0016 | 63 | c, cpp | `u0 = xorpd(_,_)` |
| K0017 | 63 | c, cpp | `u0 = xorps(_,_)` |
| K0018 | 60 | cpp, go, swift | `answer = and(u0,u1)` |
| K0019 | 55 | cpp, go, rust, swift | `answer = setae(_)` |
| K0020 | 55 | c, cpp, go, rust, swift | `return` |
| K0021 | 54 | c, cpp | `_ = ucomisd(u0,a)` |
| K0022 | 54 | c, cpp, rust, swift | `u0 = movd(u1,_)` |
| K0023 | 53 | cpp, go, rust, swift | `answer = seta(_)` |
| K0024 | 50 | c, cpp | `_ = ucomisd(u0,b)` |
| K0025 | 48 | c, cpp, go, rust, swift | `answer = and(b,a)` |
| K0026 | 46 | c, cpp, go, rust, swift | `answer = or(b,a)` |
| K0027 | 46 | cpp, go, swift | `answer = or(u0,u1)` |
| K0028 | 46 | c, cpp, swift | `u0 = setne(u1)` |
| K0029 | 45 | c, cpp | `answer = seta(u0)` |
| K0030 | 45 | c, cpp | `answer = setae(u0)` |
| K0031 | 45 | c, cpp, go, rust, swift | `answer = xor(b,a)` |
| K0032 | 44 | c, cpp | `_ = ucomiss(u0,a)` |
| K0033 | 44 | c, cpp, rust | `answer = lea(_,_)` |
| K0034 | 44 | c, cpp | `u0 = addsd(u1,u2)` |
| K0035 | 44 | c, cpp | `u0 = movapd(u1,_)` |
| K0036 | 44 | c, cpp | `u0 = subpd(k0,u1)` |
| K0037 | 44 | c, cpp | `u0 = unpckhpd(u1,u2)` |
| K0038 | 41 | c, cpp, rust | `answer = shl(b,a)` |
| K0039 | 40 | c, cpp | `_ = ucomiss(u0,b)` |
| K0040 | 35 | c, cpp, go | `u0 = and(u1,u2)` |
| K0041 | 34 | cpp, go, rust, swift | `answer = setne(_)` |
| K0042 | 31 | c, cpp | `answer = mov(_,_)` |
| K0043 | 30 | c, cpp, swift | `answer = setne(u0)` |
| K0044 | 30 | c, cpp, go, rust | `answer = sub(b,a)` |
| K0045 | 29 | c, cpp, swift | `_ = cmp(u0,a)` |
| K0046 | 27 | swift | `trap` |
| K0047 | 26 | c, cpp | `_ = cmp(u0,b)` |
| K0048 | 24 | go, swift | `_ = cmp(_,b)` |
| K0049 | 24 | c, cpp | `_ = ucomisd(a,u0)` |
| K0050 | 24 | c, cpp | `_ = ucomisd(b,u0)` |
| K0051 | 24 | c, cpp, swift | `answer = sete(u0)` |
| K0052 | 23 | cpp, go, rust, swift | `answer = sete(_)` |
| K0053 | 22 | c, cpp, rust | `answer = sar(b,a)` |
| K0054 | 22 | c, cpp | `u0 = cvtss2sd(a,_)` |
| K0055 | 22 | c, cpp | `u0 = cvtss2sd(b,_)` |
| K0056 | 22 | c, cpp | `u0 = punpckldq(k0,a)` |
| K0057 | 22 | c, cpp | `u0 = punpckldq(k0,b)` |
| K0058 | 21 | c, cpp, go, rust, swift | `answer = not(a)` |
| K0059 | 19 | c, cpp, rust | `answer = and(a,u0)` |
| K0060 | 19 | c, cpp, rust | `answer = and(b,u0)` |
| K0061 | 19 | c, cpp, rust | `answer = shr(b,a)` |
| K0062 | 19 | c, cpp, swift | `u0 = or(b,a)` |
| K0063 | 18 | c, cpp, rust | `answer = or(a,u0)` |
| K0064 | 18 | c, cpp, rust | `answer = or(b,u0)` |
| K0065 | 18 | go | `u0 = sbb(w0,w0)` |
| K0066 | 16 | c, cpp, go, rust | `answer = imul(b,a)` |
| K0067 | 16 | c, cpp | `answer = movapd(u0,_)` |
| K0068 | 16 | rust, swift | `jump jmp L?` |
| K0069 | 15 | c, cpp | `u0 = cmpneqsd(a,u1)` |
| K0070 | 15 | c, cpp | `u0 = cmpneqsd(b,u1)` |
| K0071 | 15 | cpp | `u0 = movzbl(u1,_)` |
| K0072 | 14 | c, cpp | `_ = ucomiss(a,u0)` |
| K0073 | 14 | c, cpp | `_ = ucomiss(b,u0)` |
| K0074 | 14 | cpp | `answer = cmovbe(u0,u1)` |
| K0075 | 14 | cpp | `u0 = add(u1,u1)` |
| K0076 | 14 | cpp | `u0 = cmovbe(u1,u2)` |
| K0077 | 14 | cpp | `u0 = mov(_,_)` |
| K0078 | 13 | cpp, swift | `_ = cmp(b,u0)` |
| K0079 | 13 | c, cpp, go, rust, swift | `_ = ucomisd(a,b)` |
| K0080 | 13 | c, cpp, go, rust, swift | `_ = ucomisd(b,a)` |
| K0081 | 13 | c, cpp, go, rust, swift | `_ = ucomiss(a,b)` |
| K0082 | 13 | c, cpp, go, rust, swift | `_ = ucomiss(b,a)` |
| K0083 | 13 | c, cpp, go, rust | `answer = neg(a)` |
| K0084 | 13 | c, cpp | `u0 = cmpeqsd(a,u1)` |
| K0085 | 12 | swift | `_ = cmp(a,u0)` |
| K0086 | 12 | c, cpp | `answer = movaps(u0,_)` |
| K0087 | 12 | c, cpp, swift | `answer = setg(u0)` |
| K0088 | 12 | cpp, go, rust, swift | `answer = setge(_)` |
| K0089 | 12 | c, cpp, swift | `answer = setge(u0)` |
| K0090 | 12 | cpp, go, rust, swift | `answer = setl(_)` |
| K0091 | 12 | c, cpp, swift | `answer = setl(u0)` |
| K0092 | 12 | c, cpp, swift | `answer = setle(u0)` |
| K0093 | 12 | go | `branch jl L2 if test(b,b)` |
| K0094 | 12 | go | `call runtime.panicshift` |
| K0095 | 12 | c, cpp | `u0 = addss(u1,u1)` |
| K0096 | 12 | c, cpp | `u0 = cvtsi2ss(u1,_)` |
| K0097 | 12 | c, go | `u0 = or(b,u1)` |
| K0098 | 10 | c, cpp | `answer = addsd(u0,a)` |
| K0099 | 10 | c, cpp | `answer = divsd(u0,a)` |
| K0100 | 10 | c, cpp | `answer = mulsd(u0,a)` |
| K0101 | 10 | c, cpp | `answer = subsd(u0,a)` |
| K0102 | 10 | c, cpp | `u0 = cmpeqsd(b,u1)` |
| K0103 | 10 | c, cpp, swift | `u0 = cqto(a)` |
| K0104 | 10 | go, swift | `u0 = shl(b,a)` |
| K0105 | 9 | c, cpp | `answer = setbe(u0)` |
| K0106 | 9 | c, cpp | `u0 = cmpeqss(a,u1)` |
| K0107 | 9 | c, cpp | `u0 = cmpneqss(a,u1)` |
| K0108 | 9 | c, cpp | `u0 = cmpneqss(b,u1)` |
| K0109 | 8 | cpp, go, rust | `answer = setg(_)` |
| K0110 | 8 | cpp, go, rust | `answer = setle(_)` |
| K0111 | 8 | c, cpp | `answer = xor(_,_)` |
| K0112 | 8 | c, cpp | `answer, u0 = div(u1:a, b)` |
| K0113 | 8 | c, cpp | `answer, u0 = idiv(u1:a, b)` |
| K0114 | 8 | c, cpp | `branch js L2 if test(b,b)` |
| K0115 | 8 | c, cpp | `mem = mov(a)` |
| K0116 | 8 | c, cpp | `u0 = addsd(u1,b)` |
| K0117 | 8 | c, cpp | `u0 = addss(u1,b)` |
| K0118 | 8 | c, cpp | `u0 = and(_,b)` |
| K0119 | 8 | c, cpp | `u0 = and(b,u1)` |
| K0120 | 8 | c, cpp | `u0 = divsd(b,u1)` |
| K0121 | 8 | c, cpp | `u0 = mulsd(u1,b)` |
| K0122 | 8 | c, cpp | `u0 = mulss(u1,b)` |
| K0123 | 8 | c, cpp, go, swift | `u0 = sete(_)` |
| K0124 | 8 | swift | `u0 = setns(_)` |
| K0125 | 8 | swift | `u0 = sets(_)` |
| K0126 | 8 | c, cpp | `u0 = shr(_,b)` |
| K0127 | 8 | c, cpp | `u0 = subsd(b,u1)` |
| K0128 | 8 | c, cpp | `u0, answer = div(u1:a, b)` |
| K0129 | 8 | c, cpp | `u0, answer = idiv(u1:a, b)` |
| K0130 | 8 | go, rust, swift | `u0, u1 = div(u2:a, b)` |
| K0131 | 7 | c, cpp, go | `answer = add(b,a)` |
| K0132 | 7 | cpp, go, rust, swift | `answer = setb(_)` |
| K0133 | 7 | c, cpp | `answer = setb(u0)` |
| K0134 | 7 | c | `u0 = and(a,u1)` |
| K0135 | 7 | c, cpp, rust | `u0 = xor(_,a)` |
| K0136 | 6 | c, cpp | `answer = addss(u0,a)` |
| K0137 | 6 | c, cpp | `answer = and(a,b)` |
| K0138 | 6 | c, cpp | `answer = divss(u0,a)` |
| K0139 | 6 | c, cpp | `answer = mulss(u0,a)` |
| K0140 | 6 | c, cpp | `answer = or(a,b)` |
| K0141 | 6 | c, cpp | `answer = subss(u0,a)` |
| K0142 | 6 | c, cpp, go, rust, swift | `answer = xor(_,a)` |
| K0143 | 6 | c, cpp | `answer = xor(a,b)` |
| K0144 | 6 | c, cpp | `answer = xor(a,u0)` |
| K0145 | 6 | c, cpp | `answer = xor(b,u0)` |
| K0146 | 6 | c, cpp, swift | `answer = xorps(k0,a)` |
| K0147 | 6 | c, cpp, swift | `u0 = cltd(a)` |
| K0148 | 6 | c, cpp | `u0 = cmpeqss(b,u1)` |
| K0149 | 6 | c, cpp | `u0 = cmpneqsd(u1,a)` |
| K0150 | 6 | c, cpp | `u0 = cmpneqsd(u1,b)` |
| K0151 | 6 | c, cpp | `u0 = cmpneqss(u1,a)` |
| K0152 | 6 | c, cpp | `u0 = cmpneqss(u1,b)` |
| K0153 | 6 | c, cpp | `u0 = divss(b,u1)` |
| K0154 | 6 | go | `u0 = not(u1)` |
| K0155 | 6 | c | `u0 = or(a,u1)` |
| K0156 | 6 | cpp, swift | `u0 = setg(_)` |
| K0157 | 6 | c, cpp | `u0 = subss(b,u1)` |
| K0158 | 6 | c, cpp, rust | `u0 = xor(_,b)` |
| K0159 | 5 | cpp, go, rust | `answer = setbe(_)` |
| K0160 | 5 | rust | `mem = movb(_)` |
| K0161 | 5 | c, cpp, rust, swift | `u0 = cmpneqsd(b,a)` |
| K0162 | 5 | c, cpp, rust, swift | `u0 = cmpneqss(b,a)` |
| K0163 | 5 | c, cpp, rust, swift | `u0 = xor(b,a)` |
| K0164 | 4 | cpp | `_ = ucomisd(answer,b)` |
| K0165 | 4 | cpp | `_ = ucomiss(answer,b)` |
| K0166 | 4 | c, cpp | `answer = add(a,b)` |
| K0167 | 4 | c, cpp | `answer = add(a,u0)` |
| K0168 | 4 | c, cpp | `answer = add(b,u0)` |
| K0169 | 4 | c, cpp, go, swift | `answer = addsd(b,a)` |
| K0170 | 4 | c, cpp | `answer = addsd(k0,a)` |
| K0171 | 4 | c, cpp, go, swift | `answer = addss(b,a)` |
| K0172 | 4 | c, cpp | `answer = addss(k0,a)` |
| K0173 | 4 | c, cpp | `answer = cmovne(a,u0)` |
| K0174 | 4 | c, cpp | `answer = cmovne(b,u0)` |
| K0175 | 4 | c, cpp, go, swift | `answer = divsd(b,a)` |
| K0176 | 4 | c, cpp, go, swift | `answer = divss(b,a)` |
| K0177 | 4 | c, cpp | `answer = imul(a,u0)` |
| K0178 | 4 | c, cpp | `answer = imul(b,u0)` |
| K0179 | 4 | c, cpp, go, swift | `answer = mulsd(b,a)` |
| K0180 | 4 | c, cpp, go, swift | `answer = mulss(b,a)` |
| K0181 | 4 | cpp | `answer = setne(a)` |
| K0182 | 4 | cpp | `answer = setne(b)` |
| K0183 | 4 | c, cpp | `answer = sub(b,u0)` |
| K0184 | 4 | c, cpp | `answer = sub(u0,a)` |
| K0185 | 4 | cpp | `answer = sub(u0,u1)` |
| K0186 | 4 | c, cpp, go, swift | `answer = subsd(b,a)` |
| K0187 | 4 | c, cpp, go, swift | `answer = subss(b,a)` |
| K0188 | 4 | cpp | `answer = xorpd(_,_)` |
| K0189 | 4 | cpp | `answer = xorps(_,_)` |
| K0190 | 4 | go, rust | `branch je L2 if test(b,b)` |
| K0191 | 4 | swift | `branch je L4 if test(b,b)` |
| K0192 | 4 | swift | `branch jl L2 if cmp(a,b)` |
| K0193 | 4 | c, cpp | `branch js L2 if test(a,a)` |
| K0194 | 4 | c, cpp | `u0 = and(_,a)` |
| K0195 | 4 | c, cpp, rust, swift | `u0 = cmpeqsd(b,a)` |
| K0196 | 4 | c, cpp, rust, swift | `u0 = cmpeqss(b,a)` |
| K0197 | 4 | c, cpp | `u0 = cqto(u1)` |
| K0198 | 4 | go | `u0 = sar(u1,a)` |
| K0199 | 4 | swift | `u0 = setae(_)` |
| K0200 | 4 | swift | `u0 = setb(_)` |
| K0201 | 4 | cpp | `u0 = setl(_)` |
| K0202 | 4 | swift | `u0 = setle(_)` |
| K0203 | 4 | c | `u0 = setp(u1)` |
| K0204 | 4 | c, cpp | `u0 = shr(_,a)` |
| K0205 | 4 | swift | `u0 = shr(_,u1)` |
| K0206 | 4 | go, swift | `u0 = shr(b,a)` |
| K0207 | 4 | swift | `u0, u1 = idiv(u2:a, b)` |
| K0208 | 3 | go | `answer = and(u0,a)` |
| K0209 | 3 | cpp, rust, swift | `answer = xor(_,u0)` |
| K0210 | 3 | rust | `mem = mov(b)` |
| K0211 | 3 | rust | `mem = mov(w0)` |
| K0212 | 3 | c, cpp, rust | `mem = movsd(a)` |
| K0213 | 3 | c, cpp, rust | `mem = movss(a)` |
| K0214 | 3 | swift | `u0 = add(b,a)` |
| K0215 | 3 | c, cpp | `u0 = andpd(u1,u2)` |
| K0216 | 3 | c, cpp | `u0 = andps(u1,u2)` |
| K0217 | 3 | go | `u0 = not(b)` |
| K0218 | 3 | c, cpp | `u0 = orpd(u1,u2)` |
| K0219 | 3 | c, cpp | `u0 = orps(u1,u2)` |
| K0220 | 3 | rust, swift | `u0 = shl(_,b)` |
| K0221 | 3 | swift | `u0 = sub(b,a)` |
| K0222 | 2 | swift | `_ = cmp(_,a)` |
| K0223 | 2 | c, cpp | `answer = addsd(b,u0)` |
| K0224 | 2 | swift | `answer = cmovb(u0,u1)` |
| K0225 | 2 | c, cpp | `answer = cmove(a,b)` |
| K0226 | 2 | c, cpp | `answer = cmove(b,a)` |
| K0227 | 2 | c, cpp | `answer = divsd(b,u0)` |
| K0228 | 2 | c, cpp | `answer = mulsd(b,u0)` |
| K0229 | 2 | go | `answer = pxor(u0,a)` |
| K0230 | 2 | go | `answer = sar(u0,a)` |
| K0231 | 2 | cpp | `answer = sete(a)` |
| K0232 | 2 | cpp | `answer = sete(b)` |
| K0233 | 2 | c, cpp | `answer = subsd(b,u0)` |
| K0234 | 2 | c, cpp | `answer, u0 = div(u1:a, u2)` |
| K0235 | 2 | c, cpp | `answer, u0 = div(u1:u2, b)` |
| K0236 | 2 | c, cpp | `answer, u0 = idiv(u1:a, u2)` |
| K0237 | 2 | c, cpp | `answer, u0 = idiv(u1:u2, b)` |
| K0238 | 2 | swift | `branch jb L2 if cmp(a,b)` |
| K0239 | 2 | swift | `branch jb L2 if ucomisd(a,b)` |
| K0240 | 2 | swift | `branch jb L2 if ucomiss(a,b)` |
| K0241 | 2 | swift | `branch je L3 if shr(_,u0)` |
| K0242 | 2 | swift | `branch je L5 if cmp(_,b)` |
| K0243 | 2 | swift | `branch je L5 if shr(_,u0)` |
| K0244 | 2 | swift | `branch je L6 if test(b,b)` |
| K0245 | 2 | swift | `branch je L7 if cmp(_,b)` |
| K0246 | 2 | swift | `branch jne L3 if cmp(_,a)` |
| K0247 | 2 | swift | `branch jne L3 if cmp(u0,a)` |
| K0248 | 2 | swift | `branch jo L2 if add(b,a)` |
| K0249 | 2 | swift | `branch jo L2 if imul(b,a)` |
| K0250 | 2 | swift | `branch jo L2 if neg(a)` |
| K0251 | 2 | swift | `branch jo L2 if sub(b,a)` |
| K0252 | 2 | rust | `call *0x0(%rip)` |
| K0253 | 2 | go | `call runtime.panicdivide` |
| K0254 | 2 | c, cpp | `u0 = addss(u1,a)` |
| K0255 | 2 | c, cpp | `u0 = divss(u1,a)` |
| K0256 | 2 | swift | `u0 = imul(b,a)` |
| K0257 | 2 | rust | `u0 = lea(k0,_)` |
| K0258 | 2 | swift | `u0 = movabs(_,_)` |
| K0259 | 2 | c, cpp | `u0 = mulss(u1,a)` |
| K0260 | 2 | swift | `u0 = neg(a)` |
| K0261 | 2 | swift | `u0 = or(u1,a)` |
| K0262 | 2 | swift | `u0 = seta(u1)` |
| K0263 | 2 | swift | `u0 = setae(u1)` |
| K0264 | 2 | swift | `u0 = setb(u1)` |
| K0265 | 2 | swift | `u0 = setbe(u1)` |
| K0266 | 2 | swift | `u0 = sete(u1)` |
| K0267 | 2 | cpp | `u0 = setg(u1)` |
| K0268 | 2 | go | `u0 = setnp(_)` |
| K0269 | 2 | c, cpp | `u0 = subss(u1,a)` |
| K0270 | 2 | rust | `u0 = xorps(k0,a)` |
| K0271 | 2 | c, cpp | `u0, answer = div(u1:a, u2)` |
| K0272 | 2 | c, cpp | `u0, answer = div(u1:u2, b)` |
| K0273 | 2 | c, cpp | `u0, answer = idiv(u1:a, u2)` |
| K0274 | 2 | c, cpp | `u0, answer = idiv(u1:u2, b)` |
