package main

import (
	"bufio"
	"log"
	"math"
	"os"
)

// PART 1

// Your input is a map of city blocks represented by a digit that indicates the
// cost of moving to that block. You start at the top left corner and need to
// move to the bottom right corner.
// You can move at most three blocks in a single direction, then you must turn 90
// degrees left or right. You can't reverse direction; after entering a block,
// you  may only turn left, continue straight, or turn right.
// What is the least cost of moving from the top left corner to the bottom right?

func readInput() []string {
	file, err := os.Open("../../input/17")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var lines []string

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	return lines
}

type World struct {
	blocks [][]int
	lenX   int
	lenY   int
}

type Pos struct {
	x int
	y int
}

func (w *World) get_cost(p Pos) int {
	return w.blocks[p.y][p.x]
}

func buildWorld() World {
	lines := readInput()
	world := World{lenX: len(lines[0]), lenY: len(lines)}
	world.blocks = make([][]int, world.lenY)
	for y, line := range lines {
		world.blocks[y] = make([]int, world.lenX)
		for x, cost := range line {
			world.blocks[y][x] = int(cost - '0')
		}
	}
	return world
}

type Direction [2]int

var N = Direction{0, -1}
var E = Direction{1, 0}
var S = Direction{0, 1}
var W = Direction{-1, 0}
var still = Direction{0, 0}

type Step struct {
	pos    Pos       // position we are in
	dir    Direction // direction we are going
	length int       // steps already taken in this direction
}

type Path struct {
	cost int
	path []Pos
	step Step
}

func (p *Path) currentPos() Pos {
	// Return the current position of the path
	return p.path[len(p.path)-1]
}

type Frontier struct {
	pathsByCost map[int][]Path
	minCost     int
}

func (f *Frontier) setMinCost() {
	// set the minimum cost in frontier
	f.minCost = math.MaxInt
	for cost := range f.pathsByCost {
		if cost < f.minCost {
			f.minCost = cost
		}
	}
}

func (f *Frontier) pop() Path {
	// pop the path with the lowest cost from frontier
	path := f.pathsByCost[f.minCost][0]
	f.pathsByCost[f.minCost] = f.pathsByCost[f.minCost][1:]
	if len(f.pathsByCost[f.minCost]) == 0 {
		delete(f.pathsByCost, f.minCost)
		f.setMinCost()
	}
	return path
}

func (f *Frontier) add(path Path) {
	// add a path to frontier
	if _, ok := f.pathsByCost[path.cost]; !ok {
		f.pathsByCost[path.cost] = []Path{}
	}
	f.pathsByCost[path.cost] = append(f.pathsByCost[path.cost], path)
	if path.cost < f.minCost {
		f.minCost = path.cost
	}
}

func opposite(dir Direction) Direction {
	// return the opposite direction
	switch dir {
	case N:
		return S
	case E:
		return W
	case S:
		return N
	case W:
		return E
	case still:
		return still
	}
	panic("Unknown direction")
}

func (w *World) leastCost(start, end Pos) Path {
	// Take a start and end position and return the path with the least cost of
	// moving from start to end.
	step := Step{pos: start, dir: still, length: 0}
	path := Path{cost: 0, path: []Pos{start}, step: step}

	frontier := Frontier{pathsByCost: make(map[int][]Path)}
	frontier.add(path)

	visited := make(map[Step]bool)
	visited[step] = true

	for len(frontier.pathsByCost) > 0 {
		path := frontier.pop()
		current := path.currentPos()
		if current == end {
			return path
		}
		for _, nextDir := range []Direction{N, E, S, W} {
			nextPos := Pos{current.x + nextDir[0], current.y + nextDir[1]}
			if nextPos.x < 0 || nextPos.x >= w.lenX || // out of bounds
				nextPos.y < 0 || nextPos.y >= w.lenY || // out of bounds
				nextDir == opposite(path.step.dir) || // can't reverse
				nextDir == path.step.dir && path.step.length == 3 { // must turn
				continue
			}
			var nextLength int
			if nextDir == path.step.dir {
				nextLength = path.step.length + 1
			} else {
				nextLength = 1
			}
			nextStep := Step{pos: nextPos, dir: nextDir, length: nextLength}
			if visited[nextStep] {
				continue
			}

			nextCost := path.cost + w.get_cost(nextPos)

			nextPathPath := make([]Pos, len(path.path))
			copy(nextPathPath, path.path)
			nextPathPath = append(nextPathPath, nextPos)

			frontier.add(Path{cost: nextCost, path: nextPathPath, step: nextStep})
			visited[nextStep] = true
		}
	}
	panic("No path found")
}

