package aoc

import org.example.tools.Point2D
import org.example.tools.Point2D.Companion.E
import org.example.tools.Point2D.Companion.N
import org.example.tools.Point2D.Companion.S
import org.example.tools.Point2D.Companion.W
import org.example.tools.getResourceAsStrings
import kotlin.test.Test

class aoc10 {

    private val allowedNodes = mapOf(
        W to listOf('-', 'L', 'F', 'S'),
        E to listOf('-', 'J', '7', 'S'),
        S to listOf('|', 'J', 'L', 'S'),
        N to listOf('|', '7', 'F', 'S'),
    )

    private val allowedDirectionMap = mapOf(
        'S' to listOf(S, N, E, W),
        '|' to listOf(S, N),
        '-' to listOf(E, W),
        'L' to listOf(N, E),
        'F' to listOf(S, E),
        'J' to listOf(N, W),
        '7' to listOf(S, W),
    )

    private fun parseInput(file: String) = getResourceAsStrings(file)
        .flatMapIndexed { iy, y -> y.mapIndexed { ix, x -> Point2D(ix, iy) to x } }.toMap()

    private fun followTheWhiteRabbit(grid: Map<Point2D, Char>, start: Point2D): List<Point2D> {
        val processed = mutableSetOf<Point2D>()
        val pipeWalk = mutableListOf(start)
        var nextOffset: Point2D?
        do {
            val cur = pipeWalk.last()
            processed.add(cur)
            nextOffset = allowedDirectionMap[grid[cur]!!]!!.firstOrNull { offset ->
                val allowed = grid.getOrDefault(cur + offset, '.') in allowedNodes[offset]!!
                val inProcessed = cur + offset in processed
                allowed && !inProcessed
            }
            nextOffset?.let { pipeWalk.addLast(it + cur) }
        } while (nextOffset != null)

        return pipeWalk
    }

    @Test
    fun part1() {
        val grid = parseInput("/10/input.txt")
        val start = grid.firstNotNullOf { (p, c) -> if (c == 'S') p else null }
        val pipeWalk = followTheWhiteRabbit(grid, start)

        println(pipeWalk.size / 2)
    }

    @Test
    fun part2() {
        val offsetToRight = mapOf(
            N to E,
            E to S,
            S to W,
            W to N,
        )
        val angleConnectors = setOf('L', 'J', 'F', '7')

        val grid = parseInput("/10/input.txt")
        val start = grid.firstNotNullOf { (p, c) -> if (c == 'S') p else null }
        val pipeWalk = followTheWhiteRabbit(grid, start)

        val marked = mutableSetOf<Point2D>()

        sequence {
            yieldAll(pipeWalk)
            yield(pipeWalk.first())
        }
            .windowed(3)
            .map { (a, b, c) -> Triple(b, b - a, c - b) }
            .forEach { (p, offset, nextOffset) ->

                val fillRegion = buildList {
                    add(p + offsetToRight[offset]!!)
                    if (grid[p]!! in angleConnectors) {
                        add(p + offsetToRight[nextOffset]!!)
                    }
                }.filter { it in grid && it !in marked && it !in pipeWalk }
                    .toMutableList()

                while (fillRegion.isNotEmpty()) {
                    fillRegion.removeFirst()
                        .also { marked.add(it) }
                        .neighbors(includeDiagonals = false)
                        .filter {
                            it in grid &&
                            it !in marked &&
                            it !in pipeWalk &&
                            it !in fillRegion
                        }.forEach { fillRegion.add(it) }
                }
            }

        println("Marked : ${marked.size}")
        println("PipeWalk : ${pipeWalk.size}")
        println("Grid Size : ${grid.size}")
        println("Missing : ${(grid.keys - marked - pipeWalk).size}")

//      Some visualisation
//
//        val maxX = grid.keys.maxOf { it.x }
//        val maxY = grid.keys.maxOf { it.y }
//
//        (0..maxY).forEach { y ->
//            (0..maxX).map { x ->
//                when (Point2D(x, y)) {
//                    in marked -> '+'
//                    in pipeWalk -> when(grid[Point2D(x, y)]) {
//                        'S' -> 'S'
//                        '|' -> '┃'
//                        '-' -> '━'
//                        'L' -> '┗'
//                        'F' -> '┏'
//                        'J' -> '┛'
//                        '7' -> '┓'
//                        else -> 'Z'
//                    }
//                    else -> '.' //grid[Point2D(x, y)]
//                }
//            }.joinToString("")
//                .also { println(it) }
//        }
    }
}
