package aoc

import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc7 {
    data class Hand(val value: String,) {
        val score: Int by lazy {
            val highOrderRank = grouping(value)
                .let { TYPES.indexOf(it) }
            value.fold(highOrderRank) { acc, c -> (acc shl 4) or (STRENGTH.indexOf(c)) }
        }

        val scoreWithJokers: Int by lazy {
            val withoutJokers = value.filter { it != 'J' }
            val type = grouping(withoutJokers)
                .toMutableList()
                .apply {
                    if(size > 0) {
                        this[0] += value.length - withoutJokers.length
                    } else {
                        add(5)
                    }
                }
                .let { TYPES.indexOf(it) }

            value.fold(type) { acc, c -> (acc shl 4) or (STRENGTH_WITH_JOKERS.indexOf(c)) }
        }

        companion object {
            private const val STRENGTH = "23456789TJQKA"
            private const val STRENGTH_WITH_JOKERS = "J23456789TQKA"
            private val TYPES = listOf(
                listOf(1,1,1,1,1),
                listOf(2,1,1,1),
                listOf(2,2,1),
                listOf(3,1,1),
                listOf(3,2),
                listOf(4,1),
                listOf(5),
            )
            private fun grouping(value: String) = value
                .groupingBy { it }
                .eachCount()
                .values
                .sortedDescending()
        }
    }

    data class HandWithBid(val hand: Hand, val bid: Int) {
        constructor(hand: String, bid: Int) : this(Hand(hand), bid)
    }

    fun parseInput(file: String) = getResourceAsStrings(file).map {
        it.split(' ').let { (hand, bid) -> HandWithBid(hand, bid.toInt()) }
    }

    @Test
    fun part1() {
        val games = parseInput("/7/input.txt")
        val result = games.sortedBy { it.hand.score }
            .foldIndexed(0L) { ix, acc, hand -> acc + (ix + 1) * hand.bid }
        println(result)
    }

    @Test
    fun part2() {
        val games = parseInput("/7/input.txt")
        val result = games.sortedBy { it.hand.scoreWithJokers }
            .foldIndexed(0L) { ix, acc, hand -> acc + (ix + 1) * hand.bid }
        println(result)
    }

}