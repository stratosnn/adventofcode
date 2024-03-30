package aoc

import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc2 {
    private val gameIdRegex = Regex("""Game (?<game>\d+)""")
    private val colorRegex = mapOf(
        "red" to Regex("""(?<red>\d+) red"""),
        "green" to Regex("""(?<green>\d+) green"""),
        "blue" to Regex("""(?<blue>\d+) blue"""),
    )

    data class Color(val rgb: List<UInt>) {
        val red: UInt
            get() = rgb[0]
        val green: UInt
            get() = rgb[1]
        val blue: UInt
            get() = rgb[2]
    }
    data class Game(
        val id: UInt,
        val colors: List<Color>
    )

    private fun readGameData(line: String) = line.split(':').let { (game, rawData) ->
        Game(
            id = gameIdRegex.find(game)!!.groups["game"]!!.value.toUInt(),
            colors = rawData.split(';')
                .map { gameData ->
                    Color(colorRegex.map { (color, regex) ->
                            regex.find(gameData)?.groups?.get(color)?.value?.toUInt() ?: 0U
                        }
                    )
                }
        )
    }

    @Test
    fun part1() {
        val result = getResourceAsStrings("/2/input1.txt")
            .map { readGameData(it) }
            .filter { game ->
                game.colors.all { it.red <= 12U && it.green <= 13U && it.blue <= 14U }
            }.sumOf { it.id }
        println(result)
    }

    @Test
    fun part2() {
        val result = getResourceAsStrings("/2/input1.txt")
            .map { readGameData(it) }
            .sumOf { game ->
                game.colors.maxOf { it.red } * game.colors.maxOf { it.green } * game.colors.maxOf { it.blue }
            }
        println(result)
    }
}