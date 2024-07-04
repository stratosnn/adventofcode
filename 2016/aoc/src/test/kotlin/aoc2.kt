import org.junit.jupiter.api.Test
import tools.Point2D
import tools.getResourceAsStrings

class aoc2 {

    @Test
    fun part1() {
        val keypad = (0..<9).associate { Point2D(it % 3, it / 3) to it + 1 }

        val input = getResourceAsStrings("/2/input.txt")
        var (x, y)  = 1 to 1
        input.forEach { line ->
            line.forEach { step ->
                when (step) {
                    'U' -> if (y > 0) y--
                    'D' -> if (y < 2) y++
                    'L' -> if (x > 0) x--
                    'R' -> if (x < 2) x++
                }
            }
            print(keypad[Point2D(x, y)])
        }
    }

    @Test
    fun part2() {
        val keypad = mapOf(
            Point2D(2, 0) to 1,
            Point2D(1, 1) to 2,
            Point2D(2, 1) to 3,
            Point2D(3, 1) to 4,
            Point2D(0, 2) to 5,
            Point2D(1, 2) to 6,
            Point2D(2, 2) to 7,
            Point2D(3, 2) to 8,
            Point2D(4, 2) to 9,
            Point2D(1, 3) to 'A',
            Point2D(2, 3) to 'B',
            Point2D(3, 3) to 'C',
            Point2D(2, 4) to 'D'
        )

        val input = getResourceAsStrings("/2/input.txt")
        var (x, y)  = 0 to 2
        input.forEach { line ->
            line.forEach { step ->
                when (step) {
                    'U' -> if (keypad.containsKey(Point2D(x, y - 1))) y--
                    'D' -> if (keypad.containsKey(Point2D(x, y + 1))) y++
                    'L' -> if (keypad.containsKey(Point2D(x - 1, y))) x--
                    'R' -> if (keypad.containsKey(Point2D(x + 1, y))) x++
                }
            }
            print(keypad[Point2D(x, y)])
        }
    }
}
