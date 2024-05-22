package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	if input, err := os.ReadFile("14/input.txt"); err == nil {
		deers := make([]Reindeer, 0, 16)
		for _, line := range strings.Split(string(input), "\n") {
			deers = append(deers, Parse(line))
		}

		fmt.Println(part1(deers, 2503))
		fmt.Println(part2(deers, 2503))
	}

}

var re = regexp.MustCompile(`^(\w+) .* (\d+) .* (\d+) .* (\d+) .*`)

type Reindeer struct {
	Name    string
	V, D, R int
	Score   int
}

func Parse(line string) Reindeer {
	m := re.FindStringSubmatch(line)
	v, _ := strconv.Atoi(m[2])
	d, _ := strconv.Atoi(m[3])
	r, _ := strconv.Atoi(m[4])
	return Reindeer{m[1], v, d, r, 0}
}

func part1(deers []Reindeer, duration int) int {
	maxDst := 0
	for _, deer := range deers {
		rem := min(duration%(deer.D+deer.R), deer.D) * deer.V
		dur := (duration/(deer.D+deer.R))*deer.V*deer.D + rem
		maxDst = max(maxDst, dur)
	}
	return maxDst
}

func part2(deers []Reindeer, duration int) int {
	deerMap := make(map[string]*Reindeer, len(deers))
	for _, deer := range deers {
		deerMap[deer.Name] = &deer
	}

	round := make(map[string]int, len(deers))

	for i := 1; i <= duration; i++ {
		maxDst := 0
		for _, deer := range deers {
			rem := min(i%(deer.D+deer.R), deer.D) * deer.V
			dur := (i/(deer.D+deer.R))*deer.V*deer.D + rem
			round[deer.Name] = dur
			maxDst = max(maxDst, dur)
		}

		for k, v := range round {
			if v == maxDst {
				deerMap[k].Score++
			}
		}
	}

	maxScore := 0
	for _, v := range deerMap {
		maxScore = max(maxScore, v.Score)
	}

	return maxScore
}
