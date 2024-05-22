package main

import (
	"fmt"
	"strings"
)

func main() {
	input := "1113222113"
	fmt.Println(part1and2(input, 40))
	fmt.Println(part1and2(input, 50))
}

type Pair[K, V any] struct {
	Key   K
	Value V
}

func part1and2(input string, iterations int) int {
	for i := 0; i < iterations; i++ {
		input = transform(input)
	}
	return len(input)
}

func transform(input string) string {
	stack := make([]Pair[int32, int], 0, len(input))
	stack = append(stack, Pair[int32, int]{-1, 0})
	for _, c := range input {
		if stack[len(stack)-1].Key == c {
			stack[len(stack)-1].Value++
		} else {
			stack = append(stack, Pair[int32, int]{c, 1})
		}
	}
	return Stringify(stack[1:])
}

func Stringify[K, V any](pairs []Pair[K, V]) string {
	sb := strings.Builder{}
	for _, pair := range pairs {
		sb.WriteString(fmt.Sprintf("%v%c", pair.Value, pair.Key))
	}
	return sb.String()
}
