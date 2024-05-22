package main

import (
	"aoc/common"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	if input, err := os.ReadFile("13/input.txt"); err == nil {
		index, grid := Parse(string(input))
		fmt.Println(part1(index, grid))
		fmt.Println(part2(index, grid))
	}
}

func Parse(input string) (map[string]int, [][]int) {
	index := make(map[string]int, 16)
	globalIx := 0
	lines := strings.Split(input, "\n")

	// name to index
	for _, line := range lines {
		groups := strings.Split(line[:len(line)-1], " ")
		for i := 0; i < 11; i += 10 {
			if _, ok := index[groups[i]]; !ok {
				index[groups[i]] = globalIx
				globalIx++
			}
		}
	}

	// happiness grid pre-allocate
	cnt := len(index)
	grid := make([][]int, cnt)
	for i := range grid {
		grid[i] = make([]int, cnt)
	}
	// populate happiness grid
	for _, line := range lines {
		groups := strings.Split(line[:len(line)-1], " ")
		level, _ := strconv.Atoi(groups[3])
		if groups[2] == "lose" {
			level *= -1
		}

		grid[index[groups[0]]][index[groups[10]]] = level
	}
	return index, grid
}

func CalcHappiness(grid [][]int, arrangement []int) int {
	score := 0
	for ix, p := range arrangement {
		score += grid[p][arrangement[(ix+1)%len(arrangement)]]
		score += grid[p][arrangement[(ix-1+len(arrangement))%len(arrangement)]]
	}
	return score
}

func part1(index map[string]int, grid [][]int) (m int) {
	orig := make([]int, 0, len(index))
	for _, val := range index {
		orig = append(orig, val)
	}
	m = CalcHappiness(grid, orig)

	for p := make([]int, len(orig)); p[0] < len(p); common.NextPerm(p) {
		m = max(m, CalcHappiness(grid, common.GetPerm(orig, p)))
	}
	return m
}

func part2(index map[string]int, grid [][]int) (m int) {
	index["Myself"] = len(index)

	grid = append(grid, make([]int, len(grid)))
	for i := range grid {
		grid[i] = append(grid[i], 0)
	}

	orig := make([]int, 0, len(index))
	for _, val := range index {
		orig = append(orig, val)
	}
	m = CalcHappiness(grid, orig)

	for p := make([]int, len(orig)); p[0] < len(p); common.NextPerm(p) {
		m = max(m, CalcHappiness(grid, common.GetPerm(orig, p)))
	}
	return m
}
