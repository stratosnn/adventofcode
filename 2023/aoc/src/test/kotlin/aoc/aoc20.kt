package aoc

import org.example.tools.getResourceAsStrings
import org.example.tools.lcm
import org.junit.jupiter.api.Test

class aoc20 {

    enum class Pulse() {
        HIGH, LOW;

        companion object {
            fun fromBoolean(b: Boolean) = if (b) HIGH else LOW
        }
    }

    sealed interface Module {
        val name:  String
        val outputs: List<String>

        fun process(signal: Signal): List<Signal>
    }

    data class Button(override val name: String, override val outputs: List<String>) : Module {
        override fun process(signal: Signal) = emptyList<Signal>()
    }

    data class Broadcaster(override val name: String, override val outputs: List<String>) : Module {
        override fun process(signal: Signal) = outputs.map { Signal(name, it, signal.pulse) }
    }

    data class FlipFlop(override val name: String, override val outputs: List<String>, var state: Boolean = false) : Module {
        override fun process(signal: Signal) = when (signal.pulse) {
            Pulse.HIGH -> emptyList()
            Pulse.LOW -> outputs.map { Signal(name, it, Pulse.fromBoolean(!state)) }.also { state = !state }
        }
    }

    data class Conjunction(
        override val name: String,
        override val outputs: List<String>,
        var state: MutableMap<String, Pulse> = emptyMap<String, Pulse>().toMutableMap()
    ) : Module {
        override fun process(signal: Signal) = run {
            state[signal.from] = signal.pulse
            val newPulse = Pulse.fromBoolean(!state.values.all { it == Pulse.HIGH })
            outputs.map { Signal(name, it, newPulse) }
        }
    }

    fun parseInput(file: String) = getResourceAsStrings(file)
        .map {
            val (typeName, outputs) = it.split(" -> ")
            when {
                typeName.first() == '%' -> FlipFlop(typeName.drop(1), outputs.trim().split(", "))
                typeName.first() == '&' -> Conjunction(typeName.drop(1), outputs.trim().split(", "))
                typeName == "broadcaster" -> Broadcaster(typeName, outputs.trim().split(", "))
                else -> throw IllegalArgumentException("Unknown type $typeName")
            }
        }.associateBy {
            it.name
        }.also { moduleMap ->
            val conjunctions = moduleMap.values.filterIsInstance<Conjunction>().map { it.name }.toSet()
            moduleMap.forEach { (k, v) ->
                (v.outputs.toSet() intersect conjunctions).forEach { c ->
                    (moduleMap[c] as Conjunction).state[k] = Pulse.LOW
                }
            }
        }

    data class Signal(val from: String, val to: String, val pulse: Pulse)

    fun pushButton(moduleMap: Map<String, Module>): List<Signal> {
        val fifo = mutableListOf(Signal("button", "broadcaster", Pulse.LOW))
        val signals = mutableListOf<Signal>()

        while (fifo.isNotEmpty()) {
            val signal = fifo.removeFirst()
            signals.addLast(signal)

            moduleMap[signal.to]?.let { module -> fifo.addAll(module.process(signal)) }
        }
        return signals
    }

    @Test
    fun part1() {
        val moduleMap = buildMap {
            putAll(parseInput("/20/input.txt"))
            put("button", Button("button", listOf("broadcaster")))
        }

        val result = (0..<1000)
            .flatMap { pushButton(moduleMap).groupingBy { it.pulse }.eachCount().entries }
            .groupBy({ it.key }) { it.value }
            .mapValues { it.value.reduce(Int::plus) }
            .values
            .reduce(Int::times)

        println(result)
    }

    @Test
    fun part2() {
        val moduleMap = buildMap {
            putAll(parseInput("/20/input.txt"))
            put("button", Button("button", listOf("broadcaster")))
        }

        val rxInput = moduleMap.values.first { it.outputs.contains("rx") }
        check(rxInput is Conjunction)

        val selectedInputs = moduleMap.values.filter { it.outputs.contains(rxInput.name) }.map { it.name }.toSet()
        val selectedInputsCounter = emptyMap<String, Long>().toMutableMap()
        var cnt = 0L

        while (selectedInputsCounter.size < selectedInputs.size) {
            cnt++
            pushButton(moduleMap)
                .filter { it.from in selectedInputs && it.to == rxInput.name && it.pulse == Pulse.HIGH }
                .filter { it.from !in selectedInputsCounter }
                .forEach { selectedInputsCounter[it.from] = cnt }
        }

        println(selectedInputsCounter.values.reduce(Long::lcm))
    }
}