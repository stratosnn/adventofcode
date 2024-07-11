import org.junit.jupiter.api.Test
import tools.getResourceAsStrings

data class Registers(val map: MutableMap<String, Int> = mutableMapOf("a" to 0, "b" to 0, "c" to 0, "d" to 0)) : MutableMap<String, Int> by map {
    var a: Int by map
    var b: Int by map
    var c: Int by map
    var d: Int by map
}

class Computer(
    val commands: List<Instruction>,
    val reg: Registers = Registers(),
    var frame: Int = 0
) {
    fun run() {
        while (frame < commands.size) {
            commands[frame].execute(this)
        }
    }
}

sealed interface Instruction {
    fun execute(computer: Computer)
}

data class Cpy(
    val src: String,
    val dst: String,
) : Instruction {
    override fun execute(computer: Computer) {
        val value = src.toIntOrNull() ?: computer.reg[src]!!
        computer.reg[dst] = value
        computer.frame++
    }
}

data class Inc(
    val reg: String,
) : Instruction {
    override fun execute(computer: Computer) {
        computer.reg[reg] = computer.reg[reg]!!.inc()
        computer.frame++
    }
}

data class Dec(
    val reg: String,
) : Instruction {
    override fun execute(computer: Computer) {
        computer.reg[reg] = computer.reg[reg]!!.dec()
        computer.frame++
    }
}

data class Jnz(
    val reg: String,
    val offset: Int
) : Instruction {
    override fun execute(computer: Computer) {
        if (computer.reg[reg] != 0) {
            computer.frame += offset
        } else {
            computer.frame++
        }
    }
}


class aoc12 {

    fun parseInput(fileName: String) = getResourceAsStrings(fileName).map { line ->
        val split = line.trim().split(" ")
        when (split[0]) {
            "cpy" -> Cpy(split[1], split[2])
            "inc" -> Inc(split[1])
            "dec" -> Dec(split[1])
            "jnz" -> Jnz(split[1], split[2].toInt())
            else -> error("Cannot parse instruction $line")
        }
    }

    @Test
    fun part1() {
        val input = parseInput("/12/input.txt")
        val computer = Computer(input)
        computer.apply { run() }.also { println(it.reg.a) }
    }

    @Test
    fun part2() {
        val input = parseInput("/12/input.txt")
        val computer = Computer(input, Registers().apply { c = 1 })
        computer.apply { run() }.also { println(it.reg.a) }
    }

}