"""lie_head: "In this world, every time you lie, your head gets bigger."
41 shots mapped to script word indices and synchronized to voice audio.
"""
from shotkit import *
from rbx import story
from rbx.story import *
import math, random
from mathutils import Vector

V = Video(__file__)
story.bind(V)

BOARD = "chalk_cat.png"
E_DESK = (2.5, 7.0)
E_SEAT = W.seat_pos(E_DESK)


# ------------------------------------------------------------------ cast & props
def carl(t0, t1, expr="angry", loc=(0, 0, 0), rot=0, scale=1.25):
    C = chars.Char("Carl", skin="#e8b894", shirt="#c8382b", pants="#2b2d38", hair="buzz",
                   hair_color="#2b231d", face="villain", sleeves="short", scale=scale)
    C.pose(t0, loc=loc, rot=rot)
    story._live(C, t0, t1, expr)
    return C


def toupee(name="Toupee", loc=(0, 0, 0), rot=(0, 0, 0), parent=None):
    root = empty(name, loc, parent=parent, rot=rot)
    Mt = mat("toupee_brown", hexc("#3a2012"), 0.4)
    sphere(f"{name}_cap", 0.68, (0, 0.05, 0.4), Mt, (1.0, 1.0, 0.35), parent=root)
    return root


def trophy(name="Trophy", loc=(0, 0, 0), scale=1.0):
    root = empty(name, loc)
    Mg = mat("trophy_gold", hexc("#f5c842"), 0.2, metal=0.9)
    box(f"{name}_base", (0.8 * scale, 0.8 * scale, 0.4 * scale), (0, 0, 0.2 * scale), mat("base_wood", hexc("#4a2a18"), 0.5), 0.04, parent=root)
    cyl(f"{name}_stem", 0.15 * scale, 0.8 * scale, (0, 0, 0.8 * scale), Mg, parent=root)
    cyl(f"{name}_cup", 0.5 * scale, 0.9 * scale, (0, 0, 1.5 * scale), Mg, parent=root)
    return root


def dodgeball(name="Dodgeball", loc=(0, 0, 0), scale=0.6):
    Mr = mat("ball_red", hexc("#d92828"), 0.6)
    return sphere(name, scale, loc, Mr, seg=24)


def refrigerator(name="Fridge", loc=(0, 0, 0)):
    root = empty(name, loc)
    Mw = mat("fridge_white", hexc("#e8eaed"), 0.3, metal=0.2)
    box(f"{name}_body", (2.8, 2.4, 6.0), (0, 0, 3.0), Mw, 0.1, parent=root)
    box(f"{name}_handle", (0.1, 0.2, 1.2), (1.45, -1.1, 3.5), mat("handle_chr", hexc("#aaaaaa"), 0.2, metal=0.8), 0.02, parent=root)
    return root


def eddie_big(t0, t1, head_scale=1.0, expr="neutral", loc=(0, 0, 0), rot=0):
    E = eddie(t0, t1, expr=expr, loc=loc, rot=rot)
    E.head.scale = (head_scale, head_scale, head_scale)
    if head_scale > 1.0:
        E.head.location = (0, 0, (head_scale - 1.0) * 0.4)
    return E


# ================================================================== 1. THE HOOK & RULE
@S(1, 0, 10, "HOOK: Firefighters cutting roof with chainsaw, huge Eddie head")
def s01(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=4.5, expr="panic", loc=(E_DESK[0], E_DESK[1], 0), rot=180)
    E.pose(t0, loc=(E_DESK[0], E_DESK[1], 0), rot=180, pose="hands_head")
    cam = Cam()
    cam.push(t0, t1, (E_DESK[0], E_DESK[1], 4.5), 7.0, 5.0, yaw=185, pitch=22, lens=28)
    cam.crash(t0 + 0.1, 28, 38, 0.12)
    cam.handheld(1.5)
    sfx(t0, "whoosh")
    sfx(t0 + 0.3, "alarm")


