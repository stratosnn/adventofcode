package aoc

import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test
import kotlin.math.pow

class aoc4 {

    data class Card(
        val id: Int,
        val winning: Set<Int>,
        val current: Set<Int>,
    )

    private fun parseInput(path: String) =
        getResourceAsStrings(path)
            .map { str ->
                val (rawGame, rawWinning, rawCurrent) = str.split(':', '|').map {
                    it.trim().split(' ').filter { it.isNotEmpty() }
                }
                Card(
                    id = rawGame[1].toInt(),
                    winning = rawWinning.map { it.toInt() }.toSet(),
                    current = rawCurrent.map { it.toInt() }.toSet(),
                )
            }


    @Test
    fun part1() {
        val result = parseInput("/4/input1.txt")
            .sumOf { card ->
                (card.winning intersect card.current)
                    .takeIf { it.isNotEmpty() }
                    ?.let { 2.0.pow(it.size - 1).toInt() } ?: 0
            }
        println(result)
    }

    @Test
    fun part2() {
        val cards = parseInput("/4/input1.txt")
        val dag = mutableMapOf<Int, Long>()
        cards.reversed().forEach { card ->
            dag[card.id] = (card.winning intersect card.current)
                .size
                .takeIf { it > 0 }
                ?.let {
                    ((card.id + 1)..(card.id + it)).sumOf { copyId -> dag[copyId]!! } + 1
                } ?: 1
        }

        println(dag.values.sum())
    }
}