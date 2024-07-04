import org.junit.jupiter.api.Test
import tools.getResourceAsStrings

class aoc7 {

    @Test
    fun part1() {
        val input = getResourceAsStrings("/7/input.txt").map { line ->
            line.trim().split("]", "[").filterNot { it.isEmpty() }
        }
        input.count { segments ->
            segments.mapIndexed { segmentIx, segment ->
                val hasInvertedPair = (1..<segment.length-2).any { ix ->
                    segment[ix] == segment[ix+1] && segment[ix-1] == segment[ix+2] && segment[ix] != segment[ix-1]
                }
                segmentIx to hasInvertedPair
            }.let { ixToHasInvertedPair ->
                // Odd indexes are within braces
                val hasPairInBraces = ixToHasInvertedPair.any { (ix, hasPair) -> ix % 2 == 1 && hasPair }
                if (hasPairInBraces) {
                    false
                } else {
                    ixToHasInvertedPair.any { (ix, hasPair) -> ix % 2 == 0 && hasPair }
                }
            }
        }.let {
            println(it)
        }
    }


    @Test
    fun part2() {
        val input = getResourceAsStrings("/7/input.txt").map { line ->
            line.trim().split("]", "[").filterNot { it.isEmpty() }
        }
        input.count { segments ->
            val superNetSeq = segments.mapIndexedNotNull { segmentIx, segment -> segment.takeIf { segmentIx % 2 == 0 }}
            val hyperNetSeq = segments.mapIndexedNotNull { segmentIx, segment -> segment.takeIf { segmentIx % 2 == 1 }}
            val abaSeqsPerLine = superNetSeq.flatMap { segment ->
                (1..<segment.length-1).filter { ix ->
                    segment[ix] != segment[ix+1] && segment[ix-1] == segment[ix+1]
                }.map { ix -> segment.substring(ix - 1, ix + 2) }
            }
            abaSeqsPerLine.map { "${it[1]}${it[0]}${it[1]}" }.any { bab ->
                hyperNetSeq.any { it.contains(bab) }
            }
        }.let {
            println(it)
        }
    }

}