package main

import (
	"aoc/common"
	"fmt"
	"github.com/kelindar/bitmap"
	"github.com/m4gshm/gollections/slice/sum"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Action string

const (
	TurnOn  Action = "turn on"
	TurnOff Action = "turn off"
	Toggle  Action = "toggle"
)

type CommandLine struct {
	TopLeft, BottomRight common.Point2D[int]
	action               Action
}

var re = regexp.MustCompile(`.* (\d+),(\d+) through (\d+),(\d+)$`)

func ParseCommandLine(line string) CommandLine {
	var action Action
	switch {
	case strings.HasPrefix(line, string(TurnOn)):
		action = TurnOn
	case strings.HasPrefix(line, string(TurnOff)):
		action = TurnOff
	case strings.HasPrefix(line, string(Toggle)):
		action = Toggle
	default:
		panic("invalid action")
	}

	matches := re.FindStringSubmatch(line)
	l, _ := strconv.Atoi(matches[1])
	t, _ := strconv.Atoi(matches[2])
	r, _ := strconv.Atoi(matches[3])
	b, _ := strconv.Atoi(matches[4])
	topLeft := common.Point2D[int]{l, t}
	botRight := common.Point2D[int]{r, b}

	return CommandLine{topLeft, botRight, action}
}

func main() {
	if input, err := os.ReadFile("6/input.txt"); err == nil {
		list := strings.Split(string(input), "\n")
		commands := make([]CommandLine, 0, len(list))
		for _, line := range list {
			commands = append(commands, ParseCommandLine(line))
		}
		fmt.Println(part1(commands))
		fmt.Println(part1b(commands))
		fmt.Println(part2(commands))
	}
}

func part1(commands []CommandLine) int {
	grid := bitmap.Bitmap{}
	grid.Grow(1000 * 1000)

	for _, cmd := range commands {
		for x := cmd.TopLeft.X; x <= cmd.BottomRight.X; x++ {
			for y := cmd.TopLeft.Y; y <= cmd.BottomRight.Y; y++ {
				loc := uint32(y*1000 + x)
				switch cmd.action {
				case TurnOn:
					grid.Set(loc)
				case TurnOff:
					grid.Remove(loc)
				case Toggle:
					if grid.Contains(loc) {
						grid.Remove(loc)
					} else {
						grid.Set(loc)
					}
				}
			}
		}
	}

	return grid.Count()
}

func part1b(commands []CommandLine) int {
	grid := make([]int, 1000*1000)
	for _, cmd := range commands {
		for x := cmd.TopLeft.X; x <= cmd.BottomRight.X; x++ {
			for y := cmd.TopLeft.Y; y <= cmd.BottomRight.Y; y++ {
				loc := uint32(y*1000 + x)
				switch cmd.action {
				case TurnOn:
					grid[loc] = 1
				case TurnOff:
					grid[loc] = 0
				case Toggle:
					grid[loc] = 1 - grid[loc]
				}
			}
		}
	}
	return sum.Of(grid)
}

func part2(commands []CommandLine) int {
	grid := make([]int, 1000*1000)
	for _, cmd := range commands {
		for x := cmd.TopLeft.X; x <= cmd.BottomRight.X; x++ {
			for y := cmd.TopLeft.Y; y <= cmd.BottomRight.Y; y++ {
				loc := uint32(y*1000 + x)
				switch cmd.action {
				case TurnOn:
					grid[loc]++
				case TurnOff:
					grid[loc] = max(grid[loc]-1, 0)
				case Toggle:
					grid[loc] += 2
				}
			}
		}
	}
	return sum.Of(grid)
}
