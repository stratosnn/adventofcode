import com.github.shiguruikai.combinatoricskt.permutations
import org.junit.jupiter.api.Test
import tools.Point2D
import tools.getResourceAsStrings

class aoc24 {

    companion object {
        val navigatable = buildList<Char> {
            addAll('0'..'9')
            add('.')
        }.toSet()
    }

    fun parseInput(file: String) = getResourceAsStrings(file).flatMapIndexed { y, line ->
        line.mapIndexed { x, c ->
            Point2D(x, y) to c
        }
    }.toMap()

    @Test
    fun part1() {
        val grid = parseInput("/24/input.txt")
        val poi = grid.filter { it.value in '0'..'9' }.map { it.value to it.key }.associate { it }
        val routes = poi.map { (c, p) ->
            val distances = grid.bfs(p, poi)
            c to distances
        }.toMap()

        val shortest = routes.keys.permutations().map {
            it.fold('0' to 0) { (prev, dist), c ->
                c to (dist + routes[prev]!![c]!!)
            }.second
        }.min()

        println(shortest)
    }

    @Test
    fun part2() {
        val grid = parseInput("/24/input.txt")
        val poi = grid.filter { it.value in '0'..'9' }.map { it.value to it.key }.associate { it }
        val routes = poi.map { (c, p) ->
            val distances = grid.bfs(p, poi)
            c to distances
        }.toMap()

        val shortest = routes.keys.permutations().map {
            val (last, dist) = it.fold('0' to 0) { (prev, dist), c ->
                c to (dist + routes[prev]!![c]!!)
            }
            dist + routes[last]!!['0']!!
        }.min()

        println(shortest)
    }


    fun Map<Point2D, Char>.bfs(start: Point2D, poi: Map<Char, Point2D>): Map<Char, Int> {
        val endMarks = poi.keys
        val queue = ArrayDeque<Pair<Point2D, Int>>(1024)
        val distances = mutableMapOf<Char, Int>()
        queue.addLast(start to 0)
        val visited = mutableSetOf<Point2D>()
        while (queue.isNotEmpty()) {
            val (current, distance) = queue.removeFirst()
            if (current in visited) continue
            visited.add(current)
            val c = this[current]
            if (c in endMarks) {
                distances[c!!] = distance
            }
            queue.addAll(current.neighbors().filter { this[it] in navigatable && it !in visited }.map { it to distance + 1 })
        }
        return distances
    }
}