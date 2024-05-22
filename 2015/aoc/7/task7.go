package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type GateType string

const (
	And    GateType = "AND"
	Or     GateType = "OR"
	LShift GateType = "LSHIFT"
	RShift GateType = "RSHIFT"
	Not    GateType = "NOT"
	NoOp   GateType = "NOOP"
)

var gateMap = map[string]GateType{
	"AND":    And,
	"OR":     Or,
	"LSHIFT": LShift,
	"RSHIFT": RShift,
	"NOT":    Not,
	"NOOP":   NoOp,
}

type Gate struct {
	output string
	inputs []string
	t      GateType
}

func main() {
	if input, err := os.ReadFile("7/input.txt"); err == nil {
		list := strings.Split(string(input), "\n")
		gates := make(map[string]Gate, len(list))
		for _, line := range list {
			gate := Parse(line)
			gates[gate.output] = gate
		}

		fmt.Println(part1(gates))
		fmt.Println(part2(gates))
	}
}

var re = regexp.MustCompile(`(.*) -> (\w+)`)

func Parse(line string) Gate {
	match := re.FindStringSubmatch(line)
	output := match[2]
	groups := strings.Split(match[1], " ")
	var t GateType
	var inputs []string
	switch {
	case len(groups) == 1:
		t = NoOp
		inputs = append(inputs, groups[0])
	case len(groups) == 2:
		t = Not
		inputs = append(inputs, groups[1])
	default:
		t = gateMap[groups[1]]
		inputs = append(inputs, groups[0], groups[2])
	}

	return Gate{output, inputs, t}
}

func gateDfs(gates map[string]Gate, entry string, cache map[string]uint16) (ret uint16) {
	if signal, ok := cache[entry]; ok {
		return signal
	}
	defer func() { cache[entry] = ret }()
	if val, ok := strconv.Atoi(entry); ok == nil {
		return uint16(val)
	}
	gate := gates[entry]

	switch gate.t {
	case And:
		return gateDfs(gates, gate.inputs[0], cache) & gateDfs(gates, gate.inputs[1], cache)
	case Or:
		return gateDfs(gates, gate.inputs[0], cache) | gateDfs(gates, gate.inputs[1], cache)
	case LShift:
		return gateDfs(gates, gate.inputs[0], cache) << gateDfs(gates, gate.inputs[1], cache)
	case RShift:
		return gateDfs(gates, gate.inputs[0], cache) >> gateDfs(gates, gate.inputs[1], cache)
	case Not:
		return ^gateDfs(gates, gate.inputs[0], cache)
	case NoOp:
		return gateDfs(gates, gate.inputs[0], cache)
	default:
		panic("invalid gate type")
	}
}

func part1(gates map[string]Gate) uint16 {
	cache := make(map[string]uint16, len(gates))
	return gateDfs(gates, "a", cache)
}

func part2(gates map[string]Gate) uint16 {
	signal := part1(gates)
	gates["b"] = Gate{"b", []string{strconv.Itoa(int(signal))}, NoOp}
	return part1(gates)
}
