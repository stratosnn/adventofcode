package aoc

import com.github.shiguruikai.combinatoricskt.combinations
import org.example.tools.Point2D
import org.example.tools.getResourceAsStrings
import kotlin.test.Test

class aoc11 {

    private fun parseInput(file: String) = getResourceAsStrings(file)
        .flatMapIndexed { iy, y -> y.mapIndexed { ix, x -> Point2D(ix, iy) to x } }.toMap()

    private fun expand(galaxies: List<Point2D>, multiplier: Int = 1): List<Point2D> {
        val minX = galaxies.minOf { it.x }
        val maxX = galaxies.maxOf { it.x }
        val minY = galaxies.minOf { it.y }
        val maxY = galaxies.maxOf { it.y }

        val gapsX = (minX..maxX).toSet() subtract galaxies.map { it.x }.toSet()
        val gapsY = (minY..maxY).toSet() subtract galaxies.map { it.y }.toSet()

        return galaxies.map { (x, y) ->
            Point2D(multiplier * gapsX.count { it < x } + x, multiplier * gapsY.count { it < y } + y)
        }
    }


    @Test
    fun part1 () {
        val input = parseInput("/11/input.txt")
        val galaxies = input.mapNotNull { (k, v) -> v.takeIf { it == '#' }?.let { k } }
        val expanded = expand(galaxies)

        val result = expanded.combinations(2).sumOf { (p1, p2) -> p1.manhattanDistance(p2) }

        println(result)
    }

    @Test
    fun part2 () {
        val input = parseInput("/11/input.txt")
        val galaxies = input.mapNotNull { (k, v) -> v.takeIf { it == '#' }?.let { k } }
        val expanded = expand(galaxies, 1_000_000 - 1)

        val result = expanded.combinations(2).sumOf { (p1, p2) -> p1.manhattanDistance(p2).toLong() }

        println(result)
    }
}