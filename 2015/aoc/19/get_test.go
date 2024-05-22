package main

import (
	"fmt"
	"os"
	"testing"
)

func TestPerf(t *testing.T) {
	if input, err := os.ReadFile("input.txt"); err == nil {
		replacements, molecule := Parse(string(input))
		fmt.Println(part2(replacements, molecule))
	}
}