@S(2, 10, 23, "Chainsaw cutting roof off, massive head stuck")
def s02(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=4.5, expr="scream", loc=(E_DESK[0], E_DESK[1], 0), rot=180)
    box("Chainsaw", (0.4, 2.2, 0.6), (E_DESK[0] + 2.0, E_DESK[1], 7.0), mat("saw_metal", hexc("#f59e0b"), 0.3, metal=0.7), 0.05)
    cam = Cam()
    cam.push(t0, t1, (E_DESK[0], E_DESK[1], 6.0), 5.5, 4.0, yaw=210, pitch=35, lens=24)
    cam.handheld(1.8)
    sfx(t0, "hammer")
    sfx(t0 + 0.4, "gasp")


@S(3, 23, 35, "20 students pushing on giant forehead")
def s03(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=4.8, expr="terror", loc=(E_DESK[0], E_DESK[1], 0), rot=180)
    # students pushing
    for idx, dx in enumerate((-1.5, -0.5, 0.5, 1.5)):
        k = chars.kid(idx, f"Pusher_{idx}")
        k.pose(t0, loc=(E_DESK[0] + dx, E_DESK[1] - 2.5, 0), rot=0, pose="push")
        story._live(k, t0, t1, "determined")
    cam = Cam()
    cam.push(t0, t1, (E_DESK[0], E_DESK[1] - 1.5, 4.0), 6.0, 4.5, yaw=170, pitch=12, lens=26)
    cam.handheld(1.2)
    sfx(t0 + 0.2, "stomp")


@S(4, 35, 52, "RULE: Close-up on Eddie explaining head expands by 10%")
def s04(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.0, expr="talk", loc=(0, 8, 0), rot=180)
    cam = Cam()
    cam.push(t0, t1, (0, 8, 3.8), 2.5, 1.8, yaw=180, pitch=8, lens=32)
    cam.handheld(0.8)
    sfx(t0, "whoosh")
    sfx(w(50), "ding")


@S(5, 52, 63, "Truth shrinks it back down (small pop demo)")
def s05(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    L = leo(t0, t1, expr="smile", loc=(0, 8, 0), rot=180)
    L.head.scale = (1.5, 1.5, 1.5)
    # keyframe shrink
    L.head.keyframe_insert("scale", frame=F(t0))
    L.head.scale = (1.0, 1.0, 1.0)
    L.head.keyframe_insert("scale", frame=F(t0 + 0.4))
    cam = Cam()
    cam.push(t0, t1, (0, 8, 3.8), 2.4, 1.9, yaw=190, pitch=6, lens=30)
    cam.handheld(0.8)
    sfx(t0 + 0.3, "pop")


@S(6, 63, 71, "Nobody lies on homework: diligent classroom")
def s06(t0, t1):
    R, ks = class_scene(t0, t1, kids=6, board=BOARD)
    cam = Cam()
    cam.push(t0, t1, (5.0, 8.0, 3.5), 8.0, 6.5, yaw=45, pitch=20, lens=24)
    cam.handheld(0.7)
    sfx(t0, "paper")


@S(7, 71, 86, "Kids confessing secrets at school entrance to fit through door")
def s07(t0, t1):
    W.hallway_day()
    W.sun(3.0)
    k = chars.kid(1, "Confessor")
    k.pose(t0, loc=(0, 5, 0), rot=180, pose="talk")
    story._live(k, t0, t1, "worried")
    k.head.scale = (1.6, 1.6, 1.6)
    k.head.keyframe_insert("scale", frame=F(t0))
    k.head.scale = (1.0, 1.0, 1.0)
    k.head.keyframe_insert("scale", frame=F(t1 - 0.3))
    cam = Cam()
    cam.push(t0, t1, (0, 5, 3.5), 4.0, 2.8, yaw=180, pitch=10, lens=28)
    cam.handheld(1.0)
    sfx(t0, "door")
    sfx(t1 - 0.4, "pop")


@S(8, 86, 105, "Dad's head wedged in the refrigerator for two days")
def s08(t0, t1):
    W.sky()
    W.sun(4.0)
    box("KitchenFloor", (16, 16, 0.4), (0, 0, -0.2), mat("tile_fl", hexc("#d4d8de"), 0.3))
    refrigerator("Fridge", (0, 0, 0))
    dad = chars.Char("Dad", skin="#e4b088", shirt="#2e5b88", pants="#252528", hair="short", hair_color="#555555", face="scared")
    dad.pose(t0, loc=(0, -1.8, 0), rot=0, pose="hands_head")
    dad.head.scale = (2.2, 2.2, 2.2)
    dad.head.location = (0, 0, 1.2)
    story._live(dad, t0, t1, "panic")
    cam = Cam()
    cam.push(t0, t1, (0, 0, 3.5), 6.5, 4.8, yaw=215, pitch=18, lens=26)
    cam.handheld(1.2)
    sfx(t0, "thud")
    sfx(t0 + 0.5, "buzzer")


# ================================================================== 2. THE INCIDENT (TROPHY)
@S(9, 105, 118, "Eddie intro: most honest kid in town")
def s09(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.0, expr="smile", loc=(0, 10, 0), rot=180)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 3.8), 3.0, 2.2, yaw=180, pitch=6, lens=30)
    cam.handheld(0.8)
    sfx(t0, "sparkle")


