package main

import (
	"encoding/csv"
	"fmt"
	"os"
)

func zad2PlotAvg(filePath string, nLower, nUpper, m int, h func(uint32) float64, setGenerator func(int32) *[]Element, title string) {
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
		estimatedAvg, actualAvg, _ := uniqueAvg(s, h, m)
		results = append(results, []string{
			fmt.Sprintf("%d", n),
			fmt.Sprintf("%f", estimatedAvg),
			fmt.Sprintf("%f", actualAvg)})
	}

	for _, row := range results {
		_ = writer.Write(row)
	}
}

func zad2() {
	zad2PlotAvg("./unique_avg_data/zad1_m=10.csv", 1, 1000, 10, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_AVG: m=50 const anomaly=0")
	zad2PlotAvg("./unique_avg_data/zad1_m=50.csv", 1, 1000, 50, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_AVG: m=50 const anomaly=0")
	zad2PlotAvg("./unique_avg_data/zad1_m=100.csv", 1, 1000, 100, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_AVG: m=100 const anomaly=0")
	zad2PlotAvg("./unique_avg_data/zad1_m=200.csv", 1, 1000, 200, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_AVG: m=200 const anomaly=0")
	zad2PlotAvg("./unique_avg_data/zad1_m=400.csv", 1, 1000, 400, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_AVG: m=400 const anomaly=0")

	zad2PlotAvg("./unique_avg_data/zad1_const_0.csv", 1, 1000, 100, hash1, makeSetConstGenerator(100.0, 0.0), "UNIQUE_AVG: m=100 const anomaly=0")
	zad2PlotAvg("./unique_avg_data/zad1_const_1.csv", 1, 1000, 100, hash1, makeSetConstGenerator(100.0, 1.0), "UNIQUE_AVG: m=100 const anomaly=1")
	zad2PlotAvg("./unique_avg_data/zad1_const_5.csv", 1, 1000, 100, hash1, makeSetConstGenerator(100.0, 5.0), "UNIQUE_AVG: m=100 const anomaly=5")

	zad2PlotAvg("./unique_avg_data/zad1_range_1_10.csv", 1, 1000, 100, hash1, makeSetFromRangeGenerator(1.0, 10.0), "UNIQUE_AVG: m=100 range=(1; 10)")
	zad2PlotAvg("./unique_avg_data/zad1_range_1_1000.csv", 1, 1000, 100, hash1, makeSetFromRangeGenerator(1.0, 1000.0), "UNIQUE_AVG: m=100 range=(1; 1000)")
	zad2PlotAvg("./unique_avg_data/zad1_range_1000_2000.csv", 1, 1000, 100, hash1, makeSetFromRangeGenerator(1000.0, 2000.0), "UNIQUE_AVG: m=100 range=(1000; 2000)")
}
