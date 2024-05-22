package main

import (
	"fmt"
	"math"
)

type Player struct {
	hp, damage, armor int
}

type Item struct {
	name                string
	cost, damage, armor int
}

var weapons = []Item{
	{"Dagger", 8, 4, 0},
	{"Shortsword", 10, 5, 0},
	{"Warhammer", 25, 6, 0},
	{"Longsword", 40, 7, 0},
	{"Greataxe", 74, 8, 0},
}
var armor = []Item{
	{"None", 0, 0, 0},
	{"Leather", 13, 0, 1},
	{"Chainmail", 31, 0, 2},
	{"Splintmail", 53, 0, 3},
	{"Bandedmail", 75, 0, 4},
	{"Platemail", 102, 0, 5},
}
var hand1 = []Item{
	{"None", 0, 0, 0},
	{"Defense +1", 20, 0, 1},
	{"Damage +1", 25, 1, 0},
	{"Defense +2", 40, 0, 2},
	{"Damage +2", 50, 2, 0},
	{"Defense +3", 80, 0, 3},
	{"Damage +3", 100, 3, 0},
}
var hand2 = []Item{
	{"None", 0, 0, 0},
	{"Defense +1", 20, 0, 1},
	{"Damage +1", 25, 1, 0},
	{"Defense +2", 40, 0, 2},
	{"Damage +2", 50, 2, 0},
	{"Defense +3", 80, 0, 3},
	{"Damage +3", 100, 3, 0},
}

var boss = Player{109, 8, 2}
var player = Player{hp: 100}

func main() {
	fmt.Println(part1())
	fmt.Println(part2())
}

func battle(player, boss Player) (win bool) {
	bd := max(1, player.damage-boss.armor)
	pd := max(1, boss.damage-player.armor)
	roundsForBoss := (boss.hp + bd - 1) / bd
	roundsForPlayer := (player.hp + pd - 1) / pd
	return roundsForPlayer >= roundsForBoss
}

func part1() int {
	minCost := math.MaxInt32
	for _, w := range weapons {
		for _, a := range armor {
			for _, r1 := range hand1 {
				for _, r2 := range hand2 {
					if r1 != hand1[0] && r1 == r2 {
						continue
					}
					cost := w.cost + a.cost + r1.cost + r2.cost
					if battle(player.Enhance(w, a, r1, r2), boss) {
						minCost = min(cost, minCost)
					}
				}
			}
		}
	}
	return minCost
}

func part2() int {
	maxCost := math.MinInt32
	for _, w := range weapons {
		for _, a := range armor {
			for _, r1 := range hand1 {
				for _, r2 := range hand2 {
					if r1 != hand1[0] && r1 == r2 {
						continue
					}
					cost := w.cost + a.cost + r1.cost + r2.cost
					if !battle(player.Enhance(w, a, r1, r2), boss) {
						maxCost = max(cost, maxCost)
					}
				}
			}
		}
	}
	return maxCost
}

func (p Player) Enhance(item ...Item) Player {
	for _, i := range item {
		p.armor += i.armor
		p.damage += i.damage
	}
	return p
}
