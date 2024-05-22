package main

import (
	"aoc/common"
	"fmt"
	"os"
	"strings"
)

func main() {
	if input, err := os.ReadFile("18/input.txt"); err == nil {
		grid := Parse(string(input))
		fmt.Println(part1(grid, 100))
		grid = Parse(string(input))
		fmt.Println(part2(grid, 100))
	}
}

func Parse(line string) map[common.Point2D[int]]bool {
	grid := make(map[common.Point2D[int]]bool)
	for x, line := range strings.Split(line, "\n") {
		for y, c := range line {
			grid[common.Point2D[int]{x, y}] = map[int32]bool{'.': false, '#': true}[c]
		}
	}
	return grid
}

func part1(grid map[common.Point2D[int]]bool, num int) int {
	newGrid := make(map[common.Point2D[int]]bool, len(grid))
	for it := 0; it < num; it++ {
		for p, l := range grid {
			n := p.Neighbours()
			nCnt := Count(grid, n)
			if l {
				newGrid[p] = map[int]bool{2: true, 3: true}[nCnt]
			} else {
				newGrid[p] = map[int]bool{3: true}[nCnt]
			}
		}
		grid, newGrid = newGrid, grid
	}
	cnt := 0
	for _, v := range grid {
		if v {
			cnt++
		}
	}
	return cnt
}

func part2(grid map[common.Point2D[int]]bool, num int) int {
	corners := []common.Point2D[int]{
		{0, 0},
		{0, 99},
		{99, 99},
		{99, 0},
	}
	for _, p := range corners {
		grid[p] = true
	}

	newGrid := make(map[common.Point2D[int]]bool, len(grid))
	for it := 0; it < num; it++ {
		for p, l := range grid {
			n := p.Neighbours()
			nCnt := Count(grid, n)
			if l {
				newGrid[p] = map[int]bool{2: true, 3: true}[nCnt]
			} else {
				newGrid[p] = map[int]bool{3: true}[nCnt]
			}
		}
		for _, p := range corners {
			newGrid[p] = true
		}
		grid, newGrid = newGrid, grid
	}
	cnt := 0
	for _, v := range grid {
		if v {
			cnt++
		}
	}
	return cnt
}

func Count(grid map[common.Point2D[int]]bool, points []common.Point2D[int]) int {
	cnt := 0
	for _, p := range points {
		if grid[p] {
			cnt++
		}
	}
	return cnt
}
