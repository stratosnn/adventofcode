package main

import (
	"fmt"
	"math"
	"slices"
)

type Player struct {
	hp, damage, armor, mana int
}

type Shield struct {
	duration int
}
type Poison struct {
	duration int
}
type Recharge struct {
	duration int
}

func main() {
	// This whole thing is entirely terrible implementation
	// storing effects as an array of interfaces is highly cumbersome
	var player = Player{hp: 50, mana: 500}
	var boss = Player{hp: 51, damage: 9}

	//var player = Player{hp: 10, mana: 250}
	//var boss = Player{hp: 14, damage: 8}
	// R-S-D-P-M

	fmt.Println(part1b(player, boss))
	fmt.Println(part2b(player, boss))
	// 1073 too low
	// 920 too low
}

func part1b(player, boss Player) int {
	state := State{playerTurn: true}
	return round2(player, boss, state, "")
}

func part2b(player, boss Player) int {
	state := State{playerTurn: true, hard: true}
	return round2(player, boss, state, "")
}

type State struct {
	s          Shield
	p          Poison
	r          Recharge
	playerTurn bool
	hard       bool
}

func round2(player, boss Player, state State, chain string) int {
	if state.hard && state.playerTurn {
		player.hp--
	}
	if player.hp <= 0 {
		return math.MaxInt16 << 8
	}
	if state.s.duration > 0 {
		state.s.duration--
	}
	if state.r.duration > 0 {
		state.r.duration--
		player.mana += 101
	}
	if state.p.duration > 0 {
		state.p.duration--
		boss.hp -= 3
	}
	if boss.hp <= 0 {
		return 0
	}
	if state.playerTurn {
		if player.mana < 53 {
			return math.MaxInt16 << 8
		}
		alternatives := make([]int, 0, 6)
		if player.mana >= 229 && state.r.duration <= 0 {
			p := player
			p.mana -= 229
			b := boss
			s := state
			s.r.duration = 5
			s.playerTurn = !state.playerTurn
			alternatives = append(alternatives, 229+round2(p, b, s, chain))
			//alternatives = append(alternatives, 229+round2(p, b, s, chain+"R"))
		}
		if player.mana >= 173 && state.p.duration <= 0 {
			p := player
			p.mana -= 173
			b := boss
			s := state
			s.p.duration = 6
			s.playerTurn = !state.playerTurn
			alternatives = append(alternatives, 173+round2(p, b, s, chain))
			//alternatives = append(alternatives, 173+round2(p, b, s, chain+"P"))
		}
		if player.mana >= 113 && state.s.duration <= 0 {
			p := player
			p.mana -= 113
			b := boss
			s := state
			s.s.duration = 6
			s.playerTurn = !state.playerTurn
			alternatives = append(alternatives, 113+round2(p, b, s, chain))
			//alternatives = append(alternatives, 113+round2(p, b, s, chain+"S"))
		}
		if player.mana >= 73 {
			p := player
			p.mana -= 73
			b := boss
			s := state
			p.hp += 2
			b.hp -= 2
			s.playerTurn = !state.playerTurn
			alternatives = append(alternatives, 73+round2(p, b, s, chain))
			//alternatives = append(alternatives, 73+round2(p, b, s, chain+"D"))
		}
		if player.mana >= 53 {
			p := player
			p.mana -= 53
			b := boss
			s := state
			b.hp -= 4
			s.playerTurn = !state.playerTurn
			alternatives = append(alternatives, 53+round2(p, b, s, chain))
			//alternatives = append(alternatives, 53+round2(p, b, s, chain+"M"))
		}
		res := slices.Min(alternatives)
		return res
	} else {
		bonusArmor := 0
		if state.s.duration > 0 {
			bonusArmor = 7
		}
		p := player
		s := state
		s.playerTurn = !s.playerTurn

		p.hp -= max(1, boss.damage-(player.armor+bonusArmor))
		return round2(p, boss, s, chain)
		//return round2(p, boss, s, chain+"-")
	}
}
