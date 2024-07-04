import org.junit.jupiter.api.Test
import tools.getResourceAsStrings


class aoc6 {

    @Test
    fun part1() {
        val input = getResourceAsStrings("/6/input.txt").map { it.trim() }
        input[0].indices.joinToString("") { ix ->
            input.map { it[ix] }
                .groupingBy { it }
                .eachCount()
                .toList()
                .maxByOrNull { it.second }!!
                .first
                .toString()
        }.let {
            println(it)
        }
    }

    @Test
    fun part2() {
        val input = getResourceAsStrings("/6/input.txt").map { it.trim() }
        input[0].indices.joinToString("") { ix ->
            input.map { it[ix] }
                .groupingBy { it }
                .eachCount()
                .toList()
                .minByOrNull { it.second }!!
                .first
                .toString()
        }.let {
            println(it)
        }
    }
}