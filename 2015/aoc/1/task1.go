package main

import (
	"fmt"
	"os"
)

func main() {
	if input, err := os.ReadFile("1/input.txt"); err == nil {
		fmt.Println(part1(string(input)))
		fmt.Println(part2(string(input)))
	}
}

func part1(str string) int {
	floor := 0
	for _, char := range str {
		switch char {
		case '(':
			floor++
		case ')':
			floor--
		}
	}
	return floor
}

func part2(str string) int {
	floor := 0
	for ix, char := range str {
		switch char {
		case '(':
			floor++
		case ')':
			floor--
		}
		if floor == -1 {
			return ix + 1
		}
	}
	return -1
}