@S(10, 118, 133, "Dodgeball smashes golden trophy with a loud crash!")
def s10(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    box("Pedestal", (1.2, 1.2, 3.0), (0, 15, 1.5), mat("ped_marble", hexc("#e8e6e1"), 0.2), 0.05)
    tr = trophy("GoldenTrophy", (0, 15, 3.0), scale=1.2)
    db = dodgeball("Ball", (0, 8, 4.0), scale=0.7)
    db.keyframe_insert("location", frame=F(t0))
    db.location = (0, 15, 3.8)
    db.keyframe_insert("location", frame=F(t0 + 0.3))
    # trophy falls
    tr.keyframe_insert("location", frame=F(t0 + 0.3))
    tr.location = (0.5, 16, 0.5)
    tr.rotation_euler = (math.radians(90), 0, math.radians(45))
    tr.keyframe_insert("location", frame=F(t1))
    tr.keyframe_insert("rotation_euler", frame=F(t1))
    cam = Cam()
    cam.push(t0, t1, (0, 15, 3.5), 5.0, 3.2, yaw=160, pitch=15, lens=28)
    cam.crash(t0 + 0.25, 28, 40, 0.1)
    cam.handheld(1.4)
    sfx(t0, "whoosh")
    sfx(t0 + 0.3, "splat")
    sfx(t0 + 0.4, "boom")


@S(11, 133, 143, "Principal Carl storms in: Who smashed the trophy?!")
def s11(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    C = carl(t0, t1, expr="furious", loc=(0, 22, 0), rot=180)
    C.pose(t0, loc=(0, 22, 0), rot=180, pose="point")
    cam = Cam()
    cam.push(t0, t1, (0, 22, 4.2), 4.5, 3.0, yaw=180, pitch=8, lens=30)
    cam.crash(t0 + 0.1, 30, 42, 0.12)
    cam.handheld(1.5)
    sfx(t0, "stomp")
    sfx(t0 + 0.2, "glitch")


@S(12, 143, 152, "Panic: Eddie blurts out 'A raccoon did it!'")
def s12(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.0, expr="panic", loc=(0, 10, 0), rot=0)
    E.pose(t0, loc=(0, 10, 0), rot=0, pose="hands_face")
    cam = Cam()
    cam.push(t0, t1, (0, 10, 3.8), 2.2, 1.5, yaw=0, pitch=6, lens=32)
    cam.handheld(1.8)
    sfx(t0, "gasp")


# ================================================================== 3. THE ESCALATION
@S(13, 152, 163, "POOF! Head swells to giant pumpkin size!")
def s13(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.8, expr="shock", loc=(0, 10, 0), rot=0)
    E.head.scale = (1.0, 1.0, 1.0)
    E.head.keyframe_insert("scale", frame=F(t0))
    E.head.scale = (1.8, 1.8, 1.8)
    E.head.location = (0, 0, 0.4)
    E.head.keyframe_insert("scale", frame=F(t0 + 0.25))
    E.head.keyframe_insert("location", frame=F(t0 + 0.25))
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.2), 3.8, 2.5, yaw=15, pitch=10, lens=28)
    cam.crash(t0 + 0.2, 28, 38, 0.1)
    cam.handheld(1.5)
    sfx(t0 + 0.15, "poof")
    sfx(t0 + 0.2, "boing")


