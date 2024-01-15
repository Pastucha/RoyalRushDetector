def convert_rank(rank):
    rank_conversion = {"A": 14, "K": 13, "Q": 12, "J": 11}
    return rank_conversion.get(rank, int(rank) if rank.isdigit() else None)

def parse_card(card):
    if len(card) == 2:
        rank, suit = card[0], card[1]
    else:
        rank, suit = card[0:2], card[2]
    return convert_rank(rank), suit

def find_poker_hand(hand):
    poker_hand_ranks = {
        10: "Royal Flush",
        9: "Straight Flush",
        8: "Four of a Kind",
        7: "Full House",
        6: "Flush",
        5: "Straight",
        4: "Three of a Kind",
        3: "Two Pair",
        2: "Pair",
        1: "High Card",
        0: "not coded"
    }

    ranks = []
    suits = []
    possible_ranks = []

    # Convert cards to ranks and suits
    for card in hand:
        rank, suit = parse_card(card)
        ranks.append(rank)
        suits.append(suit)

    sorted_ranks = sorted(ranks)

    # Check for Royal Flush, Straight Flush, and Flush
    if suits.count(suits[0]) == 5:
        if all(rank in sorted_ranks for rank in [10, 11, 12, 13, 14]):
            possible_ranks.append(10)  # Royal Flush
        elif all(sorted_ranks[i] == sorted_ranks[i - 1] + 1 for i in range(1, len(sorted_ranks))):
            possible_ranks.append(9)  # Straight Flush
        else:
            possible_ranks.append(6)  # Flush

    # Check for Straight
    if all(sorted_ranks[i] == sorted_ranks[i - 1] + 1 for i in range(1, len(sorted_ranks))):
        possible_ranks.append(5)  # Straight

    hand_unique_vals = list(set(sorted_ranks))
    
    # Check for Four of a kind and Full House
    if len(hand_unique_vals) == 2:
        for val in hand_unique_vals:
            if sorted_ranks.count(val) == 4:
                possible_ranks.append(8)  # Four of a Kind
            elif sorted_ranks.count(val) == 3:
                possible_ranks.append(7)  # Full House

    # Check for Three of a Kind and Two Pair
    if len(hand_unique_vals) == 3:
        for val in hand_unique_vals:
            if sorted_ranks.count(val) == 3:
                possible_ranks.append(4)  # Three of a Kind
            elif sorted_ranks.count(val) == 2:
                possible_ranks.append(3)  # Two Pair

    if not possible_ranks:
        possible_ranks.append(1)  # High Card

    output = poker_hand_ranks[max(possible_ranks)]
    return output

if __name__ == "__main__":
    hands = [
        ["AH", "KH", "QH", "JH", "10H"],  # Royal Flush
        ["QC", "JC", "10C", "9C", "8C"],  # Straight Flush
        ["5C", "5S", "5H", "5D", "QH"],  # Four of a Kind
        ["2H", "2D", "2S", "10H", "10C"],  # Full House
        ["2D", "KD", "7D", "6D", "5D"],  # Flush
        ["JC", "10H", "9C", "8C", "7D"],  # Straight
        ["10H", "10C", "10D", "2D", "5S"],  # Three of a Kind
        ["KD", "KH", "5C", "5S", "6D"],  # Two Pair
        ["2D", "2S", "9C", "KD", "10C"],  # Pair
        ["KD", "5H", "2D", "10C", "JH"]  # High Card
    ]

    for hand in hands:
        result = find_poker_hand(hand)
        print(hand, result)
