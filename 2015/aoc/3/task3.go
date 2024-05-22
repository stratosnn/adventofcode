package main

import (
	"aoc/common"
	"fmt"
	"os"
)

func main() {
	if input, err := os.ReadFile("3/input.txt"); err == nil {
		fmt.Println(part1(string(input)))
		fmt.Println(part2(string(input)))
	}
}

type Point = common.Point2D[int]

func part1(s string) int {
	visited := make(map[Point]int, len(s))
	pos := Point{}
	visited[pos] = 1

	for _, c := range s {
		switch c {
		case '>':
			pos.X++
		case '<':
			pos.X--
		case '^':
			pos.Y++
		case 'v':
			pos.Y--
		}
		visited[pos]++
	}
	return len(visited)
}

func part2(s string) int {
	visited := make(map[Point]int, len(s))
	posSanta := Point{}
	posRobot := Point{}
	visited[posSanta] = 2

	for ix, c := range s {
		pos := (map[bool]*Point{true: &posSanta, false: &posRobot})[ix%2 == 0]
		switch c {
		case '>':
			pos.X++
		case '<':
			pos.X--
		case '^':
			pos.Y++
		case 'v':
			pos.Y--
		}
		visited[*pos]++
	}
	return len(visited)
}
