package aoc

import org.example.tools.Point2D
import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc14 {

    private val S = Point2D(0  to +1) // inverted to be aligned with the grid
    private val N = Point2D(0  to -1)
    private val E = Point2D(+1 to 0)
    private val W = Point2D(-1 to 0)

    data class Grid(val grid: MutableMap<Point2D, Char>) {
        val maxX: Int by lazy { grid.keys.maxOf { it.x } }
        val maxY: Int by lazy { grid.keys.maxOf { it.y } }
    }

    private fun parseAsMap(file: String) = getResourceAsStrings(file)
        .flatMapIndexed { y, line -> line.mapIndexed { x, c -> Point2D(x to y) to c } }
        .toMap()


    private fun shiftAll(grid: Grid, direction: Point2D): Set<Point2D> {
        val input = grid.grid

        val seq = when (direction) {
            N -> (0..grid.maxY).flatMap { y -> (0..grid.maxX).map { x -> Point2D(x to y) } }
            S -> (grid.maxY downTo 0).flatMap { y -> (0..grid.maxX).map { x -> Point2D(x to y) } }
            E -> (grid.maxX downTo 0).flatMap { x -> (0..grid.maxY).map { y -> Point2D(x to y) } }
            W -> (0..grid.maxX).flatMap { x -> (0..grid.maxY).map { y -> Point2D(x to y) } }
            else -> throw IllegalArgumentException("Unknown direction $direction")
        }.filter { input[it] == 'O' }

        return seq.map { p ->
            var cur = p
            input[cur] = '.'
            while (input[cur + direction] == '.') {
                cur += direction
            }
            input[cur] = 'O'
            cur
        }.toSet()

    }


    @Test
    fun part1() {
        val grid = Grid(parseAsMap("/14/input.txt").toMutableMap())

        val result = shiftAll(grid, N).sumOf { p -> grid.maxY - p.y + 1 }

        println(result)
    }

    @Test
    fun part2() {
        val grid = Grid(parseAsMap("/14/input.txt").toMutableMap())
        val cycle = listOf(N, W, S, E)
        val previousPositions = mutableListOf<Set<Point2D>>()

        for (c in 0..<1_000_000_000) {
            val position = cycle.map { direction -> shiftAll(grid, direction) }.last()
            previousPositions.add(position)

            if (previousPositions.indexOf(position) != previousPositions.lastIndex) {
                break
            }
        }

        val cycleStart = previousPositions.indexOf(previousPositions.last())
        val cycleLength = previousPositions.size - 1 - cycleStart
        val ix = cycleStart + (1_000_000_000 - (cycleStart + 1)) % cycleLength

        val result = previousPositions[ix].sumOf { p -> grid.maxY - p.y + 1 }

        println(result)
    }
}