@S(14, 163, 172, "Carl narrows eyes: A raccoon in the cafeteria?!")
def s14(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    C = carl(t0, t1, expr="angry", loc=(0, 16, 0), rot=180)
    C.pose(t0, loc=(0, 16, 0), rot=180, pose="cross")
    cam = Cam()
    cam.push(t0, t1, (0, 16, 4.2), 3.5, 2.4, yaw=185, pitch=8, lens=30)
    cam.handheld(1.0)
    sfx(t0, "whoosh")


@S(15, 172, 180, "Eddie doubles down: Yes, and wearing a tiny cape!")
def s15(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.8, expr="talk", loc=(0, 10, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.2), 2.8, 2.0, yaw=0, pitch=6, lens=30)
    cam.handheld(1.2)
    sfx(t0, "click")


@S(16, 180, 194, "BOOM! Head swells to golf cart size!")
def s16(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=3.0, expr="terror", loc=(0, 10, 0), rot=0)
    E.head.scale = (1.8, 1.8, 1.8)
    E.head.keyframe_insert("scale", frame=F(t0))
    E.head.scale = (3.0, 3.0, 3.0)
    E.head.location = (0, 0, 0.8)
    E.head.keyframe_insert("scale", frame=F(t0 + 0.3))
    E.head.keyframe_insert("location", frame=F(t0 + 0.3))
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.5), 5.0, 3.5, yaw=10, pitch=12, lens=26)
    cam.crash(t0 + 0.25, 26, 36, 0.12)
    cam.handheld(1.6)
    sfx(t0 + 0.2, "boom")
    sfx(t0 + 0.3, "boing")


@S(17, 194, 203, "Neck wobbling, balance completely gone")
def s17(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=3.0, expr="panic", loc=(0, 10, 0), rot=0)
    E.pose(t0, loc=(0, 10, 0), rot=15, pose="recoil")
    E.root.keyframe_insert("rotation_euler", frame=F(t0))
    E.root.rotation_euler = (0, math.radians(15), 0)
    E.root.keyframe_insert("rotation_euler", frame=F(t1))
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.5), 4.5, 3.2, yaw=20, pitch=10, lens=28)
    cam.handheld(1.8)
    sfx(t0, "thud")


@S(18, 203, 211, "Carl shouts: Eddie, are you lying to me?!")
def s18(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    C = carl(t0, t1, expr="furious", loc=(0, 15, 0), rot=180)
    C.pose(t0, loc=(0, 15, 0), rot=180, pose="shout")
    cam = Cam()
    cam.push(t0, t1, (0, 15, 4.2), 3.2, 2.2, yaw=180, pitch=8, lens=32)
    cam.handheld(1.2)
    sfx(t0, "whoosh")


@S(19, 211, 220, "Honesty is my middle name!")
def s19(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=3.0, expr="scream", loc=(0, 10, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.5), 3.0, 2.0, yaw=0, pitch=6, lens=30)
    cam.handheld(1.5)
    sfx(t0, "gasp")


@S(20, 220, 230, "BAM! Head explodes to minivan size!")
def s20(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=5.0, expr="panic", loc=(0, 10, 0), rot=0)
    E.head.scale = (3.0, 3.0, 3.0)
    E.head.keyframe_insert("scale", frame=F(t0))
    E.head.scale = (5.0, 5.0, 5.0)
    E.head.location = (0, 0, 1.4)
    E.head.keyframe_insert("scale", frame=F(t0 + 0.3))
    E.head.keyframe_insert("location", frame=F(t0 + 0.3))
    cam = Cam()
    cam.push(t0, t1, (0, 10, 5.5), 8.0, 5.5, yaw=25, pitch=18, lens=24)
    cam.crash(t0 + 0.25, 24, 34, 0.12)
    cam.handheld(2.0)
    sfx(t0 + 0.2, "boom")
    sfx(t0 + 0.3, "splat")


@S(21, 230, 235, "Wedged tight between the lockers!")
def s21(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=5.0, expr="terror", loc=(0, 10, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 5.0), 6.5, 4.8, yaw=90, pitch=10, lens=26)
    cam.handheld(1.5)
    sfx(t0, "hammer")


@S(22, 235, 244, "Kids screaming, lockers crumpling!")
def s22(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    for idx, (x, y) in enumerate([(-2.5, 4), (2.5, 4), (-2.5, 16), (2.5, 16)]):
        k = chars.kid(idx, f"Screamer_{idx}")
        k.pose(t0, loc=(x, y, 0), rot=180 if y > 10 else 0, pose="shock")
        story._live(k, t0, t1, "scream")
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.0), 7.0, 5.0, yaw=180, pitch=20, lens=24)
    cam.handheld(1.8)
    sfx(t0, "gasp")
    sfx(t0 + 0.3, "glitch")


