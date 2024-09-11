import org.junit.jupiter.api.Test
import kotlin.math.log2
import kotlin.math.pow
import kotlin.collections.ArrayDeque

class aoc19 {

    companion object {
        const val INPUT = 3017957
//        const val INPUT = 5
    }

    @Test
    fun part1() {
        val p2 = log2(INPUT.toDouble()).toInt()
        println(1 + 2 * (INPUT - 2.0.pow(p2.toDouble()).toInt()))
    }

    @Test
    fun part2() {
        val left = ArrayDeque<Int>()
        val right = ArrayDeque<Int>()

        repeat(INPUT) {
            if (it < (INPUT / 2) + 1) {
                left.addLast(it + 1)
            } else {
                right.addFirst(it + 1)
            }
        }

        while (left.size + right.size > 1) {
            if (left.size > right.size) {
                left.removeLast()
            } else {
                right.removeLast()
            }
            right.addFirst(left.removeFirst())
            left.addLast(right.removeLast())
        }
        println("$left $right")

    }
}