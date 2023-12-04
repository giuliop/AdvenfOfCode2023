package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

// PART 1

// You have input such as this, a list of "games":
// Game 2: 6 blue, 3 green; 4 red, 1 green, 7 blue; 2 green

// You have to ouput the sum of game ids (e.g., 2 above) that are valid,
// that is that have a number of balls equal or lower with the following:
// 12 red cubes, 13 green cubes, and 14 blue cubes

func readInput() []string {
	file, err := os.Open("../../input/2")
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

type Draw struct {
	red   int
	green int
	blue  int
}

type Game struct {
	id    int
	draws []Draw
}

func fillDraw(draw *Draw, color string, numberString string) {
	number, _ := strconv.Atoi(numberString)
	switch color {
	case "red":
		draw.red = number
	case "green":
		draw.green = number
	case "blue":
		draw.blue = number
	}
}

func gameFromString(game string) Game {
	parts := strings.Split(game, ":")
	idString, drawsString := parts[0], parts[1]
	id, _ := strconv.Atoi(strings.Split(idString, " ")[1])

	var draws []Draw
	for _, drawString := range strings.Split(drawsString, ";") {
		var draw Draw
		for _, cube := range strings.Split(drawString, ",") {
			cube = strings.Trim(cube, " ")
			parts := strings.Split(cube, " ")
			numberString, color := parts[0], parts[1]
			fillDraw(&draw, color, numberString)
		}
		draws = append(draws, draw)
	}
	return Game{id, draws}
}

func gamesData() []Game {
	var data []Game
	for _, gameString := range readInput() {
		data = append(data, gameFromString(gameString))
	}
	return data
}

func validGame(game Game) bool {
	for _, draw := range game.draws {
		if draw.red > 12 || draw.green > 13 || draw.blue > 14 {
			return false
		}
	}
	return true
}

func answer1() int {
	var sum int
	for _, game := range gamesData() {
		if validGame(game) {
			sum += game.id
		}
	}
	return sum
}

// -----------------------------------------------------------------------

// PART 2

// For each game, find the minimum number of balls needed to make it valid.
// Then multiply this minimum number of balls together to find the `power`
// of that game. Return the sum of all powers.

func minimum_balls(game Game) Draw {
	var minimum Draw
	for _, draw := range game.draws {
		if draw.red > minimum.red {
			minimum.red = draw.red
		}
		if draw.green > minimum.green {
			minimum.green = draw.green
		}
		if draw.blue > minimum.blue {
			minimum.blue = draw.blue
		}
	}
	return minimum
}

func power(draw Draw) int {
	return draw.red * draw.green * draw.blue
}

func answer2() int {
	var sum int
	for _, game := range gamesData() {
		minimum := minimum_balls(game)
		sum += power(minimum)
	}
	return sum
}

// -----------------------------------------------------------------------

var correctAnswers = map[int]int{
	1: 2406,
	2: 78375,
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