@S(23, 244, 260, "Carl backs away in horror: Call SWAT team!")
def s23(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    C = carl(t0, t1, expr="terror", loc=(0, 18, 0), rot=180)
    C.pose(t0, loc=(0, 18, 0), rot=180, pose="phone")
    cam = Cam()
    cam.push(t0, t1, (0, 18, 4.2), 4.0, 2.5, yaw=175, pitch=12, lens=28)
    cam.handheld(1.5)
    sfx(t0, "alarm")
    sfx(t0 + 0.4, "teleport")


@S(24, 260, 273, "Ceiling cracking, concrete dust falling")
def s24(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=5.0, expr="panic", loc=(0, 10, 0), rot=0)
    # falling dust
    for i in range(5):
        sphere(f"Dust_{i}", 0.25, (random.uniform(-1, 1), 10 + random.uniform(-1, 1), 7.0 - i * 0.8), mat("dust", hexc("#d0ccc4"), 0.9), seg=12)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 6.0), 5.5, 3.8, yaw=10, pitch=35, lens=24)
    cam.handheld(1.8)
    sfx(t0, "thud")
    sfx(t0 + 0.4, "splat")


@S(25, 273, 287, "If I lied one more time, building collapses!")
def s25(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=5.0, expr="terror", loc=(0, 10, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 5.0), 4.2, 3.0, yaw=0, pitch=6, lens=28)
    cam.crash(t0 + 0.1, 28, 38, 0.12)
    cam.handheld(2.0)
    sfx(t0, "wind")


# ================================================================== 4. THE TURN & CONFESSIONS
@S(26, 287, 298, "THEN I NOTICED: Carl's toupee slipping sideways!")
def s26(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    C = carl(t0, t1, expr="shock", loc=(0, 16, 0), rot=180)
    tp = toupee("Wig", (0, 16, 5.2), rot=(0, 25, 0))
    cam = Cam()
    cam.push(t0, t1, (0, 16, 5.2), 3.0, 1.8, yaw=180, pitch=15, lens=35)
    cam.crash(t0 + 0.15, 35, 50, 0.1)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "ding")
    sfx(t0 + 0.3, "sparkle")


@S(27, 298, 304, "Truth! The rule works both ways!")
def s27(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=5.0, expr="determined", loc=(0, 10, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 5.0), 3.5, 2.2, yaw=0, pitch=8, lens=30)
    cam.handheld(1.2)
    sfx(t0, "coin")


@S(28, 304, 317, "Eddie takes deep breath and screams at top of lungs")
def s28(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=5.0, expr="shout", loc=(0, 10, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 5.0), 3.2, 2.0, yaw=5, pitch=6, lens=32)
    cam.handheld(1.6)
    sfx(t0, "whoosh")


