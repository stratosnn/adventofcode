package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)
import "github.com/emirpasic/gods/sets/hashset"

func main() {
	if input, err := os.ReadFile("16/input.txt"); err == nil {
		sueSet := Parse(string(input))
		traceAsSet := hashset.New(
			" children: 3",
			" cats: 7",
			" samoyeds: 2",
			" pomeranians: 3",
			" akitas: 0",
			" vizslas: 0",
			" goldfish: 5",
			" trees: 3",
			" cars: 2",
			" perfumes: 1",
		)

		fmt.Println(part1(traceAsSet, sueSet))
		sueMap := Parse2(string(input))
		trace := map[string]int{
			"children:":    3,
			"cats:":        7,
			"samoyeds:":    2,
			"pomeranians:": 3,
			"akitas:":      0,
			"vizslas:":     0,
			"goldfish:":    5,
			"trees:":       3,
			"cars:":        2,
			"perfumes:":    1,
		}

		fmt.Println(part2(trace, sueMap))
		// 373 too high
	}

}

func Parse(input string) map[int]*hashset.Set {
	sueSet := map[int]*hashset.Set{}
	for _, line := range strings.Split(input, "\n") {
		fc := strings.Index(line, ":")
		id, err := strconv.Atoi(strings.Split(line[:fc], " ")[1])
		if err != nil {
			panic(err)
		}
		traces := strings.Split(line[fc+1:], ",")
		sueSet[id] = hashset.New()
		for _, trace := range traces {
			sueSet[id].Add(trace)
		}
	}
	return sueSet
}

func Parse2(input string) map[int]map[string]int {
	sueMap := map[int]map[string]int{}
	for _, line := range strings.Split(input, "\n") {
		fc := strings.Index(line, ":")
		id, err := strconv.Atoi(strings.Split(line[:fc], " ")[1])
		if err != nil {
			panic(err)
		}
		traces := strings.Split(line[fc+1:], ",")
		sueMap[id] = make(map[string]int, 8)
		for _, trace := range traces {
			s := strings.Split(trace, " ")
			cnt, err := strconv.Atoi(s[2])
			if err != nil {
				panic(err)
			}
			sueMap[id][s[1]] = cnt
		}
	}
	return sueMap
}

func part1(trace *hashset.Set, sueMap map[int]*hashset.Set) int {
	for k, v := range sueMap {
		if trace.Intersection(v).Size() == v.Size() {
			return k
		}
	}
	return -1
}

func part2(trace map[string]int, sueMap map[int]map[string]int) int {
	for sue, traces := range sueMap {
		matches := 0
		for name, quantity := range traces {
			t, exists := trace[name]
			if !exists {
				continue
			}
			switch name {
			case "cats:", "trees:":
				if quantity > t {
					matches++
				}
			case "pomeranians:", "goldfish:":
				if quantity < t {
					matches++
				}
			default:
				if quantity == t {
					matches++
				}
			}
		}
		if matches == len(traces) {
			return sue
		}
	}
	return -1
}
