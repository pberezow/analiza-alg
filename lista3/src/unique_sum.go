package main

import (
	"math"
)

// UniqueSumStruct - structure used in unique_sum algorithm
type UniqueSumStruct struct {
	M []float64
	h func(uint32) float64
}

// NewUniqueSumStruct - constructor for UniqueSumStruct
func NewUniqueSumStruct(h func(uint32) float64, m int) *UniqueSumStruct {
	M := make([]float64, 0, m)
	for i := 0; i <= m; i++ {
		M = append(M, math.Inf(1))
	}

	E := UniqueSumStruct{M, h}
	return &E
}

// Add - process single element of multiset
func (us *UniqueSumStruct) Add(el Element) {
	for k := int32(0); k < int32(len(us.M)); k++ {
		u := us.h(concat(el.i, k+1))
		us.M[k] = math.Min(us.M[k], -(math.Log(u) / el.l))
	}
}

// Estimate - estimate sum of all processed elements
func (us *UniqueSumStruct) Estimate() float64 {
	L := 0.0
	for _, val := range us.M {
		L += val
	}
	L = float64(len(us.M)-1) / L

	return L
}

func uniqueSum(set *[]Element, h func(uint32) float64, m int) (float64, float64, float64) {
	us := NewUniqueSumStruct(h, m)

	for _, val := range *set {
		us.Add(val)
	}

	actualSum := 0.0
	for _, val := range *set {
		actualSum += val.l
	}

	estimatedSum := us.Estimate()
	// Return estilated sum, actual sum and relative error
	return estimatedSum, actualSum, math.Abs(estimatedSum-actualSum) / math.Abs(actualSum)
}
