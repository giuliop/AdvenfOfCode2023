package main

import (
	"bufio"
	"log"
	"os"
)

// PART 1

// Your input represents a pipe system. The system is made of a series of
// interconnected pipes making a closed loop and other pipes that are not
// connected to the loop.

// Each pipe is identified by a symbol:
// | is a vertical pipe connecting north and south.
// - is a horizontal pipe connecting east and west.
// L is a 90-degree bend connecting north and east.
// J is a 90-degree bend connecting north and west.
// 7 is a 90-degree bend connecting south and west.
// F is a 90-degree bend connecting south and east.
// . is ground; there is no pipe in this tile.

// One pipe in the loop is identified by the `S` symbol. This could be any
// of the pipe junctions above. Find the loop and calculate te number of
// steps to reach the furthest point from the `S` pipe.

var pipeDirs = map[byte][2]byte{
	'|': {'N', 'S'},
	'-': {'E', 'W'},
	'L': {'N', 'E'},
	'J': {'N', 'W'},
	'7': {'S', 'W'},
	'F': {'S', 'E'},
	'.': {},
}

type World struct {
	grid []string
	lenX int
	lenY int
}

func readInput() []string {
	file, err := os.Open("../../input/10")
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

type Pos struct {
	x int
	y int
}

func (w World) at(p Pos) byte {
	return w.grid[p.y][p.x]
}

func (w World) findStart() Pos {
	for y := 0; y < w.lenY; y++ {
		for x := 0; x < w.lenX; x++ {
			if w.at(Pos{x, y}) == 'S' {
				return Pos{x, y}
			}
		}
	}
	panic("No start found")
}

func theWorld() World {
	grid := readInput()
	return World{
		grid: grid,
		lenX: len(grid[0]),
		lenY: len(grid),
	}
}

func canConnect(pType byte, dir byte) bool {
	// returns true if pType can connect in the given direction
	// we assume we can always connect to `start`
	for _, d := range pipeDirs[pType] {
		if d == dir {
			return true
		}
	}
	return false
}

func connected(w World, p Pos) []Pos {
	// returns the positions connected to p
	res := []Pos{}
	for _, dir := range pipeDirs[w.at(p)] {
		switch dir {
		case 'N':
			if p.y > 0 && canConnect(w.at(Pos{p.x, p.y - 1}), 'S') {
				res = append(res, Pos{p.x, p.y - 1})
			}
		case 'S':
			if p.y < w.lenY-1 && canConnect(w.at(Pos{p.x, p.y + 1}), 'N') {
				res = append(res, Pos{p.x, p.y + 1})
			}
		case 'E':
			if p.x < w.lenX-1 && canConnect(w.at(Pos{p.x + 1, p.y}), 'W') {
				res = append(res, Pos{p.x + 1, p.y})
			}
		case 'W':
			if p.x > 0 && canConnect(w.at(Pos{p.x - 1, p.y}), 'E') {
				res = append(res, Pos{p.x - 1, p.y})
			}
		}
	}
	return res
}

type PathStep struct {
	pos   Pos
	steps int // steps to reach this position
}

type Path struct {
	start     Pos
	pathSteps map[Pos]int // postion visited: steps to reach it
	isLoop    bool
}

func (w World) pathFrom(start Pos) Path {
	// Take a start positions and return the complete path
	// from it traversing all possible positions

	path := Path{
		start:     start,
		pathSteps: make(map[Pos]int),
		isLoop:    false,
	}

	// we track the positions still to visit and the steps to reach them
	var toVisit []PathStep
	for _, pos := range connected(w, start) {
		toVisit = append(toVisit, PathStep{pos, 1})
	}
	if len(toVisit) == 0 {
		// no connected positions, return empty path
		return path
	}
	firstPos := toVisit[0].pos

	for len(toVisit) > 0 {
		// pop a pathStep to visit
		pos, currentSteps := toVisit[0].pos, toVisit[0].steps
		toVisit = toVisit[1:]

		// add to path
		path.pathSteps[pos] = currentSteps

		for _, newPos := range connected(w, pos) {
			if path.pathSteps[newPos] > 0 {
				// already visited, update # of steps if needed
				if currentSteps+1 < path.pathSteps[newPos] {
					path.pathSteps[newPos] = currentSteps + 1
				}
				continue
			}
			if newPos == start {
				if pos != firstPos {
					path.isLoop = true
				}
			} else {
				toVisit = append(toVisit, PathStep{newPos, currentSteps + 1})
			}
		}
	}
	return path
}

func maxSteps(steps map[Pos]int) int {
	max := 0
	for _, v := range steps {
		if v > max {
			max = v
		}
	}
	return max
}

func impossibleStart(w World, start Pos) bool {
	// returns true if start is not a valid start position for a loop,
	// i.e. it is connected to none, or only one position
	return len(connected(w, start)) < 2
}

func findLoop() (Path, World) {
	// Return the loop and the world with 'S' replaced by the
	// correct pipe type
	for startType := range pipeDirs {
		w := theWorld()
		start := w.findStart()
		w.grid[start.y] = w.grid[start.y][:start.x] + string(startType) + w.grid[start.y][start.x+1:]
		if impossibleStart(w, start) {
			continue
		}
		path := w.pathFrom(start)
		if path.isLoop {
			return path, w
		}
	}
	panic("No loop found")
}

func answer1() int {
	loop, _ := findLoop()
	return maxSteps(loop.pathSteps)
}

// -----------------------------------------------------------------------

// PART 2

func isLoopCell(path Path, pos Pos) bool {
	// returns true if pos is part of the loop path,
	if path.pathSteps[pos] > 0 || pos == path.start {
		return true
	}
	return false
}

func printWorld(w World) {
	for _, line := range w.grid {
		println(line)
	}
}

func answer2() int {
	loop, w := findLoop()
	insideCells := 0
	// Iterate over the cells in the grid to mark the ones inside the loop.
	// We can immediately exclude the grid border and the loop cells.
	// For the other cells we traverse the grid to the right from the cell
	// counting how many times we enter/exit the loop; if the number is
	// odd the cell is inside the loop.
	// To count the number of times we enter/exit the loop we need to be careful to
	// account for passing on an edge of the loop, so in practice by type of loop cell:
	// - : don't count
	// | : count
	// L,J,7,F: count 1 for each pair of opposite N/S directions, i.e., L/J and 7/F
	//			count for 0 while any other combination counts for 1. Note that these
	//			cells will always come in pairs so we just need to count either the
	//			north or south passes and check if they are odd or even.
	//
	for y := 1; y < w.lenY-1; y++ {
		for x := 1; x < w.lenX-1; x++ {
			if !isLoopCell(loop, Pos{x, y}) {
				intersections := 0
				northPasses := 0
				for x2 := x + 1; x2 < w.lenX; x2++ {
					p := Pos{x2, y}
					if isLoopCell(loop, p) {
						switch w.at(p) {
						case '|':
							intersections++
						case 'L', 'J':
							northPasses++
						default:
						}
					}
				}
				if (intersections+northPasses)%2 == 1 {
					insideCells++
				}
			}
		}
	}
	return insideCells
}

// -----------------------------------------------------------------------

var correctAnswers = map[int]int{
	1: 6768,
	2: 351,
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
