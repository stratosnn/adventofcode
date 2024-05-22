package main

import (
	"fmt"
	"github.com/emirpasic/gods/sets/hashset"
	"math"
	"math/rand"
	"os"
	"regexp"
	"strings"
)

func main() {
	if input, err := os.ReadFile("19/input.txt"); err == nil {
		replacements, molecule := Parse(string(input))
		fmt.Println(part1(replacements, molecule))
		fmt.Println(part2c(replacements, molecule))
		// 208 too high
	}
}

var re = regexp.MustCompile(`^(\w+) => (\w+)$`)

func Parse(input string) (map[string][]string, string) {
	replacements := map[string][]string{}
	var molecule string
	for _, line := range strings.Split(input, "\n") {
		match := re.FindStringSubmatch(line)
		if len(match) == 3 {
			replacements[match[1]] = append(replacements[match[1]], match[2])
		} else if len(line) > 0 {
			molecule = line
		}
	}
	return replacements, molecule
}

func part1(replacements map[string][]string, molecule string) int {
	result := map[string]int{}
	for k, v := range replacements {
		sb := strings.Builder{}
		for prefix, suffix, found := strings.Cut(molecule, k); found; prefix, suffix, found = strings.Cut(suffix, k) {
			sb.WriteString(prefix)
			for _, vv := range v {
				result[sb.String()+vv+suffix]++
			}
			sb.WriteString(k)
		}
	}
	return len(result)
}

// Too big, did not work. Too many combinations
func part2a(replacements map[string][]string, molecule string) int {
	cnt := 0
	for arr, found := []string{"e"}, false; found == false; arr, found = bfs(arr, replacements, molecule) {
		cnt++
		fmt.Println(cnt)
		if cnt == 10 {
			return -1
		}
	}
	return cnt - 1
}

// Failed, does not yield "e" in the end
func part2b(replacements map[string][]string, molecule string) int {
	pairs := make([]Pair, 0, 4*len(replacements))
	for k, v := range replacements {
		for _, vv := range v {
			pairs = append(pairs, Pair{k, vv})
		}
	}

	cnt := 0
	for s, found := molecule, true; found; s, found = greedy(pairs, s) {
		cnt++
	}
	return cnt - 1
}

func part2c(replacements map[string][]string, molecule string) int {
	pairs := make([]Pair, 0, 4*len(replacements))
	for k, v := range replacements {
		for _, vv := range v {
			pairs = append(pairs, Pair{k, vv})
		}
	}

	// Find the shortest by running it enough(?) times
	r := math.MaxInt32
	for i := 0; i < 100; i++ {
		r = min(r, randomSolve(pairs, molecule, "e"))
	}
	return r
}

func bfs(arr []string, replacements map[string][]string, molecule string) (next []string, found bool) {
	nextSet := hashset.New()
	next = make([]string, 0, 8*len(arr))
	fmt.Println(len(arr))
	for i := 0; i < len(arr); i++ {
		cur := arr[i]
		if len(cur) > len(molecule) {
			continue
		} else if cur == molecule {
			return []string{}, true
		} else if len(arr) == 0 {
			panic("empty string array")
		}

		for k, v := range replacements {
			sb := strings.Builder{}
			for prefix, suffix, found := strings.Cut(cur, k); found; prefix, suffix, found = strings.Cut(suffix, k) {
				sb.WriteString(prefix)
				fullPrefix := sb.String()
				for _, vv := range v {
					newSb := strings.Builder{}
					newSb.WriteString(fullPrefix)
					newSb.WriteString(vv)
					newSb.WriteString(suffix)
					//next = append(next, sb.String()+vv+suffix)
					nextSet.Add(newSb.String())
				}
				sb.WriteString(k)
			}
		}

	}
	for _, v := range nextSet.Values() {
		next = append(next, fmt.Sprintf("%s", v))
	}

	return next, false
}

type Pair struct {
	From string
	To   string
}

func greedy(replacements []Pair, molecule string) (string, bool) {
	longestReplacementIx := -1
	longest := -1

	for ix, r := range replacements {
		if strings.Contains(molecule, r.To) && len(r.To) >= longest {
			longestReplacementIx = ix
			longest = len(r.To)
		}
	}

	if longestReplacementIx == -1 {
		return "", false
	}

	rep := replacements[longestReplacementIx]

	return strings.Replace(molecule, rep.To, rep.From, 1), true
}

func shuffleReplace(replacements []Pair, molecule string) (string, bool) {
	candidates := make([]Pair, 0, len(replacements))

	for _, r := range replacements {
		if strings.Contains(molecule, r.To) {
			candidates = append(candidates, r)
		}
	}

	if len(candidates) == 0 {
		return molecule, false
	}

	c := candidates[rand.Intn(len(candidates))]
	return strings.Replace(molecule, c.To, c.From, 1), true
}

func randomSolve(pairs []Pair, molecule string, target string) int {
	s := molecule
	steps := 0
	found := true

	for s != target {
		s, found = shuffleReplace(pairs, s)
		if !found && s != target {
			s = molecule
			steps = 0
		}
		steps++
	}
	return steps
}
