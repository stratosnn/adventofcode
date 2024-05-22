package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	if input, err := os.ReadFile("8/input.txt"); err == nil {
		list := strings.Split(string(input), "\n")
		fmt.Println(part1(list))
		fmt.Println(part2(list))
	}
}

func part1(lines []string) int {
	size := 0
	for _, line := range lines {
		decoded := process(line)
		size += len(line) - len(decoded)
	}
	return size
}

func part2(lines []string) int {
	size := 0
	for _, line := range lines {
		encoded, _ := json.Marshal(line)
		size += len(encoded) - len(line)
	}
	return size
}

func process(line string) string {
	if len(line) == 0 {
		return ""
	}
	c := line[0]
	switch c {
	case '\\':
		c2 := line[1]
		switch c2 {
		case '\\':
			return `\` + process(line[2:])
		case '"':
			return `"` + process(line[2:])
		case 'x':
			parsed, err := strconv.ParseInt(line[2:4], 16, 16)
			if err != nil {
				panic(err)
			}
			return string(parsed%128) + process(line[4:])
		}
	case '"':
		return process(line[1:])

	default:
		return string(c) + process(line[1:])
	}
	return ""
}
