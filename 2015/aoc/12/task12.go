package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
)

func main() {
	if input, err := os.ReadFile("12/input.txt"); err == nil {
		fmt.Println(part1(string(input)))
		fmt.Println(part2(string(input)))
	}
}

func part1(input string) int {
	sum := 0
	buf := make([]byte, 0, 256)
	for _, c := range input {
		if c == '-' || (c >= '0' && c <= '9') {
			buf = append(buf, byte(c))
		} else if len(buf) > 0 {
			if val, err := strconv.Atoi(string(buf)); err == nil {
				sum += val
				buf = buf[:0]
			} else {
				panic("invalid buf")
			}
		} else {
			buf = buf[:0]
		}

	}
	return sum
}

func part2(input string) int {
	var data interface{}
	if err := json.Unmarshal([]byte(input), &data); err != nil {
		panic(err)
	}
	return WalkJSON(data)
}

func WalkJSON(v interface{}) int {
	switch vv := v.(type) {
	case string:
		return 0
	case float64:
		return int(v.(float64))
	case []interface{}:
		sum := 0
		for _, u := range vv {
			sum += WalkJSON(u)
		}
		return sum
	case map[string]interface{}:
		sum := 0
		for _, u := range vv {
			sum += WalkJSON(u)
			switch u.(type) {
			case string:
				if u.(string) == "red" {
					return 0
				}
			}
		}
		return sum
	default:
		fmt.Println("Unknown type", vv)
		return 0
	}
}
