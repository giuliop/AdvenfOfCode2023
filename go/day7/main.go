package main

import (
	"bufio"
	"log"
	"os"
	"sort"
)

// PART 1

// You will be playing camel poker.
// Your input is a list of hands of 5 cards and bids of this form:

// TQ5TT 421
// ...
// The first 5 characters are a card each, the digit is the bid.

// Cards are ranked (highest first) A K Q J T 9 8 7 6 5 4 3 2.
// Hands are ranked by type first and by highest card second,
// looking at cards in order from left to right.

// Types are (highest first):
// Five of a kind, e.g., AAAAA
// Four of a kind, e.g., AA8AA
// Full house: three of a kind and two of a kind, e.g., 23332
// Three of a kind, e.g., TTT98
// Two pairs, e.g., 23432
// One pair, e.g., A23A4
// High card, where all cards' labels are distinct, e.g.,  23456

// Rank all your hands from lowest to highest. The rank of the lowest hand is 1,
// the rank of the second lowest hand is 2, and so on.
// Multiply the rank of each hand by its bid, and add up all the products.

func readInput() []string {
	file, err := os.Open("../../input/7")
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

type HandType int

const (
	highCard HandType = iota
	onePair
	twoPairs
	threeOfAKind
	fullHouse
	fourOfAKind
	fiveOfAKind
)

type Hand struct {
	cards       [5]byte
	countByCard map[byte]int
	bid         int
	handType    HandType
}

func cardRank(c byte, joker bool) int {
	switch c {
	case 'A':
		return 14
	case 'K':
		return 13
	case 'Q':
		return 12
	case 'J':
        if joker {
            return 1
        }
		return 11
	case 'T':
		return 10
	default:
		return int(c - '0')
	}
}

func handType(h Hand, joker bool) HandType {
    var countByCard map[byte]int
    if joker {
        countByCard = jokerize(h.countByCard)
    } else {
        countByCard = h.countByCard
    }
	switch len(countByCard) {
	case 1:
		return fiveOfAKind
	case 2:
		for _, count := range countByCard {
			if count == 2 || count == 3 {
				return fullHouse
			}
			if count == 4 || count == 1 {
				return fourOfAKind
			}
		}
		panic("should not happen")
	case 3:
		for _, count := range countByCard {
			if count == 3 {
				return threeOfAKind
			}
			if count == 2 {
				return twoPairs
			}
		}
		panic("should not happen")
	case 4:
		return onePair
	case 5:
		return highCard
	}
	panic("should not happen")
}

func handfromString(s string, joker bool) Hand {
	// s is 5 chars of cards, 1 space, 1 or more digits for bid
	h := Hand{
		countByCard: make(map[byte]int),
	}
	for i := 0; i < 5; i++ {
		h.cards[i] = s[i]
		h.countByCard[s[i]]++
	}
	h.bid = 0
	for i := 6; i < len(s); i++ {
		h.bid = h.bid*10 + int(s[i]-'0')
	}
	h.handType = handType(h, joker)
	return h
}

func compareHands(h1, h2 Hand, joker bool) bool {
	// return true if h1 is lower ranked than h2
	if h1.handType != h2.handType {
		return h1.handType < h2.handType
	}
	for i := 0; i < 5; i++ {
		if h1.cards[i] != h2.cards[i] {
			return cardRank(h1.cards[i], joker) < cardRank(h2.cards[i], joker)
		}
	}
	panic("should not happen")
}

func answer1() int {
	var hands []Hand
	for _, line := range readInput() {
		hands = append(hands, handfromString(line, false))
	}
	// sort hands from lowest to highest
	sort.Slice(hands, func(i int, j int) bool {
		return compareHands(hands[i], hands[j], false)
	})
	rank := 1
	sum := 0
	for i := 0; i < len(hands); i++ {
		sum += rank * hands[i].bid
		rank++
	}
	return sum
}

// -----------------------------------------------------------------------

// PART 2

// Now `J` is a joker, it will be the card that makes your hand the highest.
// It's ranking is the lowest possible, lower than 2, so the new ranking is:
// A K Q J T 9 8 7 6 5 4 3 2 J
// Recalculate the ranking of all hands and the sum of the products of rank and bid.

func jokerize(countByCard map[byte]int) map[byte]int {
    // we turn the jokers into the card with the highest count
    newCountByCard := make(map[byte]int)
    var maxCountCard byte
    maxCount := 0
    for card, count := range countByCard {
        if card != 'J' {
            newCountByCard[card] = count
            if count > maxCount {
                maxCount = count
                maxCountCard = card
            }
        }
    }
    newCountByCard[maxCountCard] += countByCard['J']
    return newCountByCard
}

func answer2() int {
	var hands []Hand
	for _, line := range readInput() {
		hands = append(hands, handfromString(line, true))
	}
	// sort hands from lowest to highest
	sort.Slice(hands, func(i int, j int) bool {
		return compareHands(hands[i], hands[j], true)
	})
	rank := 1
	sum := 0
	for i := 0; i < len(hands); i++ {
		sum += rank * hands[i].bid
		rank++
	}
	return sum
}

// -----------------------------------------------------------------------

var correctAnswers = map[int]int{
	1: 248812215,
	2: 250057090,
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
