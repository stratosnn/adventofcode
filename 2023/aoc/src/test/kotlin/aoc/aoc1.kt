package aoc

import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc1 {

    @Test
    fun part1() {
        val result = getResourceAsStrings("/1/input1.txt")
            .map { str -> str.filter { it.isDigit() } }
            .map { "${it.first()}${it.last()}" }
            .sumOf { it.toInt() }
        println(result)
    }

    @Test
    fun part2() {
        val mapping = mapOf(
            "one" to "o1e",
            "two" to "t2o",
            "three" to "t3e",
            "four" to "f4r",
            "five" to "f5e",
            "six" to "s6x",
            "seven" to "s7n",
            "eight" to "e8t",
            "nine" to "n9e"
        )

        val result = getResourceAsStrings("/1/input1.txt")
            .map { str -> mapping.entries.fold(str) { acc, (key, value) -> acc.replace(key, value) } }
            .map { str -> str.filter { it.isDigit() } }
            .map { "${it.first()}${it.last()}" }
            .sumOf { it.toInt() }
        println(result)
    }
}