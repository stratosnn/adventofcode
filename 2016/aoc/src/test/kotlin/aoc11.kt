import com.github.shiguruikai.combinatoricskt.combinations
import org.junit.jupiter.api.Test

class aoc11 {

    enum class ElementType(val code: String) {
        MICROCHIP("M"),
        GENERATOR("G");

        override fun toString() = code
        operator fun unaryMinus() = when(this) {
            MICROCHIP -> GENERATOR
            GENERATOR -> MICROCHIP
        }
    }

    data class Item(
        val element: String,
        val type: ElementType
    ) {
        override fun toString() = "$element$type"
        operator fun unaryMinus() = Item(element, -type)
    }

    data class Building(
        val floors: List<Set<Item>>
    ) {
        val baseState by lazy { floors.map { it.map { it.type } } }
        constructor(vararg floors: Set<Item>) : this(floors.map { it })

        override fun toString() = floors.reversed().joinToString("\n") { it.joinToString() { it.toString() } }

        fun complete() = floors.dropLast(1).all { it.isEmpty() } && floors.last().isNotEmpty()

        fun valid() = floors.all { floor ->
            val generatorsAndNotShieldedChips = floor.filterNot { it.type == ElementType.MICROCHIP && -it in floor }
            generatorsAndNotShieldedChips.zipWithNext().all { it.first.type == it.second.type }
        }

        override fun equals(other: Any?): Boolean {
            return if (other is Building) {
                baseState == other.baseState
            } else {
                super.equals(other)
            }
        }

        override fun hashCode(): Int {
            return baseState.hashCode()
        }

        companion object {
            fun of(vararg floors: Set<String>) = Building(
                floors.map { floor ->
                    floor.map { item ->
                        assert(item.length >= 2)
                        Item(item.take(item.length - 1), if (item.last() == 'M') ElementType.MICROCHIP else ElementType.GENERATOR)
                    }.toSet()
                }
            )
        }
    }


    data class State(
        val building: Building,
        val elevatorFloor: Int,
        val steps: Int,
    ) {
        companion object {
            val validFloorRange =  0..<4
        }

        fun complete() = building.complete()
        fun valid() = building.valid()
        fun possibleMoves(): List<State> {
            val possibleLoad = building.floors[elevatorFloor].let { it.combinations(2) + it.combinations(1) }.map { it.toSet() }.toList()

            return listOf(elevatorFloor + 1, elevatorFloor - 1)
                .filter { it in validFloorRange }
                .flatMap { targetFloor ->
                    possibleLoad.mapNotNull { load ->
                        val newFloors = building.floors.toMutableList().apply {
                            this[elevatorFloor] = this[elevatorFloor] subtract load
                            this[targetFloor] = this[targetFloor] union load
                        }
                        Building(newFloors).takeIf { it.valid() }?.let { State(it, targetFloor, steps + 1) }
                    }
                }
        }
    }

    companion object {
        val sampleBuilding = Building(
            setOf(Item("H", ElementType.MICROCHIP), Item("L", ElementType.MICROCHIP)),
            setOf(Item("H", ElementType.GENERATOR)),
            setOf(Item("L", ElementType.GENERATOR)),
            setOf()
        )

        val inputBuilding = Building.of(
            setOf("PrG", "PrM"),
            setOf("CoG", "CuG", "RuG", "PlG"),
            setOf("CoM", "CuM", "RuM", "PlM"),
            setOf()
        )
    }

    fun resolve(building: Building): Int {
        val initialState = State(building, 0, 0)
        val visited = mutableSetOf<State>()
        val queue = ArrayDeque<State>(1024)
        queue.addLast(initialState)
        while(queue.isNotEmpty()) {
            val state = queue.removeFirst()
            if (state in visited) continue

            visited.add(state)
            if (state.complete()) {
                return state.steps
            } else {
                queue.addAll(state.possibleMoves())
            }
        }
        return -1
    }


    @Test
    fun part1() {
        println(resolve(inputBuilding))
    }

    @Test
    fun part2() {
        println(resolve(inputBuilding) + 2 * 12)
    }
}