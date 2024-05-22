package main

import (
	"fmt"
)

func main() {
	input := 33100000

	fmt.Println(part1(input))
	fmt.Println(part2(input))

}

func dividers(n int) []int {
	divs := make([]int, 0, 16)
	for i := 1; i*i <= n; i++ {
		if n%i == 0 {
			divs = append(divs, i)
			if i != n/i {
				divs = append(divs, n/i)
			}
		}
	}
	return divs
}

func part1(input int) int {
	presents := 0
	i := 1

	for presents < input {
		presents = 0
		for _, d := range dividers(i) {
			presents += d * 10
		}
		i++
	}
	return i - 1
}

func part2(input int) int {
	presents := 0
	i := 1

	for presents < input {
		presents = 0
		for _, d := range dividers(i) {
			if i/d <= 50 {
				presents += d * 11
			}
		}
		i++
	}
	return i - 1
}
