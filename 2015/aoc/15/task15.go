package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	if input, err := os.ReadFile("15/input.txt"); err == nil {
		props := make([]Ingredient, 0, 8)
		for _, line := range strings.Split(string(input), "\n") {
			props = append(props, Parse(line))
		}
		fmt.Println(part1(props))
		fmt.Println(part2(props))
	}
}

type Ingredient [5]int

func Parse(line string) Ingredient {
	var c, d, f, t, cal int
	var name string
	pattern := "%s capacity %d, durability %d, flavor %d, texture %d, calories %d"
	if _, err := fmt.Sscanf(line, pattern, &name, &c, &d, &f, &t, &cal); err != nil {
		panic(err)
	}

	return Ingredient{c, d, f, t, cal}
}

func part1(p []Ingredient) int {
	score := 0
	for i := 0; i <= 100; i++ {
		for j := 0; i+j <= 100; j++ {
			for k := 0; k+i+j <= 100; k++ {
				l := 100 - i - j - k
				newScore := 1
				for px := 0; px < 4; px++ {
					newScore *= max(p[0][px]*i+p[1][px]*j+p[2][px]*k+p[3][px]*l, 0)
				}
				score = max(score, newScore)
			}
		}
	}
	return score
}

func part2(p []Ingredient) int {
	score := 0
	for i := 0; i <= 100; i++ {
		for j := 0; i+j <= 100; j++ {
			for k := 0; k+i+j <= 100; k++ {
				l := 100 - i - j - k
				if p[0][4]*i+p[1][4]*j+p[2][4]*k+p[3][4]*l != 500 {
					continue
				}

				newScore := 1
				for px := 0; px < 4; px++ {
					newScore *= max(p[0][px]*i+p[1][px]*j+p[2][px]*k+p[3][px]*l, 0)
				}
				score = max(score, newScore)
			}
		}
	}
	return score
}
