package aoc

import org.example.tools.Point2D
import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test
import java.util.PriorityQueue

class aoc17 {

    fun parseInput(file: String) = getResourceAsStrings(file).flatMapIndexed { y, line ->
        line.mapIndexed { x, d -> Point2D(x, y) to d.digitToInt() }
    }.toMap()


    private val allowedMovements = mapOf(
        Point2D.N to listOf(Point2D.E, Point2D.N, Point2D.W),
        Point2D.S to listOf(Point2D.E, Point2D.S, Point2D.W),
        Point2D.E to listOf(Point2D.S, Point2D.E, Point2D.N),
        Point2D.W to listOf(Point2D.S, Point2D.W, Point2D.N),
    )

    data class Nav(
        val position: Point2D,
        val direction: Point2D,
        val steps: Int
    )

    data class HeatState(
        val nav: Nav,
        val heat: Int,
    ) : Comparable<HeatState> {
        override fun compareTo(other: HeatState) = heat - other.heat
    }

    fun findPath(grid: Map<Point2D, Int>, minSteps: Int = 1,  valid: (nav: Nav, next: Nav) -> Boolean): Int {
        val maxX = grid.keys.maxOf { it.x }
        val maxY = grid.keys.maxOf { it.y }

        val visited = mutableSetOf<Nav>()
        val heap = PriorityQueue<HeatState>()
        listOf(Point2D.E, Point2D.S)
            .map { HeatState(Nav(Point2D(0, 0), it, 0), 0) }
            .forEach {
                heap.add(it)
            }

        while (heap.isNotEmpty()) {
            val (nav, heat) = heap.poll()
            if (nav.position == Point2D(maxX, maxY) && nav.steps >= minSteps) {
                return heat
            }
            if (nav in visited) continue

            visited.add(nav)

            allowedMovements[nav.direction]!!
                .mapNotNull { dir ->
                    val steps = if (dir == nav.direction) nav.steps + 1 else 1
                    Nav(nav.position + dir, dir, steps).takeIf { next ->
                        next.position in grid && valid(nav, next) && next !in visited
                    }
                }.forEach {
                    heap.add(HeatState(it, heat + grid[it.position]!!))
                }
        }
        return -1
    }

    @Test
    fun part1() {
        val grid = parseInput("/17/input.txt")

        println(findPath(grid) { _, next -> next.steps <= 3 })
    }


    @Test
    fun part2() {
        val grid = parseInput("/17/input.txt")

        println(findPath(grid, 4) { cur, next ->
            if (cur.steps < 4) cur.direction == next.direction
            else if (cur.steps > 9) cur.direction != next.direction
            else true
        })
    }
}