@S(29, 317, 322, "CONFESSION 1: I DON'T ACTUALLY LIKE BROCCOLI!")
def s29(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=5.0, expr="scream", loc=(0, 10, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 5.0), 2.8, 1.8, yaw=0, pitch=6, lens=34)
    cam.crash(t0 + 0.05, 34, 44, 0.1)
    cam.handheld(1.8)
    sfx(t0, "crowd")


@S(30, 322, 328, "POP! Head shrinks 10% (down to 4.5x)!")
def s30(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=4.2, expr="shock", loc=(0, 10, 0), rot=0)
    E.head.scale = (5.0, 5.0, 5.0)
    E.head.keyframe_insert("scale", frame=F(t0))
    E.head.scale = (4.2, 4.2, 4.2)
    E.head.location = (0, 0, 1.1)
    E.head.keyframe_insert("scale", frame=F(t0 + 0.2))
    E.head.keyframe_insert("location", frame=F(t0 + 0.2))
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.8), 5.5, 4.0, yaw=15, pitch=12, lens=28)
    cam.handheld(1.4)
    sfx(t0 + 0.1, "pop")
    sfx(t0 + 0.3, "cheer")


@S(31, 328, 336, "CONFESSION 2: I COPIED LEO'S MATH HOMEWORK!")
def s31(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    L = leo(t0, t1, expr="shock", loc=(2.5, 8, 0), rot=160)
    cam = Cam()
    cam.push(t0, t1, (2.5, 8, 3.8), 2.8, 1.8, yaw=160, pitch=8, lens=30)
    cam.crash(t0 + 0.1, 30, 42, 0.1)
    cam.handheld(1.4)
    sfx(t0, "rimshot")


@S(32, 336, 342, "POP! Down to beach ball size (2.2x)!")
def s32(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=2.2, expr="grin", loc=(0, 10, 0), rot=0)
    E.head.scale = (4.2, 4.2, 4.2)
    E.head.keyframe_insert("scale", frame=F(t0))
    E.head.scale = (2.2, 2.2, 2.2)
    E.head.location = (0, 0, 0.5)
    E.head.keyframe_insert("scale", frame=F(t0 + 0.2))
    E.head.keyframe_insert("location", frame=F(t0 + 0.2))
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.2), 4.5, 3.2, yaw=10, pitch=10, lens=28)
    cam.handheld(1.2)
    sfx(t0 + 0.1, "pop")


@S(33, 342, 352, "CLIMAX TRUTH: CARL'S HAIR IS A CHEAP FAKE WIG!")
def s33(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    C = carl(t0, t1, expr="furious", loc=(0, 16, 0), rot=180)
    tp = toupee("FlyingWig", (0, 16, 5.2), rot=(0, 25, 0))
    tp.keyframe_insert("location", frame=F(t0))
    tp.location = (0, 14, 8.5)
    tp.rotation_euler = (math.radians(180), math.radians(45), 0)
    tp.keyframe_insert("location", frame=F(t1))
    tp.keyframe_insert("rotation_euler", frame=F(t1))
    cam = Cam()
    cam.push(t0, t1, (0, 16, 4.5), 4.5, 3.0, yaw=180, pitch=15, lens=28)
    cam.crash(t0 + 0.1, 28, 40, 0.12)
    cam.handheld(1.8)
    sfx(t0 + 0.1, "whoosh")
    sfx(t0 + 0.3, "gasp")


@S(34, 352, 355, "Pop! Pop! Pop! Rapid shrinking!")
def s34(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.3, expr="joy", loc=(0, 10, 0), rot=0)
    E.head.scale = (2.2, 2.2, 2.2)
    E.head.keyframe_insert("scale", frame=F(t0))
    E.head.scale = (1.1, 1.1, 1.1)
    E.head.location = (0, 0, 0.05)
    E.head.keyframe_insert("scale", frame=F(t1))
    E.head.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.0), 3.5, 2.4, yaw=5, pitch=8, lens=30)
    cam.handheld(1.4)
    sfx(t0, "pop")
    sfx(t0 + 0.12, "pop")
    sfx(t0 + 0.24, "pop")


