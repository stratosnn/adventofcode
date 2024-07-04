import org.junit.jupiter.api.Test
import tools.Point2D
import tools.getResource

class aoc1 {

    enum class Rotation {
        L, R
    }

    @Test
    fun part1 () {
        val steps = parseInput(getResource("/1/input.txt"))
        var pos = Point2D(0, 0)
        var direction = Point2D(0, 1)
        steps.forEach { (r, d) ->
            direction = when(r) {
               Rotation.L -> direction.rotate(270)
               Rotation.R -> direction.rotate(90)
            }
            pos += direction * d
        }
        println(pos.manhattanDistance(Point2D(0,0)))
    }

    @Test
    fun part2 () {
        val steps = parseInput(getResource("/1/input.txt"))
        var pos = Point2D(0, 0)
        var direction = Point2D(0, 1)
        val visited = mutableSetOf(pos)

        for ((r, distance) in steps) {
            direction = when(r) {
                Rotation.L -> direction.rotate(270)
                Rotation.R -> direction.rotate(90)
            }
            for (d in 1.. distance) {
                pos += direction
                if (visited.contains(pos)) {
                    println(pos.manhattanDistance(Point2D(0, 0)))
                    return
                } else {
                    visited.add(pos)
                }
            }
        }
    }

    fun parseInput(input: String) = input
        .split(",")
        .map { it.trim() }
        .map { Rotation.valueOf(it.first().toString()) to it.drop(1).toLong() }

}
