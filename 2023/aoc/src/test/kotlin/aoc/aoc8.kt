package aoc

import org.example.tools.getResourceAsStrings
import org.example.tools.lcm
import org.junit.jupiter.api.Test

class aoc8 {

    fun parseInput(file: String) = getResourceAsStrings(file)
        .let {
            it[0].trim() to it.drop(2).associate { str ->
                val (key, left, right) = str.split(' ', '(', ',', ')', '=').filter { it.isNotEmpty() }
                key to (left to right)
            }
        }

    fun countSteps(
        startPoint: String,
        path: String,
        desertMap: Map<String, Pair<String, String>>,
        condition:  (String) -> Boolean = { it != "ZZZ" }
    ): Int {
        var steps = 0
        var pos = startPoint
        do {
            when (path[steps++ % path.length]) {
                'L' -> pos = desertMap[pos]!!.first
                'R' -> pos = desertMap[pos]!!.second
            }
        } while (condition(pos))

        return steps
    }

    @Test
    fun part1() {
        val (path, desertMap) = parseInput("/8/input.txt")
        val steps =  countSteps("AAA", path, desertMap)
        println(steps)
    }

    @Test
    fun part2() {
        val (path, desertMap) = parseInput("/8/input.txt")

        val steps = desertMap
            .keys
            .filter { it.endsWith("A") }
            .map {
                countSteps(it, path, desertMap) { !it.endsWith("Z") }
            }.map { it.toLong() }
        val result = steps.reduce { acc, i -> acc.lcm(i) }

        println(result)
    }

}