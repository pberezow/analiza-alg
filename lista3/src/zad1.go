package main

import (
	"encoding/csv"
	"fmt"
	"os"
)

func zad1Plot(filePath string, nLower, nUpper, m int, h func(uint32) float64, setGenerator func(int32) *[]Element, title string) {
	file, err := os.Create(filePath)
	if err != nil {
		fmt.Println("Cannot create file", err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	results := [][]string{
		{
			fmt.Sprintf("%d", m),
			fmt.Sprintf("%s", title),
		},
	}

	for n := int32(nLower); n <= int32(nUpper); n++ {
		s := setGenerator(n)
		estimatedSum, actualSum, _ := uniqueSum(s, h, m)
		results = append(results, []string{
			fmt.Sprintf("%d", n),
			fmt.Sprintf("%f", estimatedSum),
			fmt.Sprintf("%f", actualSum)})
	}

	for _, row := range results {
		_ = writer.Write(row)
	}
}

func zad1() {
	// different hash functions
	zad1Plot("./unique_sum_data/zad1_hash1_const.csv", 1, 1000, 100, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=100 const hash1")
	zad1Plot("./unique_sum_data/zad1_hash2_const.csv", 1, 1000, 100, hash2, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=100 const hash2")
	zad1Plot("./unique_sum_data/zad1_fibhash_const.csv", 1, 1000, 100, fibHash, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=100 const fibHash")
	zad1Plot("./unique_sum_data/zad1_shifthash_const.csv", 1, 1000, 100, shiftHash, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=100 const shiftHash")
	zad1Plot("./unique_sum_data/zad1_hash1_range.csv", 1, 1000, 100, hash1, makeSetFromRangeGenerator(1.0, 1000.0), "UNIQUE_SUM: m=100 range=(1; 1000) hash1")
	zad1Plot("./unique_sum_data/zad1_hash2_range.csv", 1, 1000, 100, hash2, makeSetFromRangeGenerator(1.0, 1000.0), "UNIQUE_SUM: m=100 range=(1; 1000) hash2")
	zad1Plot("./unique_sum_data/zad1_fibhash_range.csv", 1, 1000, 100, fibHash, makeSetFromRangeGenerator(1.0, 1000.0), "UNIQUE_SUM: m=100 range=(1; 1000) fibHash")
	zad1Plot("./unique_sum_data/zad1_shifthash_range.csv", 1, 1000, 100, shiftHash, makeSetFromRangeGenerator(1.0, 1000.0), "UNIQUE_SUM: m=100 range=(1; 1000) shiftHash")

	// different m values
	zad1Plot("./unique_sum_data/zad1_m=10.csv", 1, 1000, 10, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=50 const anomaly=0")
	zad1Plot("./unique_sum_data/zad1_m=50.csv", 1, 1000, 50, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=50 const anomaly=0")
	zad1Plot("./unique_sum_data/zad1_m=100.csv", 1, 1000, 100, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=100 const anomaly=0")
	zad1Plot("./unique_sum_data/zad1_m=200.csv", 1, 1000, 200, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=200 const anomaly=0")
	zad1Plot("./unique_sum_data/zad1_m=400.csv", 1, 1000, 400, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=400 const anomaly=0")

	// m = 100, lambda const
	zad1Plot("./unique_sum_data/zad1_const_0.csv", 1, 1000, 100, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_SUM: m=100 const anomaly=0")
	zad1Plot("./unique_sum_data/zad1_const_1.csv", 1, 1000, 100, hash1, makeSetConstGenerator(100.0, 1.0), "UNIQUE_SUM: m=100 const anomaly=1")
	zad1Plot("./unique_sum_data/zad1_const_5.csv", 1, 1000, 100, hash1, makeSetConstGenerator(100.0, 5.0), "UNIQUE_SUM: m=100 const anomaly=5")

	// m = 100 lambda from range
	zad1Plot("./unique_sum_data/zad1_range_1_10.csv", 1, 1000, 100, hash1, makeSetFromRangeGenerator(1.0, 10.0), "UNIQUE_SUM: m=100 range=(1; 10)")
	zad1Plot("./unique_sum_data/zad1_range_1_1000.csv", 1, 1000, 100, hash1, makeSetFromRangeGenerator(1.0, 1000.0), "UNIQUE_SUM: m=100 range=(1; 1000)")
	zad1Plot("./unique_sum_data/zad1_range_1000_2000.csv", 1, 1000, 100, hash1, makeSetFromRangeGenerator(1000.0, 2000.0), "UNIQUE_SUM: m=100 range=(1000; 2000)")
}
