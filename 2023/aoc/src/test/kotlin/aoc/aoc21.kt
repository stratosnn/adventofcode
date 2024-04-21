package aoc

import org.example.tools.Point2D
import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc21 {

    fun parseInput(file: String) = getResourceAsStrings(file).flatMapIndexed { y, line ->
        line.mapIndexed { x, c -> Point2D(x, y) to c }
    }.toMap()

    fun expandGrid(grid: Map<Point2D, Char>) = run {
        val lenX = grid.keys.maxOf { it.x } - grid.keys.minOf { it.x } + 1
        val lenY = grid.keys.maxOf { it.y } - grid.keys.minOf { it.y } + 1
        Point2D(0,0).neighbors(includeDiagonals = true).flatMap { offset ->
            grid.map { (k, v) -> Point2D(lenX, lenY) * offset + k to v }
        }
    }.toMap() + grid

    fun bfs(grid: Map<Point2D, Char>, start: Point2D, count: Int) = run {
        val permitted = setOf('S', '.')
        var bfs = setOf(start)
        repeat(count) {
            bfs = bfs.flatMap { p -> p.neighbors().filter { grid[it] in permitted } }.toSet()
        }
        bfs.size
    }


    @Test
    fun part1() {
        val grid = parseInput("/21/input.txt")
        val permitted = setOf('S', '.')
        var bfs = setOf(grid.firstNotNullOf { (p, c) -> if (c == 'S') p else null })
        repeat(64) {
            bfs = bfs.flatMap { p -> p.neighbors().filter { grid[it] in permitted } }.toSet()
        }
        println(bfs.size)
    }

    @Test
    fun part2() {
        val grid = parseInput("/21/input.txt")
        println("original size ${grid.size}")
        val start = grid.firstNotNullOf { (p, c) -> if (c == 'S') p else null }

        val expanded = expandGrid(expandGrid(grid))
        println("expanded size ${expanded.size}")

        val p = (0..2).map { Point2D(it, bfs(expanded, start, 65 + it * 131)) }

        val c = p.first().y
        val (x1, y1) = p[1]
        val (x2, y2) = p[2]
        val (c1, c2) = y1 - c to y2 - c

        val det = Point2D(x1*x1, x2*x2).determinant(Point2D(x1, x2))
        val a = Point2D(c1, c2).determinant(Point2D(x1, x2)) / det
        val b = Point2D(x1*x1, x2*x2).determinant(Point2D(c1, c2)) / det

        println("a $a b $b c $c")

        val reps = (26501365L - 65L) / 131L
        println(a * reps * reps + b * reps + c)
    }
}