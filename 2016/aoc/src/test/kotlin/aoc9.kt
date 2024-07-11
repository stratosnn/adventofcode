import org.junit.jupiter.api.Test
import tools.getResource

class aoc9 {

    fun decompress(input: String): String {
        val result = StringBuilder()
        var i = 0
        while (i < input.length) {
            if (input[i] == '(') {
                val markerEnd = input.indexOf(')', i)
                val marker = input.substring(i + 1, markerEnd)
                val (chars, repeat) = marker.split('x').map { it.toInt() }
                val data = input.substring(markerEnd + 1, markerEnd + 1 + chars)
                repeat(repeat) { result.append(data) }
                i = markerEnd + 1 + chars
            } else {
                result.append(input[i])
                i++
            }
        }
        return result.toString()
    }

    fun count(input: String): Long {
        var length = 0L
        var i = 0
        while (i < input.length) {
            if (input[i] == '(') {
                val markerEnd = input.indexOf(')', i)
                val marker = input.substring(i + 1, markerEnd)
                val (chars, repeat) = marker.split('x').map { it.toInt() }
                val data = input.substring(markerEnd + 1, markerEnd + 1 + chars)
                length += repeat * count(data)
                i = markerEnd + 1 + chars
            } else {
                length++
                i++
            }
        }
        return length
    }

    @Test
    fun part1() {
        val input = getResource("/9/input.txt")
        println(decompress(input).length)
    }

    @Test
    fun part2() {
        val input = getResource("/9/input.txt")
        println(count(input))
    }

}