import tools.getResourceAsStrings
import kotlin.test.Test

class aoc20 {

    private fun parseInput(file: String) = getResourceAsStrings(file).map {
        val raw = it.trim().split("-").map { it.toLong() }
        raw[0]..raw[1]
    }

    @Test
    fun part1() {
        val ranges = parseInput("/20/input.txt").sortedBy { it.first }
        var candidate = 0L
        ranges.forEach {
            if (it.first > candidate) {
                println(candidate)
                return
            }
            if (it.last > candidate) {
                candidate = it.last + 1
            }
        }
    }

    @Test
    fun part2() {
        val ranges = parseInput("/20/input.txt").sortedBy { it.first }
        var candidate = 0L
        var count = 0
        while (candidate <= UInt.MAX_VALUE.toLong()) {
            val r = ranges.find { it.first <= candidate && it.last >= candidate }
            r?.let { candidate = it.last + 1 } ?: run {
                candidate++
                count++
            }
        }
        println(count)
    }
}