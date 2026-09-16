// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of CTZ__one__rd__go__all_constructed.
//   
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_CTZ__one__rd__go__all_constructed(a uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 63)) & uint32(0x1))
	var v1 uint32 = ((uint32((uint32(v0)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v2 uint32 = v1
	var v3 bool = ((uint32(uint32(0x1))) == (uint32(v2)))
	var v4 bool = (!(v3))
	var v5 uint64 = sel64(v4, uint64(uint64(0x3f)), uint64(uint64(0x40)))
	var v6 uint32 = ((uint32((uint64(a)) >> 62)) & uint32(0x1))
	var v7 uint32 = ((uint32((uint32(v6)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v8 uint32 = v7
	var v9 bool = ((uint32(uint32(0x1))) == (uint32(v8)))
	var v10 bool = (!(v9))
	var v11 uint64 = sel64(v10, uint64(uint64(0x3e)), uint64(v5))
	var v12 uint32 = ((uint32((uint64(a)) >> 61)) & uint32(0x1))
	var v13 uint32 = ((uint32((uint32(v12)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v14 uint32 = v13
	var v15 bool = ((uint32(uint32(0x1))) == (uint32(v14)))
	var v16 bool = (!(v15))
	var v17 uint64 = sel64(v16, uint64(uint64(0x3d)), uint64(v11))
	var v18 uint32 = ((uint32((uint64(a)) >> 60)) & uint32(0x1))
	var v19 uint32 = ((uint32((uint32(v18)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v20 uint32 = v19
	var v21 bool = ((uint32(uint32(0x1))) == (uint32(v20)))
	var v22 bool = (!(v21))
	var v23 uint64 = sel64(v22, uint64(uint64(0x3c)), uint64(v17))
	var v24 uint32 = ((uint32((uint64(a)) >> 59)) & uint32(0x1))
	var v25 uint32 = ((uint32((uint32(v24)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v26 uint32 = v25
	var v27 bool = ((uint32(uint32(0x1))) == (uint32(v26)))
	var v28 bool = (!(v27))
	var v29 uint64 = sel64(v28, uint64(uint64(0x3b)), uint64(v23))
	var v30 uint32 = ((uint32((uint64(a)) >> 58)) & uint32(0x1))
	var v31 uint32 = ((uint32((uint32(v30)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v32 uint32 = v31
	var v33 bool = ((uint32(uint32(0x1))) == (uint32(v32)))
	var v34 bool = (!(v33))
	var v35 uint64 = sel64(v34, uint64(uint64(0x3a)), uint64(v29))
	var v36 uint32 = ((uint32((uint64(a)) >> 57)) & uint32(0x1))
	var v37 uint32 = ((uint32((uint32(v36)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v38 uint32 = v37
	var v39 bool = ((uint32(uint32(0x1))) == (uint32(v38)))
	var v40 bool = (!(v39))
	var v41 uint64 = sel64(v40, uint64(uint64(0x39)), uint64(v35))
	var v42 uint32 = ((uint32((uint64(a)) >> 56)) & uint32(0x1))
	var v43 uint32 = ((uint32((uint32(v42)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v44 uint32 = v43
	var v45 bool = ((uint32(uint32(0x1))) == (uint32(v44)))
	var v46 bool = (!(v45))
	var v47 uint64 = sel64(v46, uint64(uint64(0x38)), uint64(v41))
	var v48 uint32 = ((uint32((uint64(a)) >> 55)) & uint32(0x1))
	var v49 uint32 = ((uint32((uint32(v48)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v50 uint32 = v49
	var v51 bool = ((uint32(uint32(0x1))) == (uint32(v50)))
	var v52 bool = (!(v51))
	var v53 uint64 = sel64(v52, uint64(uint64(0x37)), uint64(v47))
	var v54 uint32 = ((uint32((uint64(a)) >> 54)) & uint32(0x1))
	var v55 uint32 = ((uint32((uint32(v54)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v56 uint32 = v55
	var v57 bool = ((uint32(uint32(0x1))) == (uint32(v56)))
	var v58 bool = (!(v57))
	var v59 uint64 = sel64(v58, uint64(uint64(0x36)), uint64(v53))
	var v60 uint32 = ((uint32((uint64(a)) >> 53)) & uint32(0x1))
	var v61 uint32 = ((uint32((uint32(v60)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v62 uint32 = v61
	var v63 bool = ((uint32(uint32(0x1))) == (uint32(v62)))
	var v64 bool = (!(v63))
	var v65 uint64 = sel64(v64, uint64(uint64(0x35)), uint64(v59))
	var v66 uint32 = ((uint32((uint64(a)) >> 52)) & uint32(0x1))
	var v67 uint32 = ((uint32((uint32(v66)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v68 uint32 = v67
	var v69 bool = ((uint32(uint32(0x1))) == (uint32(v68)))
	var v70 bool = (!(v69))
	var v71 uint64 = sel64(v70, uint64(uint64(0x34)), uint64(v65))
	var v72 uint32 = ((uint32((uint64(a)) >> 51)) & uint32(0x1))
	var v73 uint32 = ((uint32((uint32(v72)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v74 uint32 = v73
	var v75 bool = ((uint32(uint32(0x1))) == (uint32(v74)))
	var v76 bool = (!(v75))
	var v77 uint64 = sel64(v76, uint64(uint64(0x33)), uint64(v71))
	var v78 uint32 = ((uint32((uint64(a)) >> 50)) & uint32(0x1))
	var v79 uint32 = ((uint32((uint32(v78)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v80 uint32 = v79
	var v81 bool = ((uint32(uint32(0x1))) == (uint32(v80)))
	var v82 bool = (!(v81))
	var v83 uint64 = sel64(v82, uint64(uint64(0x32)), uint64(v77))
	var v84 uint32 = ((uint32((uint64(a)) >> 49)) & uint32(0x1))
	var v85 uint32 = ((uint32((uint32(v84)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v86 uint32 = v85
	var v87 bool = ((uint32(uint32(0x1))) == (uint32(v86)))
	var v88 bool = (!(v87))
	var v89 uint64 = sel64(v88, uint64(uint64(0x31)), uint64(v83))
	var v90 uint32 = ((uint32((uint64(a)) >> 48)) & uint32(0x1))
	var v91 uint32 = ((uint32((uint32(v90)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v92 uint32 = v91
	var v93 bool = ((uint32(uint32(0x1))) == (uint32(v92)))
	var v94 bool = (!(v93))
	var v95 uint64 = sel64(v94, uint64(uint64(0x30)), uint64(v89))
	var v96 uint32 = ((uint32((uint64(a)) >> 47)) & uint32(0x1))
	var v97 uint32 = ((uint32((uint32(v96)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v98 uint32 = v97
	var v99 bool = ((uint32(uint32(0x1))) == (uint32(v98)))
	var v100 bool = (!(v99))
	var v101 uint64 = sel64(v100, uint64(uint64(0x2f)), uint64(v95))
	var v102 uint32 = ((uint32((uint64(a)) >> 46)) & uint32(0x1))
	var v103 uint32 = ((uint32((uint32(v102)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v104 uint32 = v103
	var v105 bool = ((uint32(uint32(0x1))) == (uint32(v104)))
	var v106 bool = (!(v105))
	var v107 uint64 = sel64(v106, uint64(uint64(0x2e)), uint64(v101))
	var v108 uint32 = ((uint32((uint64(a)) >> 45)) & uint32(0x1))
	var v109 uint32 = ((uint32((uint32(v108)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v110 uint32 = v109
	var v111 bool = ((uint32(uint32(0x1))) == (uint32(v110)))
	var v112 bool = (!(v111))
	var v113 uint64 = sel64(v112, uint64(uint64(0x2d)), uint64(v107))
	var v114 uint32 = ((uint32((uint64(a)) >> 44)) & uint32(0x1))
	var v115 uint32 = ((uint32((uint32(v114)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v116 uint32 = v115
	var v117 bool = ((uint32(uint32(0x1))) == (uint32(v116)))
	var v118 bool = (!(v117))
	var v119 uint64 = sel64(v118, uint64(uint64(0x2c)), uint64(v113))
	var v120 uint32 = ((uint32((uint64(a)) >> 43)) & uint32(0x1))
	var v121 uint32 = ((uint32((uint32(v120)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v122 uint32 = v121
	var v123 bool = ((uint32(uint32(0x1))) == (uint32(v122)))
	var v124 bool = (!(v123))
	var v125 uint64 = sel64(v124, uint64(uint64(0x2b)), uint64(v119))
	var v126 uint32 = ((uint32((uint64(a)) >> 42)) & uint32(0x1))
	var v127 uint32 = ((uint32((uint32(v126)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v128 uint32 = v127
	var v129 bool = ((uint32(uint32(0x1))) == (uint32(v128)))
	var v130 bool = (!(v129))
	var v131 uint64 = sel64(v130, uint64(uint64(0x2a)), uint64(v125))
	var v132 uint32 = ((uint32((uint64(a)) >> 41)) & uint32(0x1))
	var v133 uint32 = ((uint32((uint32(v132)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v134 uint32 = v133
	var v135 bool = ((uint32(uint32(0x1))) == (uint32(v134)))
	var v136 bool = (!(v135))
	var v137 uint64 = sel64(v136, uint64(uint64(0x29)), uint64(v131))
	var v138 uint32 = ((uint32((uint64(a)) >> 40)) & uint32(0x1))
	var v139 uint32 = ((uint32((uint32(v138)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v140 uint32 = v139
	var v141 bool = ((uint32(uint32(0x1))) == (uint32(v140)))
	var v142 bool = (!(v141))
	var v143 uint64 = sel64(v142, uint64(uint64(0x28)), uint64(v137))
	var v144 uint32 = ((uint32((uint64(a)) >> 39)) & uint32(0x1))
	var v145 uint32 = ((uint32((uint32(v144)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v146 uint32 = v145
	var v147 bool = ((uint32(uint32(0x1))) == (uint32(v146)))
	var v148 bool = (!(v147))
	var v149 uint64 = sel64(v148, uint64(uint64(0x27)), uint64(v143))
	var v150 uint32 = ((uint32((uint64(a)) >> 38)) & uint32(0x1))
	var v151 uint32 = ((uint32((uint32(v150)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v152 uint32 = v151
	var v153 bool = ((uint32(uint32(0x1))) == (uint32(v152)))
	var v154 bool = (!(v153))
	var v155 uint64 = sel64(v154, uint64(uint64(0x26)), uint64(v149))
	var v156 uint32 = ((uint32((uint64(a)) >> 37)) & uint32(0x1))
	var v157 uint32 = ((uint32((uint32(v156)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v158 uint32 = v157
	var v159 bool = ((uint32(uint32(0x1))) == (uint32(v158)))
	var v160 bool = (!(v159))
	var v161 uint64 = sel64(v160, uint64(uint64(0x25)), uint64(v155))
	var v162 uint32 = ((uint32((uint64(a)) >> 36)) & uint32(0x1))
	var v163 uint32 = ((uint32((uint32(v162)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v164 uint32 = v163
	var v165 bool = ((uint32(uint32(0x1))) == (uint32(v164)))
	var v166 bool = (!(v165))
	var v167 uint64 = sel64(v166, uint64(uint64(0x24)), uint64(v161))
	var v168 uint32 = ((uint32((uint64(a)) >> 35)) & uint32(0x1))
	var v169 uint32 = ((uint32((uint32(v168)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v170 uint32 = v169
	var v171 bool = ((uint32(uint32(0x1))) == (uint32(v170)))
	var v172 bool = (!(v171))
	var v173 uint64 = sel64(v172, uint64(uint64(0x23)), uint64(v167))
	var v174 uint32 = ((uint32((uint64(a)) >> 34)) & uint32(0x1))
	var v175 uint32 = ((uint32((uint32(v174)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v176 uint32 = v175
	var v177 bool = ((uint32(uint32(0x1))) == (uint32(v176)))
	var v178 bool = (!(v177))
	var v179 uint64 = sel64(v178, uint64(uint64(0x22)), uint64(v173))
	var v180 uint32 = ((uint32((uint64(a)) >> 33)) & uint32(0x1))
	var v181 uint32 = ((uint32((uint32(v180)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v182 uint32 = v181
	var v183 bool = ((uint32(uint32(0x1))) == (uint32(v182)))
	var v184 bool = (!(v183))
	var v185 uint64 = sel64(v184, uint64(uint64(0x21)), uint64(v179))
	var v186 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1))
	var v187 uint32 = ((uint32((uint32(v186)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v188 uint32 = v187
	var v189 bool = ((uint32(uint32(0x1))) == (uint32(v188)))
	var v190 bool = (!(v189))
	var v191 uint64 = sel64(v190, uint64(uint64(0x20)), uint64(v185))
	var v192 uint32 = ((uint32((uint64(a)) >> 31)) & uint32(0x1))
	var v193 uint32 = ((uint32((uint32(v192)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v194 uint32 = v193
	var v195 bool = ((uint32(uint32(0x1))) == (uint32(v194)))
	var v196 bool = (!(v195))
	var v197 uint64 = sel64(v196, uint64(uint64(0x1f)), uint64(v191))
	var v198 uint32 = ((uint32((uint64(a)) >> 30)) & uint32(0x1))
	var v199 uint32 = ((uint32((uint32(v198)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v200 uint32 = v199
	var v201 bool = ((uint32(uint32(0x1))) == (uint32(v200)))
	var v202 bool = (!(v201))
	var v203 uint64 = sel64(v202, uint64(uint64(0x1e)), uint64(v197))
	var v204 uint32 = ((uint32((uint64(a)) >> 29)) & uint32(0x1))
	var v205 uint32 = ((uint32((uint32(v204)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v206 uint32 = v205
	var v207 bool = ((uint32(uint32(0x1))) == (uint32(v206)))
	var v208 bool = (!(v207))
	var v209 uint64 = sel64(v208, uint64(uint64(0x1d)), uint64(v203))
	var v210 uint32 = ((uint32((uint64(a)) >> 28)) & uint32(0x1))
	var v211 uint32 = ((uint32((uint32(v210)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v212 uint32 = v211
	var v213 bool = ((uint32(uint32(0x1))) == (uint32(v212)))
	var v214 bool = (!(v213))
	var v215 uint64 = sel64(v214, uint64(uint64(0x1c)), uint64(v209))
	var v216 uint32 = ((uint32((uint64(a)) >> 27)) & uint32(0x1))
	var v217 uint32 = ((uint32((uint32(v216)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v218 uint32 = v217
	var v219 bool = ((uint32(uint32(0x1))) == (uint32(v218)))
	var v220 bool = (!(v219))
	var v221 uint64 = sel64(v220, uint64(uint64(0x1b)), uint64(v215))
	var v222 uint32 = ((uint32((uint64(a)) >> 26)) & uint32(0x1))
	var v223 uint32 = ((uint32((uint32(v222)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v224 uint32 = v223
	var v225 bool = ((uint32(uint32(0x1))) == (uint32(v224)))
	var v226 bool = (!(v225))
	var v227 uint64 = sel64(v226, uint64(uint64(0x1a)), uint64(v221))
	var v228 uint32 = ((uint32((uint64(a)) >> 25)) & uint32(0x1))
	var v229 uint32 = ((uint32((uint32(v228)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v230 uint32 = v229
	var v231 bool = ((uint32(uint32(0x1))) == (uint32(v230)))
	var v232 bool = (!(v231))
	var v233 uint64 = sel64(v232, uint64(uint64(0x19)), uint64(v227))
	var v234 uint32 = ((uint32((uint64(a)) >> 24)) & uint32(0x1))
	var v235 uint32 = ((uint32((uint32(v234)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v236 uint32 = v235
	var v237 bool = ((uint32(uint32(0x1))) == (uint32(v236)))
	var v238 bool = (!(v237))
	var v239 uint64 = sel64(v238, uint64(uint64(0x18)), uint64(v233))
	var v240 uint32 = ((uint32((uint64(a)) >> 23)) & uint32(0x1))
	var v241 uint32 = ((uint32((uint32(v240)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v242 uint32 = v241
	var v243 bool = ((uint32(uint32(0x1))) == (uint32(v242)))
	var v244 bool = (!(v243))
	var v245 uint64 = sel64(v244, uint64(uint64(0x17)), uint64(v239))
	var v246 uint32 = ((uint32((uint64(a)) >> 22)) & uint32(0x1))
	var v247 uint32 = ((uint32((uint32(v246)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v248 uint32 = v247
	var v249 bool = ((uint32(uint32(0x1))) == (uint32(v248)))
	var v250 bool = (!(v249))
	var v251 uint64 = sel64(v250, uint64(uint64(0x16)), uint64(v245))
	var v252 uint32 = ((uint32((uint64(a)) >> 21)) & uint32(0x1))
	var v253 uint32 = ((uint32((uint32(v252)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v254 uint32 = v253
	var v255 bool = ((uint32(uint32(0x1))) == (uint32(v254)))
	var v256 bool = (!(v255))
	var v257 uint64 = sel64(v256, uint64(uint64(0x15)), uint64(v251))
	var v258 uint32 = ((uint32((uint64(a)) >> 20)) & uint32(0x1))
	var v259 uint32 = ((uint32((uint32(v258)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v260 uint32 = v259
	var v261 bool = ((uint32(uint32(0x1))) == (uint32(v260)))
	var v262 bool = (!(v261))
	var v263 uint64 = sel64(v262, uint64(uint64(0x14)), uint64(v257))
	var v264 uint32 = ((uint32((uint64(a)) >> 19)) & uint32(0x1))
	var v265 uint32 = ((uint32((uint32(v264)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v266 uint32 = v265
	var v267 bool = ((uint32(uint32(0x1))) == (uint32(v266)))
	var v268 bool = (!(v267))
	var v269 uint64 = sel64(v268, uint64(uint64(0x13)), uint64(v263))
	var v270 uint32 = ((uint32((uint64(a)) >> 18)) & uint32(0x1))
	var v271 uint32 = ((uint32((uint32(v270)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v272 uint32 = v271
	var v273 bool = ((uint32(uint32(0x1))) == (uint32(v272)))
	var v274 bool = (!(v273))
	var v275 uint64 = sel64(v274, uint64(uint64(0x12)), uint64(v269))
	var v276 uint32 = ((uint32((uint64(a)) >> 17)) & uint32(0x1))
	var v277 uint32 = ((uint32((uint32(v276)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v278 uint32 = v277
	var v279 bool = ((uint32(uint32(0x1))) == (uint32(v278)))
	var v280 bool = (!(v279))
	var v281 uint64 = sel64(v280, uint64(uint64(0x11)), uint64(v275))
	var v282 uint32 = ((uint32((uint64(a)) >> 16)) & uint32(0x1))
	var v283 uint32 = ((uint32((uint32(v282)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v284 uint32 = v283
	var v285 bool = ((uint32(uint32(0x1))) == (uint32(v284)))
	var v286 bool = (!(v285))
	var v287 uint64 = sel64(v286, uint64(uint64(0x10)), uint64(v281))
	var v288 uint32 = ((uint32((uint64(a)) >> 15)) & uint32(0x1))
	var v289 uint32 = ((uint32((uint32(v288)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v290 uint32 = v289
	var v291 bool = ((uint32(uint32(0x1))) == (uint32(v290)))
	var v292 bool = (!(v291))
	var v293 uint64 = sel64(v292, uint64(uint64(0xf)), uint64(v287))
	var v294 uint32 = ((uint32((uint64(a)) >> 14)) & uint32(0x1))
	var v295 uint32 = ((uint32((uint32(v294)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v296 uint32 = v295
	var v297 bool = ((uint32(uint32(0x1))) == (uint32(v296)))
	var v298 bool = (!(v297))
	var v299 uint64 = sel64(v298, uint64(uint64(0xe)), uint64(v293))
	var v300 uint32 = ((uint32((uint64(a)) >> 13)) & uint32(0x1))
	var v301 uint32 = ((uint32((uint32(v300)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v302 uint32 = v301
	var v303 bool = ((uint32(uint32(0x1))) == (uint32(v302)))
	var v304 bool = (!(v303))
	var v305 uint64 = sel64(v304, uint64(uint64(0xd)), uint64(v299))
	var v306 uint32 = ((uint32((uint64(a)) >> 12)) & uint32(0x1))
	var v307 uint32 = ((uint32((uint32(v306)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v308 uint32 = v307
	var v309 bool = ((uint32(uint32(0x1))) == (uint32(v308)))
	var v310 bool = (!(v309))
	var v311 uint64 = sel64(v310, uint64(uint64(0xc)), uint64(v305))
	var v312 uint32 = ((uint32((uint64(a)) >> 11)) & uint32(0x1))
	var v313 uint32 = ((uint32((uint32(v312)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v314 uint32 = v313
	var v315 bool = ((uint32(uint32(0x1))) == (uint32(v314)))
	var v316 bool = (!(v315))
	var v317 uint64 = sel64(v316, uint64(uint64(0xb)), uint64(v311))
	var v318 uint32 = ((uint32((uint64(a)) >> 10)) & uint32(0x1))
	var v319 uint32 = ((uint32((uint32(v318)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v320 uint32 = v319
	var v321 bool = ((uint32(uint32(0x1))) == (uint32(v320)))
	var v322 bool = (!(v321))
	var v323 uint64 = sel64(v322, uint64(uint64(0xa)), uint64(v317))
	var v324 uint32 = ((uint32((uint64(a)) >> 9)) & uint32(0x1))
	var v325 uint32 = ((uint32((uint32(v324)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v326 uint32 = v325
	var v327 bool = ((uint32(uint32(0x1))) == (uint32(v326)))
	var v328 bool = (!(v327))
	var v329 uint64 = sel64(v328, uint64(uint64(0x9)), uint64(v323))
	var v330 uint32 = ((uint32((uint64(a)) >> 8)) & uint32(0x1))
	var v331 uint32 = ((uint32((uint32(v330)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v332 uint32 = v331
	var v333 bool = ((uint32(uint32(0x1))) == (uint32(v332)))
	var v334 bool = (!(v333))
	var v335 uint64 = sel64(v334, uint64(uint64(0x8)), uint64(v329))
	var v336 uint32 = ((uint32((uint64(a)) >> 7)) & uint32(0x1))
	var v337 uint32 = ((uint32((uint32(v336)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v338 uint32 = v337
	var v339 bool = ((uint32(uint32(0x1))) == (uint32(v338)))
	var v340 bool = (!(v339))
	var v341 uint64 = sel64(v340, uint64(uint64(0x7)), uint64(v335))
	var v342 uint32 = ((uint32((uint64(a)) >> 6)) & uint32(0x1))
	var v343 uint32 = ((uint32((uint32(v342)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v344 uint32 = v343
	var v345 bool = ((uint32(uint32(0x1))) == (uint32(v344)))
	var v346 bool = (!(v345))
	var v347 uint64 = sel64(v346, uint64(uint64(0x6)), uint64(v341))
	var v348 uint32 = ((uint32((uint64(a)) >> 5)) & uint32(0x1))
	var v349 uint32 = ((uint32((uint32(v348)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v350 uint32 = v349
	var v351 bool = ((uint32(uint32(0x1))) == (uint32(v350)))
	var v352 bool = (!(v351))
	var v353 uint64 = sel64(v352, uint64(uint64(0x5)), uint64(v347))
	var v354 uint32 = ((uint32((uint64(a)) >> 4)) & uint32(0x1))
	var v355 uint32 = ((uint32((uint32(v354)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v356 uint32 = v355
	var v357 bool = ((uint32(uint32(0x1))) == (uint32(v356)))
	var v358 bool = (!(v357))
	var v359 uint64 = sel64(v358, uint64(uint64(0x4)), uint64(v353))
	var v360 uint32 = ((uint32((uint64(a)) >> 3)) & uint32(0x1))
	var v361 uint32 = ((uint32((uint32(v360)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v362 uint32 = v361
	var v363 bool = ((uint32(uint32(0x1))) == (uint32(v362)))
	var v364 bool = (!(v363))
	var v365 uint64 = sel64(v364, uint64(uint64(0x3)), uint64(v359))
	var v366 uint32 = ((uint32((uint64(a)) >> 2)) & uint32(0x1))
	var v367 uint32 = ((uint32((uint32(v366)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v368 uint32 = v367
	var v369 bool = ((uint32(uint32(0x1))) == (uint32(v368)))
	var v370 bool = (!(v369))
	var v371 uint64 = sel64(v370, uint64(uint64(0x2)), uint64(v365))
	var v372 uint32 = ((uint32((uint64(a)) >> 1)) & uint32(0x1))
	var v373 uint32 = ((uint32((uint32(v372)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v374 uint32 = v373
	var v375 bool = ((uint32(uint32(0x1))) == (uint32(v374)))
	var v376 bool = (!(v375))
	var v377 uint64 = sel64(v376, uint64(uint64(0x1)), uint64(v371))
	var v378 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x1))
	var v379 uint32 = ((uint32((uint32(v378)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v380 uint32 = v379
	var v381 bool = ((uint32(uint32(0x1))) == (uint32(v380)))
	var v382 bool = (!(v381))
	var v383 uint64 = sel64(v382, uint64(uint64(0x0)), uint64(v377))
	return uint64(v383)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_CTZ__one__rd__go__all_constructed(g0)
	_ = sink
}
