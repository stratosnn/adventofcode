package aoc

import org.example.tools.Point2D
import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc18 {

    data class DigVector(
        val direction: Point2D,
        val length: Long,
        val color: Long,
    )

    fun parseInput(file: String) = getResourceAsStrings(file)
        .map { line ->
            val (d, l, c) = line.split(' ', '(', '#', ')').filter { it.isNotBlank() }
            DigVector(Point2D.fromDirectionString(d), l.toLong(), c.toLong(16))
        }

    fun parseInput2(file: String) = getResourceAsStrings(file)
        .map { line ->
            val code = line.substringAfter('#').substringBefore(')')
            DigVector(
                when(code.last()) {
                    '0' -> Point2D.E
                    '1' -> Point2D.S
                    '2' -> Point2D.W
                    '3' -> Point2D.N
                    else -> throw IllegalArgumentException("Illegal arg $code")
                },
                code.take(code.length - 1).toLong(16),
                0
            )
        }


    @Test
    fun part1() {
        val input = parseInput("/18/input.txt")

        val area = input.runningFold(Point2D(0, 0)) { acc, v -> acc + (v.direction * v.length.toInt()) }
            .windowed(2)
            .sumOf { (a, b) -> a.determinant(b) } / 2

        println(area + input.sumOf { it.length } / 2 + 1)
    }

    @Test
    fun part2() {
        val input = parseInput2("/18/input.txt")

        val area = input.runningFold(Point2D(0, 0)) { acc, v -> acc + (v.direction * v.length.toInt()) }
            .windowed(2)
            .sumOf { (a, b) -> a.determinant(b) } / 2L

        println(area + input.sumOf { it.length } / 2L + 1L)
    }
}