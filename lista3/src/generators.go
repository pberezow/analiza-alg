package main

import "math/rand"

// set generator - const lambda values with some % anomaly
func makeSetConstGenerator(lambda, anomaly float64) func(int32) *[]Element {
	currID := int32(1)

	return func(size int32) *[]Element {
		set := make([]Element, 0, size)
		for i := int32(0); i < size; i++ {
			if r := rand.Float64(); r < anomaly {
				// add random lambda
				l := rand.Float64() * 1000000.0
				set = append(set, Element{i + currID, l})
			} else {
				// add const lambda
				set = append(set, Element{i + currID, lambda})
			}
		}

		currID += size
		return &set
	}
}

// set generator - lambda values from range [lambdaMin, lambdaMax]
func makeSetFromRangeGenerator(lambdaMin, lambdaMax float64) func(int32) *[]Element {
	currID := int32(1)

	return func(size int32) *[]Element {
		set := make([]Element, 0, size)
		for i := int32(0); i < size; i++ {
			lambda := (rand.Float64() * (lambdaMax - lambdaMin)) + lambdaMin
			set = append(set, Element{i + currID, lambda})
		}

		currID += size
		return &set
	}
}
