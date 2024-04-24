package aoc

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.runBlocking
import org.example.tools.getResourceAsStrings
import kotlin.math.abs
import kotlin.test.Test
import kotlin.time.measureTime

class aoc12 {

    data class SpringRecord(
        val states: String,
        val damagedGroups: List<Int>,
        val prevSymbol: Char = '.'
    ) {
        fun matches() = states
            .split('.')
            .filter { it.isNotEmpty() }
            .map { it.length } == damagedGroups

        fun defined() = states.all { it != '?' }

        fun fold() = SpringRecord(
            List(5) { states }.joinToString("?"),
            (0..<5).flatMap { damagedGroups }
        )
    }

    private fun combinations(record: SpringRecord): Long =
        if (record.defined()) {
            1L.takeIf { record.matches() } ?: 0L
        } else {
            combinations(record.copy(states = record.states.replaceFirst('?', '.'))) +
                    combinations(record.copy(states = record.states.replaceFirst('?', '#')))
        }

    private fun List<Int>.decFirstIfNotEmpty() = if (isEmpty()) {
        listOf(Int.MIN_VALUE)
    } else {
        listOf(first() - 1) + drop(1)
    }

    private fun combinationsWithCache(
        record: SpringRecord,
        cache: MutableMap<SpringRecord, Long>
    ): Long {
        cache[record]?.let { return it }
        if (record.states.isEmpty()) return if (record.damagedGroups.sumOf { abs(it) } == 0) 1L else 0L
        if (record.damagedGroups.isNotEmpty() && record.damagedGroups.first() < 0) return 0L
        return when(record.states.first()) {
            '.' -> when (record.prevSymbol) {
                '.' -> combinationsWithCache(record.copy(states = record.states.dropWhile { it == '.' }, prevSymbol = '.'), cache)
                '#' -> if (record.damagedGroups.isEmpty() || record.damagedGroups.first() == 0) {
                        combinationsWithCache(record.copy(states = record.states.drop(1), damagedGroups = record.damagedGroups.drop(1), prevSymbol = '.'), cache)
                    } else {
                        0L
                    }
                else -> throw IllegalStateException("Unknown prev char ${record.prevSymbol}")
            }
            '?' -> combinationsWithCache(record.copy(states = record.states.replaceFirst('?', '#')), cache) +
                    combinationsWithCache(record.copy(states = record.states.replaceFirst('?', '.')), cache)
            '#' -> combinationsWithCache(record.copy(
                    states = record.states.drop(1),
                    damagedGroups = record.damagedGroups.decFirstIfNotEmpty(),
                    prevSymbol = '#',
                ), cache)
            else -> throw IllegalStateException("Unknown char ${record.states.first()}")
        }.also {
            cache[record] = it
        }
    }

    private fun parseInput(file: String) = getResourceAsStrings(file)
        .map { it.split(' ') }
        .map { (states, rawDamagedGroups) ->
            SpringRecord(states, rawDamagedGroups.split(',').map { it.toInt() })
        }

    @Test
    fun part1() {
        val input = parseInput("/12/input.txt")

        val tm = measureTime {
            input.sumOf { combinations(it) }.also { println(it) }
        }
        println(tm)
    }

    @Test
    fun part2() {
        val input = parseInput("/12/input.txt")
        runBlocking(Dispatchers.Default) {
            input.map {
                async {
                    combinationsWithCache(it.fold(), mutableMapOf())
                }
            }.awaitAll().sum().also { println(it) }
        }
    }
}