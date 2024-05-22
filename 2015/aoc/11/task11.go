package main

import (
	"fmt"
)

func main() {
	input := "hxbxwxba"
	res := part1and2(input)
	fmt.Println(res)
	input2 := string(Inc([]uint8(res)))
	fmt.Println(part1and2(input2))
}

func part1and2(input string) string {
	str := []uint8(input)
	for {
		if Has3ConsecutiveChars(str) && HasAtlLeastTwoPairs(str) {
			return string(str)
		}
		Next(str)
	}
}

func Has3ConsecutiveChars(str []uint8) bool {
	if len(str) < 3 {
		return false
	}
	for i := 1; i < len(str)-1; i++ {
		if str[i-1]+1 == str[i] && str[i] == str[i+1]-1 {
			return true
		}
	}
	return false
}

var forbiddenChars = []uint8{'i', 'o', 'l'}

const filler = "aaaaaaaa"

func Next(str []uint8) []uint8 {
	for _, c := range forbiddenChars {
		if ix := IndexOf(str, c); ix >= 0 {
			str[ix] = c + 1
			copy(str[ix+1:], filler[:(len(str)-ix-1)])
			return str
		}
	}
	return Inc(str)
}

func IndexOf[T comparable](collection []T, el T) int {
	for i, x := range collection {
		if x == el {
			return i
		}
	}
	return -1
}

func Inc(str []uint8) []uint8 {
	str[len(str)-1] = str[len(str)-1] + 1
	for i := len(str) - 1; i >= 0; i-- {
		if str[i] == 'z'+1 {
			str[i] = 'a'
			str[i-1]++
		}
	}
	return str
}

func HasAtlLeastTwoPairs(str []uint8) bool {
	cnt := 0
	for i := 0; i < len(str)-1; i++ {
		if str[i] == str[i+1] {
			cnt++
			i++
		}
	}
	return cnt >= 2
}