@S(35, 355, 363, "Head zipped right back to normal size!")
def s35(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.0, expr="happy", loc=(0, 10, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 10, 3.8), 2.8, 1.8, yaw=0, pitch=6, lens=32)
    cam.handheld(1.0)
    sfx(t0, "sparkle")


@S(36, 363, 370, "Eddie squeezes loose and hits the floor!")
def s36(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.0, expr="smile", loc=(0, 10, 0), rot=0)
    E.pose(t0, loc=(0, 10, 0), rot=0, pose="jump")
    cam = Cam()
    cam.push(t0, t1, (0, 10, 2.5), 4.0, 2.8, yaw=45, pitch=15, lens=28)
    cam.handheld(1.2)
    sfx(t0 + 0.2, "thud")


# ================================================================== 5. PAYOFF & BUTTON
@S(37, 370, 376, "Cafeteria erupts into cheers!")
def s37(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    for idx, (x, y) in enumerate([(-2, 6), (2, 6), (-2, 14), (2, 14)]):
        k = chars.kid(idx, f"Cheerer_{idx}")
        k.pose(t0, loc=(x, y, 0), rot=180 if y > 10 else 0, pose="cheer")
        story._live(k, t0, t1, "joy")
    cam = Cam()
    cam.push(t0, t1, (0, 10, 4.0), 6.5, 4.8, yaw=180, pitch=18, lens=24)
    cam.handheld(1.5)
    sfx(t0, "cheer")
    sfx(t0 + 0.2, "confetti")


@S(38, 376, 388, "Carl bright red, hands over bald head in humiliation")
def s38(t0, t1):
    W.hallway_day()
    W.sun(4.0)
    C = carl(t0, t1, expr="furious", loc=(0, 16, 0), rot=180)
    C.pose(t0, loc=(0, 16, 0), rot=180, pose="hands_head")
    cam = Cam()
    cam.push(t0, t1, (0, 16, 4.2), 3.5, 2.2, yaw=185, pitch=10, lens=30)
    cam.handheld(1.0)
    sfx(t0, "buzzer")


@S(39, 388, 398, "Eddie struts out of school like an absolute champion")
def s39(t0, t1):
    W.town()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.0, expr="smug", loc=(0, -25, 0), rot=180)
    E.walk(t0, t1, (0, -20, 0), (0, -32, 0))
    cam = Cam()
    cam.push(t0, t1, (0, -28, 3.5), 5.0, 3.5, yaw=170, pitch=8, lens=28)
    cam.handheld(0.8)
    sfx(t0, "whoosh")


@S(40, 398, 412, "Mom calls phone: Did you eat the last chocolate cupcake?")
def s40(t0, t1):
    W.town()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=1.0, expr="talk", loc=(0, -30, 0), rot=180)
    E.pose(t0, loc=(0, -30, 0), rot=180, pose="phone")
    cam = Cam()
    cam.push(t0, t1, (0, -30, 3.8), 2.5, 1.8, yaw=180, pitch=6, lens=32)
    cam.handheld(1.0)
    sfx(t0, "ding")


@S(41, 412, None, "BUTTON: 'No Mom.' -> BOING! Head balloons straight into camera!")
def s41(t0, t1):
    W.town()
    W.sun(4.0)
    E = eddie_big(t0, t1, head_scale=2.5, expr="panic", loc=(0, -30, 0), rot=180)
    E.head.scale = (1.0, 1.0, 1.0)
    E.head.keyframe_insert("scale", frame=F(t0))
    E.head.scale = (3.5, 3.5, 3.5)
    E.head.location = (0, 0, 0.8)
    E.head.keyframe_insert("scale", frame=F(t1 - 0.2))
    E.head.keyframe_insert("location", frame=F(t1 - 0.2))
    cam = Cam()
    cam.push(t0, t1, (0, -30, 4.0), 3.0, 1.5, yaw=180, pitch=6, lens=30)
    cam.crash(t1 - 0.4, 30, 45, 0.15)
    cam.handheld(2.0)
    sfx(t1 - 0.5, "boing")
