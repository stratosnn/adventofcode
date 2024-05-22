package main

import "fmt"

func main() {
	row := 2978
	column := 3083

	diag := row + column - 1
	iter := diag * (diag - 1) / 2
	iter = iter + column

	fmt.Println(part1(iter))
}

func Rotate(num uint) uint {
	return num * 252533 % 33554393
}

func part1(iter int) uint {
	code := uint(20151125)
	for i := 0; i < iter-1; i++ {
		code = Rotate(code)
	}
	return code
}
