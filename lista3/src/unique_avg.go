package main

import (
	"math"
)

// UniqueAvgStruct - structure used in unique_avg algorithm
type UniqueAvgStruct struct {
	M      []float64
	Unique []float64
	h      func(uint32) float64
}

// NewUniqueAvgStruct - constructor for UniqueAvgStruct
func NewUniqueAvgStruct(h func(uint32) float64, m int) *UniqueAvgStruct {
	M := make([]float64, 0, m)
	U := make([]float64, 0, m)
	for i := 0; i <= m; i++ {
		M = append(M, math.Inf(1))
		U = append(U, math.Inf(1))
	}

	E := UniqueAvgStruct{M, U, h}
	return &E
}

// Add - process single element of multiset
func (ua *UniqueAvgStruct) Add(el Element) {
	for k := int32(0); k < int32(len(ua.M)); k++ {
		u := ua.h(concat(el.i, k+1))
		ua.M[k] = math.Min(ua.M[k], -(math.Log(u) / el.l))
		ua.Unique[k] = math.Min(ua.Unique[k], -(math.Log(u) / 1.0))
	}
}

// Estimate - estimate avg of all processed elements
func (ua *UniqueAvgStruct) Estimate() float64 {
	L := 0.0
	for _, val := range ua.M {
		L += val
	}
	L = float64(len(ua.M)-1) / L

	elementCount := 0.0
	for _, val := range ua.Unique {
		elementCount += val
	}
	elementCount = float64(len(ua.Unique)-1) / elementCount

	return L / elementCount
}

func uniqueAvg(set *[]Element, h func(uint32) float64, m int) (float64, float64, float64) {
	ua := NewUniqueAvgStruct(h, m)

	for _, val := range *set {
		ua.Add(val)
	}

	actualAvg := 0.0
	for _, val := range *set {
		actualAvg += val.l
	}
	actualAvg = actualAvg / float64(len(*set))

	estimatedAvg := ua.Estimate()
	// Return estilated sum, actual sum and relative error
	return estimatedAvg, actualAvg, math.Abs(estimatedAvg-actualAvg) / math.Abs(actualAvg)
}
