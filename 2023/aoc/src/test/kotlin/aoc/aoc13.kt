package aoc

import org.example.tools.getResource
import kotlin.test.Test
import kotlin.test.assertEquals

class aoc13 {

    fun parseInput(file: String) = getResource(file)
        .split("\n\n")
        .map { it.split("\n") }

    fun transpose(input: List<String>) = (0 ..< input[0].length)
        .map { ix -> input.joinToString("") { it[ix].toString() } }

    fun reflectedNumber(
        grid: List<String>,
    ) = grid.indices.filter { ix ->
        val distance = minOf(ix, grid.size - ix)
        (1..distance)
            .takeUnless { it.isEmpty() }
            ?.all { offset -> grid[ix + offset - 1] == grid[ix - offset] }
            ?: false
    }.takeIf { it.size == 1 }?.first() ?: 0


    infix fun String.diff(other: String): String {
        val setA = this.mapIndexed { ix, c -> ix to c }.toSet()
        val setB = other.mapIndexed { ix, c -> ix to c }.toSet()
        return (setA union setB subtract setA).joinToString("") { it.second.toString() }
    }

    fun reflectedNumberWithSmudge(
        grid: List<String>,
    ) = grid.indices.filter { ix ->
        val distance = minOf(ix, grid.size - ix)
        (1..distance)
            .takeUnless { it.isEmpty() }
            ?.sumOf { offset -> (grid[ix + offset - 1] diff grid[ix - offset]).length }
            ?.takeIf { it == 1 }
            ?.let { true }
            ?: false
    }.takeIf { it.size == 1 }?.first() ?: 0

    @Test
    fun part1() {
        val input = parseInput("/13/input.txt")

        val result = input.map { transpose(it) }.sumOf { reflectedNumber(it) } + input.sumOf { 100 * reflectedNumber(it) }

        println(result)

    }

    @Test
    fun part2() {
        val input = parseInput("/13/input.txt")

        val result = listOf(
            input.map { transpose(it) }.sumOf { reflectedNumberWithSmudge(it) },
            input.sumOf { 100 * reflectedNumberWithSmudge(it) }
        ).sum()

        println(result)


    }

    @Test
    fun diffTest() {
        assertEquals("..", "#...##..#" diff "#.......#")
        assertEquals("##", "#.......#" diff "#...##..#")
        assertEquals("#.", "....##..#" diff "#...##...")
    }
}