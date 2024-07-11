import org.junit.jupiter.api.Test

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
    val slots: List<Set<Item>>
) {
    constructor(vararg floors: Set<Item>) : this(floors.map { it })

    override fun toString() = slots.joinToString("\n") { it.joinToString() { it.toString() } }

    fun complete() = slots.dropLast(1).all { it.isEmpty() } && slots.last().isNotEmpty()

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

data class Elevator(
    val floor: Int,
    val load: List<Item>,
    val steps: Int,
)

data class State(
    val elevator: Elevator,
    val building: Building,
) {
    fun complete() = elevator.load.isEmpty() && building.complete()
}

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


//fun bfsStep(state: State): List<State> {
//
//}


class aoc11 {

    @Test
    fun part1() {

    }
}