package main

import (
	"fmt"
	"os"
	"slices"
	"sort"
	"strconv"
	"strings"
)

func main() {
	if input, err := os.ReadFile("17/input.txt"); err == nil {
		containers := make([]int, 0, 16)
		for _, cs := range strings.Split(string(input), "\n") {
			c, _ := strconv.Atoi(cs)
			containers = append(containers, c)
		}
		sort.Ints(containers)
		slices.Reverse(containers)

		fmt.Println(part1(containers, 150))
		fmt.Println(part2(containers, 150))
	}
}

func part1(containers []int, sum int) int {
	cnt := 0
	var dp func(i, s int)
	dp = func(i, s int) {
		if s == sum {
			cnt++
			return
		}
		if i >= len(containers)-1 {
			return
		}
		dp(i+1, s)
		dp(i+1, s+containers[i+1])
	}
	dp(-1, 0)

	return cnt
}

func part2(containers []int, sum int) int {
	cnt := map[int]int{}
	var dp func(i, s, num int)
	dp = func(i, s, num int) {
		if s == sum {
			cnt[num]++
			return
		}
		if i >= len(containers)-1 {
			return
		}
		dp(i+1, s, num)
		dp(i+1, s+containers[i+1], num+1)
	}
	dp(-1, 0, 0)

	for i := 1; i < len(containers); i++ {
		num, exists := cnt[i]
		if exists {
			return num
		}
	}

	return -1
}
