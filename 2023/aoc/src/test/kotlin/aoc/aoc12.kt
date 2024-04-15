package aoc

import org.example.tools.getResourceAsStrings
import kotlin.test.Test
import kotlin.time.measureTime

class aoc12 {

    data class SpringRecord(
        val states: String,
        val damagedGroups: List<Int>,
    ) {
        private val cachedSum by lazy { damagedGroups.sum() }

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

    private fun combinationsWithCache(record: SpringRecord, cache: MutableMap<SpringRecord, Long>): Long {
        cache[record]?.let { return it }
        if (record.states.isEmpty()) return if (record.damagedGroups.isEmpty()) 1L else 0L
        return when(record.states.first()) {
            '.' -> combinationsWithCache(record.copy(states = record.states.dropWhile { it == '.' }), cache)
            '?' -> combinationsWithCache(record.copy(states = "#" + record.states.drop(1)), cache) +
                    combinationsWithCache(record.copy(states = "." + record.states.drop(1)), cache)
            '#' -> TODO()
            else -> throw IllegalStateException("Unknown char ${record.states.first()}")
        }.also { cache[record] = it }
    }

    private fun parseInput(file: String) = getResourceAsStrings(file).map {
        val (states, rawDamagedGroups) = it.split(' ')
        SpringRecord(states, rawDamagedGroups.split(',').map { it.toInt() })
    }

    @Test
    fun part1() {
        val input = parseInput("/12/input.txt")

        val tm = measureTime {
//            runBlocking(Dispatchers.Default) {
//                input.map {
//                    async {
//                        simpleCombinations(it) //.also { println(it) }
//                    }
//                }.awaitAll().sum().also { println(it) }
//            }
            input.sumOf { combinations(it) }.also { println(it) }
        }
        println(tm)
    }
}