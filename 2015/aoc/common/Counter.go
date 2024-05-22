package common

func Counter[T comparable](data []T) map[T]int {
	result := make(map[T]int)
	for _, v := range data {
		result[v]++
	}
	return result
}

func CounterStr(data string) map[byte]int {
	return Counter[byte]([]byte(data))
}
