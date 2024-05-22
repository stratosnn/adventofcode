package common

type Point2D[T int | float64] struct {
	X, Y T
}

func (p Point2D[T]) Neighbours() []Point2D[T] {
	return []Point2D[T]{
		{p.X - 1, p.Y - 1},
		{p.X, p.Y - 1},
		{p.X + 1, p.Y - 1},
		{p.X - 1, p.Y},
		{p.X + 1, p.Y},
		{p.X - 1, p.Y + 1},
		{p.X, p.Y + 1},
		{p.X + 1, p.Y + 1},
	}
}
