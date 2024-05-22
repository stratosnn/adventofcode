package main

import (
	"aoc/common"
	"fmt"
	"os"
	"strings"
)

func main() {
	if input, err := os.ReadFile("5/input.txt"); err == nil {
		list := strings.Split(string(input), "\n")
		fmt.Println(IsNice(list, IsNiceForPart1))
		fmt.Println(IsNice(list, IsNiceForPart2))
	}
}

func IsNice(input []string, pred func(str string) bool) int {
	nice := 0
	for _, line := range input {
		if pred(line) {
			nice++
		}
	}
	return nice
}

func IsNiceForPart1(str string) bool {
	counter := common.CounterStr(str)
	hasVowels := counter['a']+counter['e']+counter['i']+counter['o']+counter['u'] >= 3

	hasConsecutiveChars := HasConsecutiveChars(str)

	hasSubstring := strings.Count(str, "ab")+
		strings.Count(str, "cd")+
		strings.Count(str, "pq")+
		strings.Count(str, "xy") > 0

	return hasVowels && hasConsecutiveChars && !hasSubstring
}

func IsNiceForPart2(str string) bool {
	return HasAtlLeastTwoPairs(str) && HasSymmetricalPair(str)
}

func HasConsecutiveChars(str string) bool {
	for i := 1; i < len(str); i++ {
		if str[i-1] == str[i] {
			return true
		}
	}
	return false
}

func HasSymmetricalPair(str string) bool {
	for i := 1; i < len(str)-1; i++ {
		if str[i-1] == str[i+1] {
			return true
		}
	}
	return false
}

func HasAtlLeastTwoPairs(str string) bool {
	for i := 0; i < len(str)-2; i++ {
		if strings.Index(str[i+2:], str[i:i+2]) >= 0 {
			return true
		}
	}
	return false
}
