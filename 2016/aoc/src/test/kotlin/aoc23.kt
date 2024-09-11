import tools.getResourceAsStrings
import kotlin.test.Test


class aoc23 {

    data class Registers(val map: MutableMap<String, Int> = mutableMapOf("a" to 0, "b" to 0, "c" to 0, "d" to 0)) : MutableMap<String, Int> by map {
        var a: Int by map
        var b: Int by map
        var c: Int by map
        var d: Int by map
    }

    class Computer(
        val commands: MutableList<Instruction>,
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
        val offset: String
    ) : Instruction {
        override fun execute(computer: Computer) {
            if (computer.reg[reg] != 0) {
                computer.frame += offset.toIntOrNull() ?: computer.reg[offset]!!
            } else {
                computer.frame++
            }
        }
    }

    data class Tgl(
        val reg: String,
    ) : Instruction {
        override fun execute(computer: Computer) {
            val value = computer.reg[reg]!!
            val offset = computer.frame + value
            if (offset < computer.commands.size) {
                val newCommand = when (val oldCmd = computer.commands[offset]) {
                    is Inc -> Dec(oldCmd.reg)
                    is Tgl -> Inc(oldCmd.reg)
                    is Dec -> Inc(oldCmd.reg)
                    is Cpy -> Jnz(oldCmd.src, oldCmd.dst)
                    is Jnz -> Cpy(oldCmd.reg, oldCmd.offset)
                    else -> error("Cannot toggle instruction ${computer.commands[offset]}")
                }
                computer.commands[offset] = newCommand
            }
            computer.frame++
        }
    }

    fun parseInput(fileName: String) = getResourceAsStrings(fileName).map { line ->
        val split = line.trim().split(" ")
        when (split[0]) {
            "cpy" -> Cpy(split[1], split[2])
            "inc" -> Inc(split[1])
            "dec" -> Dec(split[1])
            "jnz" -> Jnz(split[1], split[2])
            "tgl" -> Tgl(split[1])
            else -> error("Cannot parse instruction $line")
        }
    }

    @Test
    fun part1() {
        val commands = parseInput("/23/input.txt").toMutableList()
        val computer = Computer(commands, Registers().apply { a = 7 })
        computer.apply { run() }.also { println(it.reg.a) }
    }

    @Test
    fun part2() {
        List(7) {
            val commands = parseInput("/23/input.txt").toMutableList()
            val computer = Computer(commands, Registers().apply { a = it + 6 })
            computer.apply { run() }
            computer.reg
        }.forEachIndexed() { ix, v -> println("${ix + 6} -> $v") }
    }
}