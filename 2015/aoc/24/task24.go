package main

import (
	"fmt"
	"github.com/m4gshm/gollections/slice/sum"
	"math"
	"os"
	"slices"
	"sort"
	"strconv"
	"strings"
)

func main() {
	if input, err := os.ReadFile("24/input.txt"); err == nil {
		packages := make([]int, 0)
		for _, line := range strings.Fields(string(input)) {
			p, _ := strconv.Atoi(line)
			packages = append(packages, p)
		}
		sort.Ints(packages)
		slices.Reverse(packages)

		fmt.Println(part1(packages))
		fmt.Println(part2(packages))

	}
}

func part1(packages []int) int {
	targetWeight := sum.Of(packages) / 3

	_, qe := ssp(packages, -1, 0, targetWeight, 0, 1)
	return qe
}

func part2(packages []int) int {
	targetWeight := sum.Of(packages) / 4

	_, qe := ssp(packages, -1, 0, targetWeight, 0, 1)
	return qe
}

func ssp(packages []int, ix, sum, targetWeight int, sz, qe int) (int, int) {
	if sum == targetWeight {
		return sz, qe
	}
	if ix+1 >= len(packages) {
		return math.MaxInt16, math.MaxInt16
	}

	sza, qea := ssp(packages, ix+1, sum, targetWeight, sz, qe)
	szb, qeb := ssp(packages, ix+1, sum+packages[ix+1], targetWeight, sz+1, qe*packages[ix+1])
	if sza < szb {
		return sza, qea
	} else if sza > szb {
		return szb, qeb
	} else if qea < qeb {
		return sza, qea
	} else if qea > qeb {
		return szb, qeb
	} else {
		return sza, qea
	}
}
