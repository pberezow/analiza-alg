package main

import (
	"fmt"
	"math"
)

type edge struct {
	v1 int
	v2 int
}

func indexToConf(index int, n int) []int {
	conf := make([]int, n)

	for i := n - 1; i >= 0; i-- {
		val := index / int(math.Pow(float64(n+1), float64(i)))
		conf[i] = val
		index -= val * int(math.Pow(float64(n+1), float64(i)))
	}

	return conf
}

func confToIndex(conf []int) int {
	index := 0
	n := len(conf)
	for i := 0; i < n; i++ {
		index += conf[i] * int(math.Pow(float64(n+1), float64(i)))
	}
	return index
}

func getConfigurations(n int) []bool {
	return make([]bool, int(math.Pow(float64(n+1), float64(n))))
}

func getSafeConfigurations(n int) []int {
	confs := make([]int, n+1)
	safeConf := make([]int, n)
	for i := 0; i <= n; i++ {
		for j := 0; j < len(safeConf); j++ {
			safeConf[j] = i
		}
		safeIdx := confToIndex(safeConf)
		confs[i] = safeIdx
	}

	return confs
}

func getTransitions(conf []int) [][]int {
	transitions := make([][]int, 0)

	if conf[0] == conf[len(conf)-1] {
		newConf := make([]int, len(conf))
		_ = copy(newConf, conf)
		newConf[0] = (newConf[0] + 1) % (len(conf) + 1)
		transitions = append(transitions, newConf)
	}

	for i := 1; i < len(conf); i++ {
		if conf[i] != conf[i-1] {
			newConf := make([]int, len(conf))
			_ = copy(newConf, conf)
			newConf[i] = newConf[i-1]
			transitions = append(transitions, newConf)
		}
	}

	return transitions
}

func traverse(actualConf []int, configurations *[]bool, edges *[]edge) {
	idx := confToIndex(actualConf)
	if (*configurations)[idx] == true {
		return
	}
	(*configurations)[idx] = true

	transitions := getTransitions(actualConf)
	for _, conf := range transitions {
		i := confToIndex(conf)
		*edges = append(*edges, edge{idx, i})
		if (*configurations)[i] == true {
			continue
		}
		traverse(conf, configurations, edges)
	}
}

func convertListOfEdges(listOfEdges *[]edge, numOfVertices int) [][]int {
	edges := make([][]int, numOfVertices)

	for _, e := range *listOfEdges {
		edges[e.v2] = append(edges[e.v2], e.v1)
	}

	return edges
}

func isSafeConf(conf int, safeConfs []int) bool {
	for _, sc := range safeConfs {
		if sc == conf {
			return true
		}
	}
	return false
}

func getLongestPath(edges *[][]int, safeConfs []int, currIdx int, isRoot bool) int {
	if isSafeConf(currIdx, safeConfs) && !isRoot {
		return 0
	}

	pathLen := 0
	for _, v1 := range (*edges)[currIdx] {
		l := getLongestPath(edges, safeConfs, v1, false)
		if l > pathLen {
			pathLen = l
		}
	}

	return 1 + pathLen
}

func simulation(n int) {
	configurations := getConfigurations(n)
	edges := make([]edge, 0)

	for i := 0; i < len(configurations); i++ {
		conf := indexToConf(i, n)
		traverse(conf, &configurations, &edges)
	}

	safeConfs := getSafeConfigurations(n)
	convertedEdges := convertListOfEdges(&edges, len(configurations))

	longestPath := 0
	for _, sc := range safeConfs {
		pathLen := getLongestPath(&convertedEdges, safeConfs, sc, true)
		if pathLen > longestPath {
			longestPath = pathLen
		}
	}

	fmt.Println("Longest path: ", longestPath)
	// fmt.Println(configurations)
}

func main() {
	simulation(6)
}
