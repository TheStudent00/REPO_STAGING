// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of CTZW__one__rd__go__all_constructed.
//   
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_CTZW__one__rd__go__all_constructed(a uint32) uint64 {
	var v0 uint32 = ((uint32((uint32(a)) >> 31)) & uint32(0x1))
	var v1 uint32 = ((uint32((uint32(v0)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v2 uint32 = v1
	var v3 bool = ((uint32(uint32(0x1))) == (uint32(v2)))
	var v4 bool = (!(v3))
	var v5 uint32 = sel32(v4, uint32(uint32(0x1f)), uint32(uint32(0x20)))
	var v6 uint32 = ((uint32((uint32(a)) >> 30)) & uint32(0x1))
	var v7 uint32 = ((uint32((uint32(v6)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v8 uint32 = v7
	var v9 bool = ((uint32(uint32(0x1))) == (uint32(v8)))
	var v10 bool = (!(v9))
	var v11 uint32 = sel32(v10, uint32(uint32(0x1e)), uint32(v5))
	var v12 uint32 = ((uint32((uint32(a)) >> 29)) & uint32(0x1))
	var v13 uint32 = ((uint32((uint32(v12)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v14 uint32 = v13
	var v15 bool = ((uint32(uint32(0x1))) == (uint32(v14)))
	var v16 bool = (!(v15))
	var v17 uint32 = sel32(v16, uint32(uint32(0x1d)), uint32(v11))
	var v18 uint32 = ((uint32((uint32(a)) >> 28)) & uint32(0x1))
	var v19 uint32 = ((uint32((uint32(v18)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v20 uint32 = v19
	var v21 bool = ((uint32(uint32(0x1))) == (uint32(v20)))
	var v22 bool = (!(v21))
	var v23 uint32 = sel32(v22, uint32(uint32(0x1c)), uint32(v17))
	var v24 uint32 = ((uint32((uint32(a)) >> 27)) & uint32(0x1))
	var v25 uint32 = ((uint32((uint32(v24)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v26 uint32 = v25
	var v27 bool = ((uint32(uint32(0x1))) == (uint32(v26)))
	var v28 bool = (!(v27))
	var v29 uint32 = sel32(v28, uint32(uint32(0x1b)), uint32(v23))
	var v30 uint32 = ((uint32((uint32(a)) >> 26)) & uint32(0x1))
	var v31 uint32 = ((uint32((uint32(v30)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v32 uint32 = v31
	var v33 bool = ((uint32(uint32(0x1))) == (uint32(v32)))
	var v34 bool = (!(v33))
	var v35 uint32 = sel32(v34, uint32(uint32(0x1a)), uint32(v29))
	var v36 uint32 = ((uint32((uint32(a)) >> 25)) & uint32(0x1))
	var v37 uint32 = ((uint32((uint32(v36)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v38 uint32 = v37
	var v39 bool = ((uint32(uint32(0x1))) == (uint32(v38)))
	var v40 bool = (!(v39))
	var v41 uint32 = sel32(v40, uint32(uint32(0x19)), uint32(v35))
	var v42 uint32 = ((uint32((uint32(a)) >> 24)) & uint32(0x1))
	var v43 uint32 = ((uint32((uint32(v42)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v44 uint32 = v43
	var v45 bool = ((uint32(uint32(0x1))) == (uint32(v44)))
	var v46 bool = (!(v45))
	var v47 uint32 = sel32(v46, uint32(uint32(0x18)), uint32(v41))
	var v48 uint32 = ((uint32((uint32(a)) >> 23)) & uint32(0x1))
	var v49 uint32 = ((uint32((uint32(v48)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v50 uint32 = v49
	var v51 bool = ((uint32(uint32(0x1))) == (uint32(v50)))
	var v52 bool = (!(v51))
	var v53 uint32 = sel32(v52, uint32(uint32(0x17)), uint32(v47))
	var v54 uint32 = ((uint32((uint32(a)) >> 22)) & uint32(0x1))
	var v55 uint32 = ((uint32((uint32(v54)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v56 uint32 = v55
	var v57 bool = ((uint32(uint32(0x1))) == (uint32(v56)))
	var v58 bool = (!(v57))
	var v59 uint32 = sel32(v58, uint32(uint32(0x16)), uint32(v53))
	var v60 uint32 = ((uint32((uint32(a)) >> 21)) & uint32(0x1))
	var v61 uint32 = ((uint32((uint32(v60)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v62 uint32 = v61
	var v63 bool = ((uint32(uint32(0x1))) == (uint32(v62)))
	var v64 bool = (!(v63))
	var v65 uint32 = sel32(v64, uint32(uint32(0x15)), uint32(v59))
	var v66 uint32 = ((uint32((uint32(a)) >> 20)) & uint32(0x1))
	var v67 uint32 = ((uint32((uint32(v66)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v68 uint32 = v67
	var v69 bool = ((uint32(uint32(0x1))) == (uint32(v68)))
	var v70 bool = (!(v69))
	var v71 uint32 = sel32(v70, uint32(uint32(0x14)), uint32(v65))
	var v72 uint32 = ((uint32((uint32(a)) >> 19)) & uint32(0x1))
	var v73 uint32 = ((uint32((uint32(v72)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v74 uint32 = v73
	var v75 bool = ((uint32(uint32(0x1))) == (uint32(v74)))
	var v76 bool = (!(v75))
	var v77 uint32 = sel32(v76, uint32(uint32(0x13)), uint32(v71))
	var v78 uint32 = ((uint32((uint32(a)) >> 18)) & uint32(0x1))
	var v79 uint32 = ((uint32((uint32(v78)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v80 uint32 = v79
	var v81 bool = ((uint32(uint32(0x1))) == (uint32(v80)))
	var v82 bool = (!(v81))
	var v83 uint32 = sel32(v82, uint32(uint32(0x12)), uint32(v77))
	var v84 uint32 = ((uint32((uint32(a)) >> 17)) & uint32(0x1))
	var v85 uint32 = ((uint32((uint32(v84)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v86 uint32 = v85
	var v87 bool = ((uint32(uint32(0x1))) == (uint32(v86)))
	var v88 bool = (!(v87))
	var v89 uint32 = sel32(v88, uint32(uint32(0x11)), uint32(v83))
	var v90 uint32 = ((uint32((uint32(a)) >> 16)) & uint32(0x1))
	var v91 uint32 = ((uint32((uint32(v90)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v92 uint32 = v91
	var v93 bool = ((uint32(uint32(0x1))) == (uint32(v92)))
	var v94 bool = (!(v93))
	var v95 uint32 = sel32(v94, uint32(uint32(0x10)), uint32(v89))
	var v96 uint32 = ((uint32((uint32(a)) >> 15)) & uint32(0x1))
	var v97 uint32 = ((uint32((uint32(v96)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v98 uint32 = v97
	var v99 bool = ((uint32(uint32(0x1))) == (uint32(v98)))
	var v100 bool = (!(v99))
	var v101 uint32 = sel32(v100, uint32(uint32(0xf)), uint32(v95))
	var v102 uint32 = ((uint32((uint32(a)) >> 14)) & uint32(0x1))
	var v103 uint32 = ((uint32((uint32(v102)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v104 uint32 = v103
	var v105 bool = ((uint32(uint32(0x1))) == (uint32(v104)))
	var v106 bool = (!(v105))
	var v107 uint32 = sel32(v106, uint32(uint32(0xe)), uint32(v101))
	var v108 uint32 = ((uint32((uint32(a)) >> 13)) & uint32(0x1))
	var v109 uint32 = ((uint32((uint32(v108)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v110 uint32 = v109
	var v111 bool = ((uint32(uint32(0x1))) == (uint32(v110)))
	var v112 bool = (!(v111))
	var v113 uint32 = sel32(v112, uint32(uint32(0xd)), uint32(v107))
	var v114 uint32 = ((uint32((uint32(a)) >> 12)) & uint32(0x1))
	var v115 uint32 = ((uint32((uint32(v114)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v116 uint32 = v115
	var v117 bool = ((uint32(uint32(0x1))) == (uint32(v116)))
	var v118 bool = (!(v117))
	var v119 uint32 = sel32(v118, uint32(uint32(0xc)), uint32(v113))
	var v120 uint32 = ((uint32((uint32(a)) >> 11)) & uint32(0x1))
	var v121 uint32 = ((uint32((uint32(v120)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v122 uint32 = v121
	var v123 bool = ((uint32(uint32(0x1))) == (uint32(v122)))
	var v124 bool = (!(v123))
	var v125 uint32 = sel32(v124, uint32(uint32(0xb)), uint32(v119))
	var v126 uint32 = ((uint32((uint32(a)) >> 10)) & uint32(0x1))
	var v127 uint32 = ((uint32((uint32(v126)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v128 uint32 = v127
	var v129 bool = ((uint32(uint32(0x1))) == (uint32(v128)))
	var v130 bool = (!(v129))
	var v131 uint32 = sel32(v130, uint32(uint32(0xa)), uint32(v125))
	var v132 uint32 = ((uint32((uint32(a)) >> 9)) & uint32(0x1))
	var v133 uint32 = ((uint32((uint32(v132)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v134 uint32 = v133
	var v135 bool = ((uint32(uint32(0x1))) == (uint32(v134)))
	var v136 bool = (!(v135))
	var v137 uint32 = sel32(v136, uint32(uint32(0x9)), uint32(v131))
	var v138 uint32 = ((uint32((uint32(a)) >> 8)) & uint32(0x1))
	var v139 uint32 = ((uint32((uint32(v138)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v140 uint32 = v139
	var v141 bool = ((uint32(uint32(0x1))) == (uint32(v140)))
	var v142 bool = (!(v141))
	var v143 uint32 = sel32(v142, uint32(uint32(0x8)), uint32(v137))
	var v144 uint32 = ((uint32((uint32(a)) >> 7)) & uint32(0x1))
	var v145 uint32 = ((uint32((uint32(v144)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v146 uint32 = v145
	var v147 bool = ((uint32(uint32(0x1))) == (uint32(v146)))
	var v148 bool = (!(v147))
	var v149 uint32 = sel32(v148, uint32(uint32(0x7)), uint32(v143))
	var v150 uint32 = ((uint32((uint32(a)) >> 6)) & uint32(0x1))
	var v151 uint32 = ((uint32((uint32(v150)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v152 uint32 = v151
	var v153 bool = ((uint32(uint32(0x1))) == (uint32(v152)))
	var v154 bool = (!(v153))
	var v155 uint32 = sel32(v154, uint32(uint32(0x6)), uint32(v149))
	var v156 uint32 = ((uint32((uint32(a)) >> 5)) & uint32(0x1))
	var v157 uint32 = ((uint32((uint32(v156)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v158 uint32 = v157
	var v159 bool = ((uint32(uint32(0x1))) == (uint32(v158)))
	var v160 bool = (!(v159))
	var v161 uint32 = sel32(v160, uint32(uint32(0x5)), uint32(v155))
	var v162 uint32 = ((uint32((uint32(a)) >> 4)) & uint32(0x1))
	var v163 uint32 = ((uint32((uint32(v162)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v164 uint32 = v163
	var v165 bool = ((uint32(uint32(0x1))) == (uint32(v164)))
	var v166 bool = (!(v165))
	var v167 uint32 = sel32(v166, uint32(uint32(0x4)), uint32(v161))
	var v168 uint32 = ((uint32((uint32(a)) >> 3)) & uint32(0x1))
	var v169 uint32 = ((uint32((uint32(v168)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v170 uint32 = v169
	var v171 bool = ((uint32(uint32(0x1))) == (uint32(v170)))
	var v172 bool = (!(v171))
	var v173 uint32 = sel32(v172, uint32(uint32(0x3)), uint32(v167))
	var v174 uint32 = ((uint32((uint32(a)) >> 2)) & uint32(0x1))
	var v175 uint32 = ((uint32((uint32(v174)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v176 uint32 = v175
	var v177 bool = ((uint32(uint32(0x1))) == (uint32(v176)))
	var v178 bool = (!(v177))
	var v179 uint32 = sel32(v178, uint32(uint32(0x2)), uint32(v173))
	var v180 uint32 = ((uint32((uint32(a)) >> 1)) & uint32(0x1))
	var v181 uint32 = ((uint32((uint32(v180)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v182 uint32 = v181
	var v183 bool = ((uint32(uint32(0x1))) == (uint32(v182)))
	var v184 bool = (!(v183))
	var v185 uint32 = sel32(v184, uint32(uint32(0x1)), uint32(v179))
	var v186 uint32 = ((uint32((uint32(a)) >> 0)) & uint32(0x1))
	var v187 uint32 = ((uint32((uint32(v186)) ^ (uint32(uint32(0x1))))) & uint32(0x1))
	var v188 uint32 = v187
	var v189 bool = ((uint32(uint32(0x1))) == (uint32(v188)))
	var v190 bool = (!(v189))
	var v191 uint32 = sel32(v190, uint32(uint32(0x0)), uint32(v185))
	var v192 uint32 = v191
	var v193 uint32 = uint32(0x0)
	var v194 uint64 = (uint64(((uint64(v193)) << 32) | (uint64(v192))))
	return uint64(v194)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_CTZW__one__rd__go__all_constructed(g0)
	_ = sink
}
