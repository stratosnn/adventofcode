import org.junit.jupiter.api.Test
import tools.getResource
import tools.getResourceAsStrings

class aoc3 {

    @Test
    fun part1() {
        println(solve(parseInput1("/3/input.txt")))
    }

    @Test
    fun part2() {
        println(solve(parseInput2("/3/input.txt")))
    }

    private fun solve(triangles: List<List<Int>>) = triangles
        .map { (a, b, c) -> a + b > c && a + c > b && b + c > a }
        .count { it }

    private fun parseInput1(fileName: String) = getResourceAsStrings(fileName).map { line ->
        line.split(" ").filterNot { it.isEmpty() }.map { it.toInt() }
    }

    private fun parseInput2(fileName: String) = getResource(fileName)
        .trim()
        .split("\\s+".toRegex())
        .map { it.toInt() }
        .let {
            buildList {
                for (i in it.indices step 9) {
                    for (offset in 0..2) {
                        add(listOf(it[i + offset], it[i + offset + 3], it[i + offset + 6]))
                    }
                }
            }
        }
}