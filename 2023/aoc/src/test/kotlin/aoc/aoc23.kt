package aoc

import org.example.tools.Point2D
import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc23 {

    private val allowedForDirection = mapOf(
        Point2D.N to setOf('.', '^'),
        Point2D.E to setOf('.', '>'),
        Point2D.S to setOf('.', 'v'),
        Point2D.W to setOf('.', '<'),
    )

    private val walkable = setOf('.', '<', '^', '>', 'v')


    fun parseInput(file: String) = getResourceAsStrings(file).flatMapIndexed { y, line ->
        line.mapIndexed { x, c -> Point2D(x, y) to c }
    }.toMap()


    private fun Map<Point2D, Char>.simpleDfs(
        start: Point2D,
        finish: Point2D,
        visited: Set<Point2D> = emptySet()
    ): Long {
        val lifo = ArrayDeque<Point2D>().apply { add(start) }
        val currentlyVisited = visited.toMutableSet()
        while (lifo.isNotEmpty()) {
            val current = lifo.removeLast()
            currentlyVisited.add(current)
            if (current == finish) {
                return currentlyVisited.size.toLong()
            }

            val neighbours = current.neighbors().filter {
                getOrDefault(it, '#') in allowedForDirection[it - current]!! && it !in currentlyVisited
            }

            when(neighbours.size) {
                0 -> return 0L
                1 -> lifo.add(neighbours.first())
                else -> return neighbours.maxOf { simpleDfs(it, finish, currentlyVisited.toSet()) }
            }
        }
        return Long.MIN_VALUE
    }

    private fun Map<Point2D, Char>.traceUntilStop(
        start: Point2D,
        stopPoints: Set<Point2D>,
        visited: Set<Point2D> = emptySet()
    ): Map<Point2D, Int> {
        val lifo = ArrayDeque<Point2D>().apply { add(start) }
        val currentlyVisited = visited.toMutableSet()
        while (lifo.isNotEmpty()) {
            val current = lifo.removeLast()
            currentlyVisited.add(current)
            if (current in stopPoints) {
                return mapOf(current to currentlyVisited.size - 1)
            }

            val neighbours = current.neighbors().filter {
                getOrDefault(it, '#') in walkable && it !in currentlyVisited
            }

            when(neighbours.size) {
                0 -> return emptyMap()
                1 -> lifo.add(neighbours.first())
                else -> return neighbours
                        .flatMap { traceUntilStop(it, stopPoints, currentlyVisited.toSet()).entries }
                        .sortedBy { it.value }.associate { (k, v) -> k to v }
            }
        }
        return emptyMap()
    }

    private fun Map<Point2D, Char>.reduceGraph(decisionPoints: Set<Point2D>) =
        decisionPoints.associateWith { start -> traceUntilStop(start, decisionPoints - start) }

    private fun Map<Point2D, Map<Point2D, Int>>.dfs(start: Point2D, finish: Point2D, visited: Set<Point2D> = emptySet()): Int {
        if (start in visited) return 0
        if (start == finish) return 0
        val currentlyVisited = visited + start
        return this[start]!!
            .filterKeys { it !in currentlyVisited }
            .takeIf { it.isNotEmpty() }
            ?.entries
            ?.maxOf { (n, d) -> dfs(n, finish, currentlyVisited) + d }
            ?: Int.MIN_VALUE
    }


    @Test
    fun part1() {
        val grid = parseInput("/23/input.txt")

        val start = grid.entries.first { (p, c) -> p.y == 0L && c == '.' }.key
        val maxY = grid.keys.maxOf { it.y }
        val finish = grid.entries.first { (p, c) -> p.y == maxY && c == '.' }.key

        println(grid.simpleDfs(start, finish) - 1)

    }

    @Test
    fun part2() {
        val grid = parseInput("/23/input.txt")

        val start = grid.entries.first { (p, c) -> p.y == 0L && c == '.' }.key
        val maxY = grid.keys.maxOf { it.y }
        val finish = grid.entries.first { (p, c) -> p.y == maxY && c == '.' }.key

        val decisionPoints = grid.filterValues { it != '#' }
            .filterKeys { p -> p.neighbors().filter { grid[it] in walkable }.size > 2 }.keys + start + finish

        val reduced = grid.reduceGraph(decisionPoints)

        reduced.dfs(start, finish).also { println(it) }

    }
}