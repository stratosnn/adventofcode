package aoc

import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

typealias Graph = MutableMap<String, aoc25.Node>

class aoc25 {

    data class Node(
        val neighbours: MutableList<String> = mutableListOf(),
        val compactedNodes: MutableList<String> = mutableListOf()
    )

    fun parseInput(file: String) = buildMap<String, Node> {
        getResourceAsStrings(file).map { line ->
            val tokens = line.split(':', ' ')
            val a = tokens.first()
            tokens.drop(2).forEach { b ->
                getOrPut(a) { Node() }.neighbours.add(b)
                getOrPut(b) { Node() }.neighbours.add(a)
            }
        }
    }

    // Note: this is not a proper random pair generator.
    fun Graph.randomPair() = entries.random().let { (k, v) -> k to v.neighbours.random() }

    fun contractStep(graph: Graph) {
        val (a, b) = graph.randomPair()
        graph[a]!!.neighbours.forEach { other ->
            graph[other]!!.neighbours.removeAll { it == a }
            if (other != b) {
                graph[other]!!.neighbours.add(b)
                graph[b]!!.neighbours.add(other)
            }
        }
        graph[b]!!.compactedNodes.add(a)
        graph[b]!!.compactedNodes.addAll(graph[a]!!.compactedNodes)
        graph.remove(a)
    }

    fun contract(graph: Graph): Int {
        while (graph.size > 2) contractStep(graph)
        require(graph.values.first().neighbours.size == graph.values.last().neighbours.size)
        return graph.values.first().neighbours.size
    }

    @Test
    fun part1() {
        var minCut = 0
        var contractedGraph: Graph? = null
        while (minCut != 3) {
            contractedGraph = parseInput("/25/input.txt").toMutableMap()
            minCut = contract(contractedGraph)
        }

        val result = contractedGraph!!.values.fold(1) { acc, node -> acc * (node.compactedNodes.size + 1) }
        println(result)
    }
}
