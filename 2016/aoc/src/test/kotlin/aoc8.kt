import org.junit.jupiter.api.Test
import tools.getResourceAsStrings

fun BooleanArray.shift(offset: Int) {
    val copy = this.copyOf()
    indices.forEach { i ->
        this[(i + offset) % size] = copy[i]
    }
}

class aoc8 {

    sealed interface Command {
        fun execute(screen: Array<BooleanArray>)
    };

    class Rect(
        val width: Int,
        val height: Int,
    ) : Command {
        override fun execute(screen: Array<BooleanArray>) =
            (0..<height).forEach { y -> (0..<width).forEach { x -> screen[y][x] = true } }
    }

    sealed interface Rotate : Command {
        val position: Int
        val offset: Int
    }

    class RotateRow(
        override val position: Int,
        override val offset: Int,
    ) : Rotate {
        val row: Int by this::position
        override fun execute(screen: Array<BooleanArray>) =
            screen[row].shift(offset)
    }

    class RotateColumn(
        override val position: Int,
        override val offset: Int,
    ) : Rotate {
        val column: Int by this::position
        override fun execute(screen: Array<BooleanArray>) {
            val extracted = BooleanArray(screen.size) { x -> screen[x][column] }
            extracted.shift(offset)
            extracted.forEachIndexed { x, value -> screen[x][column] = value }
        }
    }


    fun draw(screen: Array<BooleanArray>) {
        screen.forEach { row ->
            row.forEach { print(if (it) "#" else " ") }
            println()
        }
    }

    fun parseCommands(fileName: String) = getResourceAsStrings(fileName)
        .map {
            val split = it.trim().split(" ")
            when {
                it.startsWith("rect") -> {
                    val (areaX, areaY) = split[1].split("x")
                    Rect(areaX.toInt(), areaY.toInt())
                }
                it.startsWith("rotate row") -> {
                    val (_, position) = split[2].split("=")
                    RotateRow(position.toInt(), split[4].toInt())
                }
                it.startsWith("rotate column") -> {
                    val (_, position) = split[2].split("=")
                    RotateColumn(position.toInt(), split[4].toInt())
                }
                else -> error("Unexpected command $it")
            }
        }

    @Test
    fun part1() {
        val commands = parseCommands("/8/input.txt")
        val screen = Array(6) { BooleanArray(50) }
        commands.forEach { it.execute(screen) }
        println(screen.sumOf { r -> r.count { it } })
    }

    @Test
    fun part2() {
        val commands = parseCommands("/8/input.txt")
        val screen = Array(6) { BooleanArray(50) }
        commands.forEach { it.execute(screen) }
        draw(screen)
    }

}