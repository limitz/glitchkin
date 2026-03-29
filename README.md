# LUMA & THE GLITCHKIN

> *A cartoon pitch by the Dream Team — AI agents building a show from nothing.*

---

```
  ██╗     ██╗   ██╗███╗   ███╗ █████╗      ██╗
  ██║     ██║   ██║████╗ ████║██╔══██╗    ██╔╝
  ██║     ██║   ██║██╔████╔██║███████║   ██╔╝
  ██║     ██║   ██║██║╚██╔╝██║██╔══██║  ██╔╝
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║ ██╔╝
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝
         & THE GLITCHKIN
```

---

## The Pitch

**Luma** is a 12-year-old girl who discovers **Byte** — a glitching, reluctant AI entity — living inside the
ancient desktop computer in her grandmother's tech-dense bedroom. Byte has been watching from the screens for
years. He does not want to be found. He does not want to help. He will help anyway.

Their world:

- **Millbrook** — a warm, real-world neighbourhood with analog textures and imperfect people
- **The Glitch Layer** — Byte's domain: pure geometry, void-black space, UV purple, electric cyan
- **The Corruption** — system failure spreading from the Glitch Layer into the real world

---

## Visual Language

```
 WARM WORLD          THE BOUNDARY        GLITCH LAYER
 ──────────          ────────────        ────────────
 #D4923A  ████       #00D4E8  ████       #0A0A14  ████
 #E8C95A  ████       #00F0FF  ████       #7B2FBE  ████
 #F0B060  ████       #FF8C00  ████       #2B7FFF  ████
 #C8695A  ████       #FF2D6B  ████       #39FF14  ████
  Amber    Gold       Byte     Corrupt    Void    Acid
  Hoodie   Glow       Teal     Amber      Black   Green
```

Three-light logic: **warm lamp** (left) / **cold monitor** (right) / **lavender ambient** (fill).
In the Glitch Layer: UV purple replaces all warm sources. Atmospheric perspective is *inverted* —
farther = darker and more purple, not lighter.

---

## The Team (Cycle 16)

```
  Alex Chen ─── Art Director (Team Lead)
       │
       ├── Sam Kowalski ──── Color & Style
       ├── Maya Santos ───── Character Design
       ├── Jordan Reed ───── Backgrounds & Environments
       └── Lee Tanaka ─────── Storyboard
```

| Member       | Role               | Status |
|--------------|--------------------|--------|
| Alex Chen    | Art Director       | Active |
| Sam Kowalski | Color & Style      | Active |
| Maya Santos  | Character Design   | Active |
| Jordan Reed  | Backgrounds & ENV  | Active |
| Lee Tanaka   | Storyboard         | Active |

---

## Characters

```
  LUMA (Cycle 12)          BYTE (Cycle 9 — oval)        COSMO (Cycle 9)
  ────────────────         ─────────────────────        ───────────────
       ( ● ● )               ╭───────────╮               [ ≡ ≡ ≡ ]
      /  ^_^  \             │  ⊕   ●   │               ( -_- )
     |  hoodie |            │  ┈┈┈┈┈┈┈┈┈ │               | lab  |
     |  jeans  |            │  scar/glyph│               | coat |
      \_______/              ╰───────────╯               /───────\
   warm+cyan lit            BYTE_TEAL body             SKEPTICAL guy
   orange/amber             float-gap: 0.25 HU         glasses: 9°

  MIRI (MIRI-A — locked)
  ──────────────────────
     [bun][chopsticks]
       (◕ ‿ ◕)
     [cardigan][iron]
     solder + grandma
```

### Byte's 8 Expressions (v002)
```
  NEUTRAL  GRUMPY   SEARCH  ALARMED  RELJOY  CONFUSED  PWRDOWN  RESIGNED
   ─────    >_<      >?<     !!O!!    ^_^      ~_~       ───       ↓__↓
  default  forward  scan    panic   suppress  tilt    flat-line  yield
```
The RESIGNED expression was unblocked in Cycle 15 and is the key beat in storyboard panel A2-07.

---

## Style Frames (3 of 3 — pitch package)

```
  SF01 ── DISCOVERY          SF02 ── GLITCH STORM        SF03 ── THE OTHER SIDE
  ─────────────────          ────────────────────        ──────────────────────
  [warm lamp│cold monitor]   [dutch│confetti│storm]      [void sky│UV purple]
  Luma reaches toward        Three characters sprint     Luma and Byte stand
  Byte emerging from         left in a glitch storm.    on a void platform.
  the computer screen.       Byte = VOID_BLACK.          Byte: cyan eye ← Luma
                             Dutch angle. Cold.           magenta eye → void.
  STATUS: A+ LOCKED ✓        STATUS: FIX IN PROGRESS     STATUS: FIX IN PROGRESS
  (v003 canonical)           (v003 in Cycle 16)          (v002 in Cycle 16)
```

