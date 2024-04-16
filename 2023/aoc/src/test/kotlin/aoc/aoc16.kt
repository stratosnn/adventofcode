package aoc

import org.example.tools.Point2D
import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc16 {
    private val S = Point2D(0  to +1) // inverted to be aligned with the grid
    private val N = Point2D(0  to -1)
    private val E = Point2D(+1 to 0)
    private val W = Point2D(-1 to 0)

    fun parseInput(file: String) = getResourceAsStrings(file).flatMapIndexed { y, line ->
        line.mapIndexed { x, c -> Point2D(x, y) to c }
    }.toMap()

    fun energizedSet(grid: Map<Point2D, Char>, start: Point2D, initialDirection: Point2D): Set<Point2D> {
        val dfs = mutableListOf(start to initialDirection)
        val visited = mutableSetOf<Pair<Point2D, Point2D>>()

        while (dfs.isNotEmpty()) {
            val (p, direction) = dfs.removeLast()
            if (p to direction in visited || p !in grid) continue

            visited.add(p to direction)
            when (grid[p] to direction) {
                '.' to S, '.' to N, '.' to E, '.' to W -> dfs.add((p + direction) to direction)
                '|' to S, '|' to N, '-' to E, '-' to W -> dfs.add((p + direction) to direction)
                '|' to E, '|' to W, '-' to N, '-' to S -> listOf(
                        direction.rotate(90),
                        direction.rotate(270)
                    ).forEach { dfs.add((p + it) to it) }
                '/' to W, '/' to E, '\\' to S, '\\' to N, -> {
                    val newDirection = direction.rotate(90)
                    dfs.add((p + newDirection) to newDirection)
                }
                '\\' to E, '\\' to W, '/' to N, '/' to S -> {
                    val newDirection = direction.rotate(270)
                    dfs.add((p + newDirection) to newDirection)
                }
                else -> {}
            }

        }
        return visited.map { it.first }.toSet()
    }

    @Test
    fun part1() {
        val input = parseInput("/16/input.txt")
        val energized = energizedSet(input, Point2D(0, 0), E)
        println(energized.size)

    }

    @Test
    fun part2() {
        val grid = parseInput("/16/input.txt")
        val maxX = grid.keys.maxOf { it.x }
        val maxY = grid.keys.maxOf { it.y }
        val candidates = buildList {
            addAll((0..maxY).map { Point2D(0, it) to E })
            addAll((0..maxY).map { Point2D(maxX, it) to W })
            addAll((0..maxX).map { Point2D(it, 0) to S })
            addAll((0..maxX).map { Point2D(it, maxY) to N })
        }

        val result = candidates.maxOf { (p, d) -> energizedSet(grid, p, d).size }
        println(result)
    }
}