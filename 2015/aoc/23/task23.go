package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Instruction interface {
	Apply(s *State)
}

type Hlf struct {
	reg byte
}

type Tpl struct {
	reg byte
}

type Inc struct {
	reg byte
}

type Jmp struct {
	offset int
}

type Jie struct {
	reg    byte
	offset int
}

type Jio struct {
	reg    byte
	offset int
}

func (i *Hlf) Apply(s *State) {
	var r *uint64
	switch i.reg {
	case 'a':
		r = &s.a
	case 'b':
		r = &s.b
	}
	*r /= 2
	s.execIx++
}

func (i *Tpl) Apply(s *State) {
	var r *uint64
	switch i.reg {
	case 'a':
		r = &s.a
	case 'b':
		r = &s.b
	}
	*r *= 3
	s.execIx++
}

func (i *Inc) Apply(s *State) {
	var r *uint64
	switch i.reg {
	case 'a':
		r = &s.a
	case 'b':
		r = &s.b
	}
	*r++
	s.execIx++
}

func (i *Jmp) Apply(s *State) {
	s.execIx += i.offset
}

func (i *Jie) Apply(s *State) {
	var r *uint64
	switch i.reg {
	case 'a':
		r = &s.a
	case 'b':
		r = &s.b
	}
	if *r%2 == 0 {
		s.execIx += i.offset
	} else {
		s.execIx++
	}
}

func (i *Jio) Apply(s *State) {
	var r *uint64
	switch i.reg {
	case 'a':
		r = &s.a
	case 'b':
		r = &s.b
	}
	if *r == 1 {
		s.execIx += i.offset
	} else {
		s.execIx++
	}
}

type State struct {
	instructions []Instruction
	a, b         uint64
	execIx       int
}

func main() {
	if input, err := os.ReadFile("23/input.txt"); err == nil {
		s := State{instructions: Parse(string(input))}

		fmt.Println(part1(s))
		fmt.Println(part2(s))
	}

}

func part1(s State) uint64 {
	for s.execIx < len(s.instructions) {
		s.instructions[s.execIx].Apply(&s)
	}
	return s.b
}

func part2(s State) uint64 {
	s.a = 1
	for s.execIx < len(s.instructions) {
		s.instructions[s.execIx].Apply(&s)
	}
	return s.b
}

func Parse(s string) []Instruction {
	instructions := make([]Instruction, 0, 32)
	for _, line := range strings.Split(s, "\n") {
		instructions = append(instructions, ParseInstructionLine(line))
	}
	return instructions
}

func ParseInstructionLine(line string) Instruction {
	ri := strings.Split(line, " ")
	switch ri[0] {
	case "hlf":
		return &Hlf{reg: ri[1][0]}
	case "tpl":
		return &Tpl{reg: ri[1][0]}
	case "inc":
		return &Inc{reg: ri[1][0]}
	case "jmp":
		offset, _ := strconv.Atoi(ri[1])
		return &Jmp{offset: offset}
	case "jie":
		offset, _ := strconv.Atoi(ri[2])
		return &Jie{reg: ri[1][0], offset: offset}
	case "jio":
		offset, _ := strconv.Atoi(ri[2])
		return &Jio{reg: ri[1][0], offset: offset}
	default:
		panic(fmt.Sprintf("Unknown instruction: %s", ri[0]))
	}
}
