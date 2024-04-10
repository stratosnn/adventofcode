package aoc

import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test
import kotlin.math.ceil
import kotlin.math.sqrt

class aoc6 {

    private fun parseInput(file: String) = getResourceAsStrings(file)
        .map { line ->
            line.split(':')[1].split(' ').filterNot { it.isEmpty() }.map { it.toInt() }
        }.let { (time, distance) -> time zip distance}


    @Test
    fun part1() {
        val races = parseInput("/6/input.txt")
        val result = races.map { (time, distance) ->
            (0 .. time).map { it * (time - it) }.filter { it > distance }
        }.map { it.count() }.reduce { a, b -> a * b }
        println(result)
    }

    @Test
    fun part1QuadraticEquation() {
        val races = parseInput("/6/input.txt")
        val result = races.map { (time, distance) ->
            val d = sqrt(time * time - 4.0 * distance)
            IntRange(
                ((time - d) / 2 + 1).toInt(),
                ceil((time + d) / 2 - 1).toInt()
            ).count()
        }.reduce { a, b -> a * b }
        println(result)
    }

    @Test
    fun part2() {
        val (time, distance) = getResourceAsStrings("/6/input.txt")
            .map { line ->
                line.substringAfter(':').filterNot { it.isWhitespace() }.toLong()
            }

        val d = sqrt(time * time - 4.0 * distance)
        val result = LongRange(
            ((time - d) / 2 + 1).toLong(),
            ceil((time + d) / 2 - 1).toLong()
        ).count()
        println(result)
    }


}