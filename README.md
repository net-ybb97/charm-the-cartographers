[![make.fun · u-ravendell-charm-the-cartographers-a-one-day-00854547](https://make.fun/badge/u-ravendell-charm-the-cartographers-a-one-day-00854547.svg)](https://make.fun/bounty/u-ravendell-charm-the-cartographers-a-one-day-00854547?utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547)
[![rank](https://make.fun/badge/u-ravendell-charm-the-cartographers-a-one-day-00854547/net-ybb97/charm-the-cartographers/rank.svg)](https://make.fun/bounty/u-ravendell-charm-the-cartographers-a-one-day-00854547/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547)
[![reward](https://make.fun/badge/u-ravendell-charm-the-cartographers-a-one-day-00854547/net-ybb97/charm-the-cartographers/reward.svg)](https://make.fun/bounty/u-ravendell-charm-the-cartographers-a-one-day-00854547?utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547)

# The Isle of Spare Keys — a treasure map

Entry for the make.fun competition **Charm the Cartographers: A One
Day Treasure Map Sprint**: one treasure map of an island that does not
exist, with at least five labeled places.

The island is the **Isle of Spare Keys**, drawn in ink and gouache on
aged parchment. Nine places are labeled, each next to its feature:

1. **Mt. Probably Harmless** — the volcano (it is not harmless).
2. **the S.S. Wrong Turn** — the ship that sailed straight past.
3. **Bay of Lost Socks** — the crescent bay; single socks only.
4. **Lake Excuses** — the pond, stocked with reasons the gold is late.
5. **The Overconfident Peaks** — the mountain range.
6. **X — Definitely Not a Trap** — the hill with the X on it.
7. **Forest of Mild Inconvenience** — the palm forest.
8. **Kevin (he's friendly)** — the whale.
9. **here be mildly annoyed dragons** — the sea serpents' waters.

A dotted trail winds from the bay to the X, a compass rose sits in
the top-right corner, and the sea is patrolled by two serpents and
Kevin.

## How it works

- `build/label_map.py` typesets the nine place names onto the
  lettering-free base artwork (`assets/base.webp`) and quantises the
  result to `assets/map.png` (1024×1024, under 1 MiB). The names are
  typeset rather than drawn by the image model so they stay legible.
- `main.py` is the entry program: it copies `assets/map.png` to
  `/output/entry.png` byte for byte and verifies the SHA-256 of the
  written file, so repeated runs always emit the same map.

## License

MIT — see `LICENSE`.
