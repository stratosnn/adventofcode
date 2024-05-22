package main

import (
	"cmp"
	"fmt"
	"os"
	"regexp"
	"slices"
	"strconv"
	"strings"
)

func main() {
	if input, err := os.ReadFile("9/input.txt"); err == nil {
		list := strings.Split(string(input), "\n")
		index, grid := parse(list)
		fmt.Println(part1and2(index, grid, slices.Min[[]int]))
		fmt.Println(part1and2(index, grid, slices.Max[[]int]))
	}
}

var re = regexp.MustCompile(`^(\w+) to (\w+) = (\d+)$`)

func parse(list []string) (map[string]int, [][]int) {
	indexMap := make(map[string]int)
	globalIx := 0
	for _, line := range list {
		match := re.FindStringSubmatch(line)
		if match == nil {
			panic("RegExp does not match")
		}
		// Generate name to to index map
		for i := 1; i <= 2; i++ {
			if _, ok := indexMap[match[i]]; !ok {
				indexMap[match[i]] = globalIx
				globalIx++
			}
		}
	}
	// now generate distance matrix
	cnt := len(indexMap)
	dist := make([][]int, cnt)
	for i := range dist {
		dist[i] = make([]int, cnt)
	}
	for _, line := range list {
		match := re.FindStringSubmatch(line)
		if match == nil {
			panic("RegExp does not match")
		}
		d, _ := strconv.Atoi(match[3])
		dist[indexMap[match[1]]][indexMap[match[2]]] = d
		dist[indexMap[match[2]]][indexMap[match[1]]] = d
	}
	return indexMap, dist
}

func tsp[S ~[]E, E cmp.Ordered](index map[string]int, grid [][]int, cur *string, others []string, comp func(x S) E) E {
	if len(others) == 0 {
		return E(0)
	}
	results := make(S, 0, len(others))
	for ix, other := range others {
		dst := 0
		if cur != nil {
			dst = grid[index[*cur]][index[other]]
		}
		newOthers := removeIx(others, ix)
		results = append(results, E(dst)+tsp(index, grid, &other, newOthers, comp))
	}
	return comp(results)
}

func part1and2[S ~[]E, E cmp.Ordered](index map[string]int, grid [][]int, comp func(x S) E) E {
	all := make([]string, 0, len(index))
	for key := range index {
		all = append(all, key)
	}
	return tsp(index, grid, nil, all, comp)
}

// For this exercise we need to force copy list of other cities
// re-slicing will modify underlying array and that we don't want
func removeIx[T any](orig []T, ix int) []T {
	sliced := append([]T{}, orig[:ix]...)
	sliced = append(sliced, orig[ix+1:]...)
	return sliced
}
