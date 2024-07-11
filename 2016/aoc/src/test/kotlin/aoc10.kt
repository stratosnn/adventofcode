import org.junit.jupiter.api.Test
import tools.getResourceAsStrings


typealias BotInterceptor = (Bot) -> Unit

sealed interface NodeWithId {
    val id: Int
}

sealed class Node(
) : NodeWithId {
    fun getName() = "${javaClass.simpleName.lowercase()} $id"
    abstract fun process(chip: Int, network:  Map<String, Node>)
}

data class Output(
    override val id: Int,
    val chips: MutableList<Int>,
) : Node() {
    override fun process(chip: Int, network:  Map<String, Node>) {
        chips.add(chip)
    }
}

data class Bot(
    override val id: Int,
    val chips: MutableList<Int>,
    val low: String,
    val high: String,
    val interceptor: BotInterceptor
) : Node() {
    override fun process(chip: Int, network:  Map<String, Node>) {
        chips.add(chip)
        interceptor(this)
        if (chips.size == 2) {
            val (lowId, highId) = listOf(chips.minOf { it }, chips.maxOf { it })
            network[low]!!.process(lowId, network)
            network[high]!!.process(highId, network)
            chips.clear()
        }
    }
}

class aoc10 {

    fun parseInput(fileName: String, botInterceptor: BotInterceptor) = let {
        val lines = getResourceAsStrings(fileName)
        val values = lines.filter { it.startsWith("value") }.map { line ->
            val split = line.split(" ")
            split[1].toInt() to "${split[4]} ${split[5]}"
        }
        val bots = lines.filter { it.startsWith("bot") }.associate { line ->
            val split = line.split(" ")
            val bot = Bot(
                split[1].toInt(),
                mutableListOf(),
                "${split[5]} ${split[6]}",
                "${split[10]} ${split[11]}",
                botInterceptor
            )
            bot.getName() to bot
        }

        values to buildMap {
            putAll(bots)
            val outputs = bots.values.flatMap { bot ->
                    listOf(bot.low, bot.high)
                        .filter { it.startsWith("output") || it.startsWith("output") }
                        .map { output ->
                            val split = output.split(" ")
                            Output(split[1].toInt(), mutableListOf())
                        }
                }.associateBy { it.getName() }
            putAll(outputs)
        }
    }

    @Test
    fun part1() {
        val (values, bots) = parseInput("/10/input.txt") {
            if (it.chips.contains(61) && it.chips.contains(17)) {
                println(it.id)
            }
        }
        values.forEach { value ->
            bots[value.second]!!.process(value.first, bots)
        }
    }

    @Test
    fun part2() {
        val (values, bots) = parseInput("/10/input.txt") {}
        values.forEach { value ->
            bots[value.second]!!.process(value.first, bots)
        }

        (0..2).map { "output $it" }.fold(1) {
            acc, output ->
            acc * (bots[output]!! as Output).chips.first()
        }.also { println(it) }
    }
}