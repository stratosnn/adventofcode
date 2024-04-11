package aoc

import org.example.tools.getResourceAsStrings
import kotlin.test.Test


class aoc9 {

    private fun parseInput(file: String) = getResourceAsStrings(file)
        .map { it.trim().split(' ').map { it.toInt() } }

    private fun reduce(seq: Collection<Int>): Int =
    if (!seq.all { it == 0 }) {
        seq.last() + reduce( seq.windowed(2).map { it[1] - it[0] })
    } else {
        0
    }

    @Test
    fun part1() {
        val sequences = parseInput("/9/input.txt")
        sequences.sumOf { reduce(it) }.also { println(it) }
    }

    @Test
    fun part2() {
        val sequences = parseInput("/9/input.txt")
        sequences.sumOf { reduce(it.reversed()) }.also { println(it) }
    }
}