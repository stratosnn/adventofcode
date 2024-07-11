import org.junit.jupiter.api.Test
import tools.Point2D

const val favNumber = 1358L

class aoc13 {

    fun formula(p: Point2D, favNumber: Long) = let {
        val value = p.x*p.x + 3*p.x + 2*p.x*p.y + p.y + p.y*p.y + favNumber
        (0..< 62).sumOf { (value shr it) and 1 } % 2 == 1L
    }

    @Test
    fun part1() {
        val target = Point2D(31,39)
        val start = Point2D(1,1)
        val grid = mutableMapOf(start to false)
        var cur = start
        var steps = 0
        val queue = mutableListOf(cur to 0)
        val visited = mutableSetOf(start)
        while (cur != target) {
            val pair = queue.removeFirst()
            cur = pair.first
            steps = pair.second
            visited.add(cur)
            queue.addAll(
                cur.neighbors((0..Int.MAX_VALUE), (0..Int.MAX_VALUE)).map {
                    grid[it] = formula(it, favNumber)
                    it to steps + 1
                }.filterNot { grid[it.first]!! || it.first in visited }
            )
        }
        println(steps)
    }

    @Test
    fun part2() {
        val start = Point2D(1,1)
        val grid = mutableMapOf(start to false)
        val queue = mutableListOf(start to 0)
        val visited = mutableSetOf(start)
        while (queue.isNotEmpty()) {
            val (cur, steps) = queue.removeFirst()
            visited.add(cur)
            queue.addAll(
                cur.neighbors((0..Int.MAX_VALUE), (0..Int.MAX_VALUE)).map {
                    grid[it] = formula(it, favNumber)
                    it to steps + 1
                }.filterNot { grid[it.first]!! || it.first in visited || it.second > 50 }
            )
        }
        println(visited.size)
    }
}