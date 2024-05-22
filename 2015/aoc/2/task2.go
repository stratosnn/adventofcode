package main

import (
	"fmt"
	"github.com/m4gshm/gollections/slice/sum"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	if input, err := os.ReadFile("2/input.txt"); err == nil {
		var list []Box
		for _, line := range strings.Split(string(input), "\n") {
			list = append(list, Parse(line))
		}
		fmt.Println(part1(list))
		fmt.Println(part2(list))
	}
}

type Box struct {
	l, w, h int
}

func Parse(str string) Box {
	b := strings.Split(str, "x")
	l, _ := strconv.Atoi(b[0])
	w, _ := strconv.Atoi(b[1])
	h, _ := strconv.Atoi(b[2])
	return Box{l, w, h}
}

func (b Box) Area() int {
	return 2*b.l*b.w + 2*b.w*b.h + 2*b.h*b.l
}

func (b Box) MinSide() int {
	return min(b.l*b.w, b.w*b.h, b.h*b.l)
}

func (b Box) RibbonSide() int {
	list := []int{b.l, b.w, b.h}
	sort.Ints(list)
	return 2*list[0] + 2*list[1]
}

func part1(boxes []Box) int {
	var list []int
	for _, box := range boxes {
		list = append(list, box.Area()+box.MinSide())
	}
	return sum.Of(list)
}

func part2(boxes []Box) int {
	var list []int
	for _, box := range boxes {
		list = append(list, box.RibbonSide()+(box.w*box.h*box.l))
	}
	return sum.Of(list)
}
