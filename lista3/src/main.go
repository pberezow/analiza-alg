package main

import (
	"math"
	"math/rand"
)

// Element of multiset
type Element struct {
	i int32
	l float64
}

func reverse(val int32) (uint32, int32) {
	valBCount := int32(0)
	val1 := uint32(val)
	revVal := uint32(0)

	for val1 > 0 {
		valBCount++
		revVal <<= 1
		if val1%2 == 1 {
			revVal++
		}
		val1 >>= 1
	}

	return revVal, valBCount
}

func concat(i, k int32) uint32 {
	revK, kBCount := reverse(k)
	result := uint32(i)

	for kBCount > 0 {
		kBCount--
		result <<= 1
		if revK%2 == 1 {
			result++
		}
		revK >>= 1
	}

	return result
}

// HASH FUNCTIONS
func hash1(x uint32) float64 {
	w := uint32((1 << 31) + ((1 << 31) - 1))
	x = ((x >> 16) ^ x) * 0x45d9f3b
	x = ((x >> 16) ^ x) * 0x45d9f3b
	x = (x >> 16) ^ x
	return float64(x) / float64(w)
}

func hash2(x uint32) float64 {
	w := uint32((1 << 31) + ((1 << 31) - 1))
	x ^= (x << 13)
	x ^= (x >> 17)
	x ^= (x << 5)
	return float64(x) / float64(w)
}

func shiftHash(x uint32) float64 {
	w := uint32((1 << 31) + ((1 << 31) - 1))
	return float64(x>>22) / float64(w)
}

func fibHash(x uint32) float64 {
	w := uint32((1 << 31) + ((1 << 31) - 1))
	A := math.Floor(float64(w) / 1.6180339)
	return float64(uint32(A)*x) / float64(w)
}

// create set with lambda values from range [from, to]
func makeSet(from, to float64, size int32, firstID int32) *[]Element {
	set := make([]Element, 0, size)
	for i := int32(0); i < size; i++ {
		l := (rand.Float64() * (to - from)) + from
		set = append(set, Element{i + firstID, l})
	}

	return &set
}

func main() {
	zad1()
	zad2()
	// from := 1.0
	// to := 1000.0
	// size := int32(10000)
	// h := hash
	// set := makeSet(from, to, size, 1)

	// start := time.Now()

	// result, _, relativeError := uniqueSum(set, h, 50)

	// fmt.Println("Elapsed: ", time.Since(start).Seconds(), " sec")
	// fmt.Println("Estimated sum: ", result, "   Relative error: ", relativeError)
}
