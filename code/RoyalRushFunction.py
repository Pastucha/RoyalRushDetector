POKER_HAND_RANKS = {
    10: "Royal Flush",
    9: "Straight Flush",
    8: "Four of a Kind",
    7: "Full House",
    6: "Flush",
    5: "Straight",
    4: "Three of a Kind",
    3: "Two Pair",
    2: "Pair",
    1: "High Card"
}

def convert_rank(rank):
    
    rank_conversion = {"A": 14, "K": 13, "Q": 12, "J": 11}
    return rank_conversion.get(rank, int(rank) if rank.isdigit() else None)

def parse_card(card):
    
    if len(card) == 2:
        rank, suit = card[0], card[1]
    else:
        rank, suit = card[0:2], card[2]
    return convert_rank(rank), suit

def is_royal_flush(sorted_ranks, suits):
    return suits.count(suits[0]) == 5 and sorted_ranks == [10, 11, 12, 13, 14]

def is_straight_flush(sorted_ranks, suits):
    return suits.count(suits[0]) == 5 and all(sorted_ranks[i] == sorted_ranks[i - 1] + 1 for i in range(1, 5))

def is_flush(suits):
    return suits.count(suits[0]) == 5

def is_straight(sorted_ranks):
    return all(sorted_ranks[i] == sorted_ranks[i - 1] + 1 for i in range(1, 5))

def find_poker_hand(hand):
   
    ranks = []
    suits = []

    # Convert cards to ranks and suits
    for card in hand:
        rank, suit = parse_card(card)
        ranks.append(rank)
        suits.append(suit)

    sorted_ranks = sorted(ranks)

    # Check for Royal Flush, Straight Flush, and Flush
    if is_royal_flush(sorted_ranks, suits):
        return 10  # Royal Flush
    elif is_straight_flush(sorted_ranks, suits):
        return 9  # Straight Flush
    elif is_flush(suits):
        return 6  # Flush

    # Check for Straight
    if is_straight(sorted_ranks):
        return 5  # Straight

    hand_unique_vals = list(set(sorted_ranks))

    # Check for Four of a kind and Full House
    if len(hand_unique_vals) == 2:
        for val in hand_unique_vals:
            if sorted_ranks.count(val) == 4:
                return 8  # Four of a Kind
            elif sorted_ranks.count(val) == 3:
                return 7  # Full House

    # Check for Three of a Kind and Two Pair
    if len(hand_unique_vals) == 3:
        for val in hand_unique_vals:    
            if sorted_ranks.count(val) == 3:
                return 4  # Three of a Kind
            elif sorted_ranks.count(val) == 2:
                return 3  # Two Pair

    # Check for Pair
    for i in range(len(sorted_ranks) - 1):
        if sorted_ranks[i] == sorted_ranks[i + 1]:
            return 2  # Pair

    return 1  # High Card

if __name__ == "__main__":
    hands = [
        ["8D", "8H", "8S", "8C", "7H"],    # Four of a Kind (better than Full House)
        ["5H", "5D", "5S", "5C", "7C"],    # Four of a Kind (better than Flush)
        ["AD", "2D", "3D", "4D", "6D"],    # Flush (better than Three of a Kind)
        ["2H", "3S", "4D", "5C", "6H"],    # Straight (better than Pair)
        ["6S", "6H", "7D", "7C", "8D"],    # Two Pair (better than High Card)
    ]

    best_hand = None
    best_rank = -1

    for hand in hands:
        current_rank = find_poker_hand(hand)

        if current_rank > best_rank:
            best_rank = current_rank
            best_hand = hand

        print(f"Hand: {hand}, Result: {POKER_HAND_RANKS[current_rank]}")

    print("Best hand:", best_hand)
    print("Best hand result:", POKER_HAND_RANKS[find_poker_hand(best_hand)])