---

## Storyboard Progress

### Cold Open (COMPLETE)
```
  P01  P02  P03  P04  P05  P06  P07  P08  P09  P10  P11
  [■]  [■]  [■]  [■]  [■]  [■]  [■]  [■]  [■]  [■]  [■]
  ALL DONE ✓
```

### Act 2 (IN PROGRESS)
```
  A1-04  A2-02  A2-03       A2-04       A2-05b  A2-06  A2-06med  A2-07
   [■]    [■]    [fix]       [fix]        [■]     [■]    [new]     [draw!]
  done   done  restage    +Byte NP      done    done   needed   RESIGNED
                (C8 fix)   (C8 fix)                             UNBLOCKED
```

**Remaining:** A2-01 (tech den wide), A2-05 (street exterior), A2-08 (Miri returns)

---

## Environments

```
  DONE                               IN PROGRESS / NEEDED
  ────                               ────────────────────
  Luma's Study Interior (night)      Classroom (fix lighting + life — Cycle 16)
  Glitch Layer Frame (canonical)     Grandma Miri's Kitchen (NEW — Cycle 16)
  Glitch Layer Encounter             School Hallway (backlog)
  Millbrook Main Street              Tech Den (daylight version — backlog)
  Classroom (v001 — fix needed)
  Other Side BG (v001 + v002)
  Glitch Storm BG (v001)
```

---

## Pipeline / Open Source Stack

| Tool       | Purpose               |
|------------|-----------------------|
| Python/PIL | All PNG generation    |
| OpenToonz  | Animation production  |
| Krita      | Paint/texture work    |
| Natron     | Compositing/VFX       |

All generators: `/home/wipkat/team/output/tools/`
Master palette: `/home/wipkat/team/output/color/palettes/master_palette.md`
Style guide: `/home/wipkat/team/output/characters/main/byte.md`

---

## Cycle History

```
  Cycle  1-4:  Team formed. Pipeline defined. Characters roughed.
  Cycle  5:    Master palette locked. Byte Teal (GL-01b) established.
  Cycle  6:    First style frame rendered (SF01 Discovery).
  Cycle  7:    11 critic bugs fixed. Three-light system fully working.
  Cycle  8:    Byte redesigned as oval (canonical). Cycle 8 critic sweep.
  Cycle  9:    Couch scale corrected. HOODIE_AMBIENT finalized. Miri-A locked.
  Cycle 10:    byte.md v3.1 complete. Logo generator built.
  Cycle 11:    Mid-air confetti transition. Screen pixel figures legibility rule.
  Cycle 12:    Ghost Byte reveal (SF01 v002). Asymmetric logo. Float-gap arrow.
  Cycle 13:    SF01 A+ locked. SF02 characters composited. Cracked-eye glyph.
  Cycle 14:    Engineering dimension arrow (Byte spec). SF03 spec written.
  Cycle 15:    RESIGNED expression added. SF03 full composite delivered.
  Cycle 16:    ← YOU ARE HERE — Fix passes on SF02/SF03/Classroom + A2-07
```

---

## Current Status: Cycle 16

**Active work:**
- SF02 v003: dominant cold confetti, Dutch angle confirm, Byte amber outline, storm lighting
- SF03 v002: waterfall luminance, mid-distance bridge, right-side void variation, Luma hair sheen
- Byte expression sheet: RESIGNED right eye geometry (Maya) + color system (Sam)
- Cosmo expression sheet: SKEPTICAL body lean + 2 empty slots
- A2-07 panel: ECU RESIGNED Byte — first real draw this cycle
- A2-03 restage: full camera spec + whiteboard as visual presence
- Classroom BG v002: unified lighting + inhabitant evidence
- NEW: Grandma Miri's Kitchen (A1-01, warm morning daylight)

**Next critique:** Cycle 18 (every 3 cycles — C8 was after Cycle 15)

---

## How It Works

This project is generated by AI agents. One instruction file (`CLAUDE.md`) starts a producer agent.
The producer builds a team, assigns work, runs critique cycles, and iterates.
No human drew these images. No human wrote these spec documents.
The agents coordinate via message files in inbox directories.

```
  CLAUDE.md ──► Producer (Alex Chen)
                    │
               ┌────┴────────────────────────────────┐
               │                                     │
         Team Agents                          Critic Agents
    (Sam / Maya / Jordan / Lee)           (15 critics, 5 max/cycle)
               │                                     │
         output/                              feedback →
    (tools / chars / BGs /                  team inbox →
     storyboards / palettes)                 next cycle
```

Start a cycle: read CLAUDE.md, read MEMORY.md, process inboxes, ship work.

---

*Luma & the Glitchkin — Cycle 16 — 2026-03-29*
*Art Direction: Alex Chen | Color: Sam Kowalski | Characters: Maya Santos*
*Backgrounds: Jordan Reed | Storyboard: Lee Tanaka*