func answer1() int {
	w := buildWorld()
	minPath := w.leastCost(Pos{0, 0}, Pos{w.lenX - 1, w.lenY - 1})
	return minPath.cost
}

// -----------------------------------------------------------------------

// PART 2

// Now when we move in a direction we need to move a minimum of 4 steps and a maximum
// of 10 steps. What is the new least cost of moving from the top left corner to the
// bottom right?

func (w *World) leastCost2(start, end Pos) Path {
	// Take a start and end position and return the path with the least cost of
	// moving from start to end.
	step := Step{pos: start, dir: still, length: 0}
	path := Path{cost: 0, path: []Pos{start}, step: step}

	frontier := Frontier{pathsByCost: make(map[int][]Path)}
	frontier.add(path)

	visited := make(map[Step]bool)
	visited[step] = true

	for len(frontier.pathsByCost) > 0 {
		path := frontier.pop()
		current := path.currentPos()
		if current == end {
			return path
		}
		for _, nextDir := range []Direction{N, E, S, W} {
			if nextDir == opposite(path.step.dir) ||
				nextDir == path.step.dir {
				continue // can't reverse or continue straight
			}
			for nextLength := 4; nextLength <= 10; nextLength++ {
				next_pos := Pos{current.x + nextDir[0]*nextLength,
					current.y + nextDir[1]*nextLength}
				if next_pos.x < 0 || next_pos.x >= w.lenX ||
					next_pos.y < 0 || next_pos.y >= w.lenY {
					continue
				}
				nextStep := Step{pos: next_pos, dir: nextDir, length: nextLength}
				if visited[nextStep] {
					continue
				}

				nextCost := path.cost
				for i := 1; i <= nextLength; i++ {
					pos := Pos{current.x + nextDir[0]*i, current.y + nextDir[1]*i}
					nextCost += w.get_cost(pos)
				}

				nextPathPath := make([]Pos, len(path.path))
				copy(nextPathPath, path.path)
				nextPathPath = append(nextPathPath, next_pos)

				frontier.add(Path{cost: nextCost, path: nextPathPath, step: nextStep})
				visited[nextStep] = true
			}
		}
	}
	panic("No path found")
}

func answer2() int {
	w := buildWorld()
	minPath := w.leastCost2(Pos{0, 0}, Pos{w.lenX - 1, w.lenY - 1})
	return minPath.cost
}

// -----------------------------------------------------------------------

var correctAnswers = map[int]int{
	1: 1044,
	2: 1227,
}

var answerFuncs = map[int]func() int{
	1: answer1,
	2: answer2,
}

func printAndTest(question int) {
	answer := answerFuncs[question]()
	correctAnswer, ok := correctAnswers[question]
	if ok && answer != correctAnswer {
		log.Fatal("Wrong answer, expected ", correctAnswer, " got ", answer)
	}
	println(answer)
}

func main() {
	// if no argument, run all answers, otherwise only part 1 or 2
	if len(os.Args) == 1 || os.Args[1] == "1" {
		printAndTest(1)
	}
	if len(os.Args) == 1 || os.Args[1] == "2" {
		printAndTest(2)
	}
	if len(os.Args) > 1 && os.Args[1] != "1" && os.Args[1] != "2" {
		println("Give 1 or 2 as argument, or no argument at all")
	}
}
