package aoc

import org.example.tools.getResource
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class aoc19 {

    infix fun IntRange.intersect(other: IntRange) =
        maxOf(this.first, other.first)..minOf(this.last, other.last)

    data class Part(val map: Map<String, Int>) {
        companion object {
            private val pattern = Regex("""\{x=(?<x>\d+),\s*m=(?<m>\d+),a=(?<a>\d+),\s*s=(?<s>\d+)}""")
            fun fromString(str: String) = pattern.find(str)!!.let { match ->
                Part("xmas".associate { it.toString() to match.groups[it.toString()]!!.value.toInt() })
            }
        }

        fun accessor(c: Char) = map[c.toString()]!!

        fun score() = map.values.sum()
    }

    data class PartRange(val map: Map<String, IntRange>) {
        fun copy(attribute: Char, range: IntRange) = PartRange(
            map.toMutableMap().apply { this[attribute.toString()] = range }
        )

        fun accessor(c: Char) = map[c.toString()]!!

        fun score() = map.values.fold(1L) { acc, range -> acc * range.count().toLong() }
    }


    enum class Condition(private val symbol: Char) {
        GT('>'),
        LS('<');

        companion object {
            fun fromChar(char: Char) = entries.first { it.symbol == char }
        }
    }

    data class Rule(
        val attribute: Char,
        val condition: Condition,
        val threshold: Int,
        val target: String,
    )

    data class RuleSet(
        val name: String,
        val rules: List<Rule>,
        val defaultTarget: String,
    ) {
        companion object {
            fun fromString(str: String): RuleSet {
                val rawRules = str
                    .substringAfter('{')
                    .substringBefore('}')
                    .split(",")
                return RuleSet(
                    name = str.substringBefore('{'),
                    rules = rawRules.take(rawRules.size - 1).map {
                        Rule(
                            attribute = it.first(),
                            condition = Condition.fromChar(it[1]),
                            threshold = it.substring(2).substringBefore(':').toInt(),
                            target = it.substringAfter(':')
                        )
                    },
                    defaultTarget = rawRules.last()
                )
            }
        }

        fun resolve(part: Part) = rules.firstOrNull { rule ->
            val value = part.accessor(rule.attribute)
            when (rule.condition) {
                Condition.GT -> value > rule.threshold
                Condition.LS -> value < rule.threshold
            }
        }?.target ?: defaultTarget
    }

    fun Map<String, RuleSet>.resolve(part: Part): String {
        var cur = this["in"]!!.resolve(part)
        while (cur !in setOf("A", "R")) {
            cur = this[cur]!!.resolve(part)
        }
        return cur
    }

    fun Map<String, RuleSet>.resolve(part: PartRange, ruleSet: RuleSet): List<PartRange> = when (ruleSet.name) {
        "A" -> listOf(part)
        "R" -> emptyList()
        else -> {
            var current = part
            ruleSet.rules.flatMap { rule ->
                val (matchedRange, missedRange) = when (rule.condition) {
                    Condition.LS -> 1..< rule.threshold to rule.threshold..4000
                    Condition.GT -> (rule.threshold + 1)..4000 to 1.. rule.threshold
                }
                val (matchedPartRange, missedPartRange) = listOf(matchedRange, missedRange)
                    .map { current.copy(rule.attribute, it intersect current.accessor(rule.attribute)) }
                current = missedPartRange
                resolve(matchedPartRange, this[rule.target]!!)
            } + resolve(current, this[ruleSet.defaultTarget]!!)
        }
    }

    fun parseInput(file: String) = getResource(file).let { data ->
        val (rawRules, rawParts) = data.split("\n\n")
        val rules = rawRules.lines().map { RuleSet.fromString(it.trim()) }.associateBy { it.name }
        val parts = rawParts.lines().map { Part.fromString(it.trim()) }
        rules to parts
    }

    @Test
    fun part1() {
        val (rules, parts) = parseInput("/19/input.txt")
        val processed = parts.map { part ->
            part to rules.resolve(part)
        }.groupBy({ it.second }) { it.first }

        val result = processed["A"]!!.sumOf { it.score() }
        println(result)
    }

    @Test
    fun part2() {
        val (parsedRules, _) = parseInput("/19/input.txt")
        val rules = buildMap {
            putAll(parsedRules)
            put("A", RuleSet("A", listOf(), "none"))
            put("R", RuleSet("R", listOf(), "none"))
        }

        val start = PartRange("xmas".associate{ it.toString() to 1..4000 })

        val partRanges = rules.resolve(start, rules["in"]!!)
        println(partRanges.sumOf { it.score() })
    }

    @Test
    fun `Can parse Part from string`() {
        val part = Part.fromString("{x=1679,m=44,a=2067,s=496}")
        assertEquals(Part(mapOf("x" to 1679, "m" to 44, "a" to 2067, "s" to 496)), part)
    }

    @Test
    fun `Can parse RuleSet from string`() {
        val ruleset = RuleSet.fromString("qqz{s>2770:qs,m<1801:hdj,R}")
        val expected = RuleSet(
            name = "qqz",
            rules = listOf(
                Rule('s', Condition.GT, 2770, "qs"),
                Rule('m', Condition.LS, 1801, "hdj"),
            ),
            defaultTarget = "R"
        )
        assertEquals(expected, ruleset)
    }
}