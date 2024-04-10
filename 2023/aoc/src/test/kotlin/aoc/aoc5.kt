package aoc

import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc5 {

    private fun String.toRange() = trim()
        .split(' ')
        .map { it.toLong() }
        .let { it[1] ..< (it[1] + it[2]) to it[0] ..< (it[0] + it[2]) }

    private fun parseInput(file: String) = getResourceAsStrings(file).let { rawInput ->
        val seeds = rawInput[0].trim().split(" ").drop(1).map { it.toLong() }
        val mapData = rawInput
            .drop(2)
            .filterNot { it.contains("map") }
            .joinToString("\n")
            .split("\n\n")
            .map { group -> group.split("\n").map { it.toRange() } }
        seeds to mapData
    }

    @Test
    fun part1() {
        val (seeds, almanac) = parseInput("/5/input.txt")

        val result = seeds.minOf { seed ->
            almanac.fold(seed) { acc, ranges ->
                ranges.firstOrNull { acc in it.first }?.let { (from, to) ->
                    to.first + (acc - from.first)
                } ?: acc
            }
        }
        println(result)
    }

    @Test
    fun part2() {
        val (seedsRaw, almanac) = parseInput("/5/input.txt")
        val seedRanges = seedsRaw.chunked(2).map { it[0] ..< (it[0] + it[1]) }
        val almanacReversed = almanac.reversed()
        val result =  generateSequence(0L) { it.inc() }.first { loc ->
            val seed = almanacReversed.fold(loc) { acc, ranges ->
                ranges.firstOrNull { acc in it.second }?.let { (from, to) ->
                    from.first + (acc - to.first)
                } ?: acc
            }
           seedRanges.any { seed in it }
        }

        println(result)
    }

}