"""Canonical underworld reputation, distinct from a mutable player's standing."""
SCORES = {'sylvanis': 100, 'crow': 100, 'ivan': 98, 'garrett': 95}
DIRECTION = ('Sylvanis, the Crazed Demon / Coloured Joker, has the highest feared reputation in this setting: '
    'the most dangerous man on Earth. His reputation is 100/100; the Crow ranks next in underworld fear '
    'and authority, also 100/100. The shared numeric ceiling does not make their feared reputations equal. '
    'Ivan is 98/100, Garrett 95/100. Criminal characters speak of Sylvanis with intense, credible fear: '
    'guarded words, reluctance to provoke him, and serious warnings instead of casual mockery or bravado. '
    'Keep individual voices; do not repeat a fear speech in unrelated conversations, force the player to feel '
    'afraid, or invent an atrocity to prove his danger. The Crow inspires the next greatest dread. '
    'Reputation does not reveal the Crow’s identity, Ace identities, headquarters locations or private deeds. '
    'Ivan belongs to the Syndicate as its Black and White Joker AND leads the Black and White Joker network. '
    'These are concurrent affiliations, not rival alternatives.')


def context(s, who):
    import bubblegram_progression as progression
    import gang_leaders
    import gang_members
    if who in gang_members.MEMBERS:
        return DIRECTION
    if who in progression.ESTABLISHED or who in gang_leaders.BY_NAME or who in ('Keisuke Hachimura','rei','thirteen'):
        return DIRECTION
    return ''
