package main

import (
	"fmt"
	"testing"
)

func TestPerf(t *testing.T) {
	var player = Player{hp: 50, mana: 500}
	var boss = Player{hp: 28, damage: 9}
	fmt.Println(part1b(player, boss))

}
