"""hiccup_shrink: "In this world, every time you hiccup, you shrink."
65 shots mapped to script word indices and synchronized to voice audio.
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


def lunch_lady(t0, t1, expr="neutral", loc=(0, 0, 0), rot=0):
    L = chars.Char("LunchLady", skin="#f0d5be", shirt="#f4f4f4", pants="#4a5060", hair="bun",
                   hair_color="#a8a8a8", face="plain", sleeves="short", extras=("glasses",))
    L.pose(t0, loc=loc, rot=rot)
    story._live(L, t0, t1, expr)
    return L


def dog_buster(name="Buster", loc=(0, 0, 0), rot=0):
    d = W.dog(name, loc, color="#8a5530")
    d.rotation_euler[2] = math.radians(rot)
    return d


def soda_bottle(name="MegaFizz", loc=(0, 0, 0), scale=1.0):
    root = empty(name, loc)
    Mb = mat("bottle_dark", (0.1, 0.04, 0.02), 0.1, alpha=0.8, spec=0.9)
    box(f"{name}_body", (0.5 * scale, 0.5 * scale, 1.4 * scale), (0, 0, 0.7 * scale), Mb, 0.08, parent=root)
    cyl(f"{name}_neck", 0.15 * scale, 0.4 * scale, (0, 0, 1.6 * scale), Mb, parent=root)
    box(f"{name}_cap", (0.32 * scale, 0.32 * scale, 0.15 * scale), (0, 0, 1.85 * scale), mat("cap_red", hexc("#d92b2b"), 0.3), 0.02, parent=root)
    return root


def chili_bowl(name="ChiliBowl", loc=(0, 0, 0), scale=1.0):
    root = empty(name, loc)
    Mb = mat("bowl_white", (0.9, 0.9, 0.95), 0.3)
    cyl(f"{name}_rim", 1.8 * scale, 0.9 * scale, (0, 0, 0.45 * scale), Mb, parent=root)
    cyl(f"{name}_stew", 1.6 * scale, 0.2 * scale, (0, 0, 0.65 * scale), mat("chili_brown", hexc("#7a2b16"), 0.8), parent=root)
    return root


def giant_boot(name="Boot", loc=(0, 0, 0), scale=1.0):
    root = empty(name, loc)
    Ms = mat("boot_black", hexc("#1a1a20"), 0.6)
    box(f"{name}_sole", (2.2 * scale, 4.4 * scale, 0.7 * scale), (0, 0.4 * scale, 0.35 * scale), mat("sole_gum", hexc("#c88a45"), 0.7), 0.1, parent=root)
    box(f"{name}_upper", (1.9 * scale, 3.8 * scale, 2.0 * scale), (0, 0.2 * scale, 1.5 * scale), Ms, 0.2, parent=root)
    return root


def textbook(name="Book", loc=(0, 0, 0), scale=1.0):
    root = empty(name, loc)
    box(f"{name}_cover", (2.2 * scale, 3.0 * scale, 0.4 * scale), (0, 0, 0), mat("book_blue", hexc("#2b5bb8"), 0.4), 0.04, parent=root)
    box(f"{name}_pages", (2.0 * scale, 2.8 * scale, 0.3 * scale), (0.05 * scale, 0, 0), mat("pages_cream", (0.95, 0.93, 0.88), 0.8), 0.02, parent=root)
    return root


def trash_can(name="Trash", loc=(0, 0, 0)):
    root = empty(name, loc)
    cyl(f"{name}_body", 2.2, 4.2, (0, 0, 2.1), mat("trash_metal", hexc("#60656e"), 0.4, metal=0.8), parent=root)
    return root


# ================================================================== 1. THE HOOK & RULE
@S(1, 0, 6, "HOOK: Eddie shrank to pencil size on the desk")
def s01(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.15)
    E.pose(t0, loc=(E_DESK[0], E_DESK[1] - 0.5, 3.4), rot=180)
    story._live(E, t0, t1, "shock")
    soda_bottle("MiniCan", (E_DESK[0] + 0.5, E_DESK[1] - 0.5, 3.4), scale=0.3)
    cam = Cam()
    cam.push(t0, t1, (E_DESK[0], E_DESK[1] - 0.5, 3.8), 2.2, 1.6, yaw=190, pitch=12, lens=28)
    cam.crash(t0 + 0.1, 28, 38, 0.1)
    cam.handheld(1.2)
    sfx(t0, "whoosh")
    sfx(w(1), "glitch")


@S(2, 6, 12, "Huge textbook falling toward tiny Eddie")
def s02(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.15)
    E.pose(t0, loc=(E_DESK[0], E_DESK[1] - 0.5, 3.4), rot=180)
    story._live(E, t0, t1, "scream")
    bk = textbook("FallingBook", (E_DESK[0], E_DESK[1] - 0.5, 8.0), scale=2.0)
    bk.keyframe_insert("location", frame=F(t0))
    bk.location = (E_DESK[0], E_DESK[1] - 0.5, 4.2)
    bk.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.push(t0, t1, (E_DESK[0], E_DESK[1] - 0.5, 4.5), 3.5, 2.5, yaw=210, pitch=25, lens=24)
    cam.handheld(1.5)
    sfx(t0 + 0.2, "whoosh")
    sfx(t1 - 0.1, "thud")


@S(3, 12, 22, "Teacher drops textbook, students in shock")
def s03(t0, t1):
    R, ks = class_scene(t0, t1, kids=6, board=BOARD)
    T = story.pickle(t0, t1, "shock")
    T.pose(t0, loc=(-1.5, 12.0, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (-1.5, 10.0, 5.0), 7.5, 6.0, yaw=0, pitch=8, lens=24)
    cam.crash(t0 + 0.1, 24, 32, 0.08)
    sfx(t0, "gasp")


@S(4, 22, 37, "RULE: You see in this world, hiccups shrink you by half")
def s04(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = eddie(t0, t1, "neutral")
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    E.talk(t0, t1)
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 4.5), 6.5, 5.0, yaw=180, pitch=4, lens=24)
    cam.handheld(0.8)


@S(5, 37, 45, "SOCIETY: Soda is banned in thirty countries (crossed out soda sign)")
def s05(t0, t1):
    W.town(school=True)
    W.sun(4.0)
    soda_bottle("BigSoda", (0, -25.0, 0), scale=3.0)
    cop = story.pilot(t0, t1, "neutral", name="Guard", shirt="#1e2a4a")
    cop.pose(t0, loc=(2.5, -24.0, 0), rot=210)
    cam = Cam()
    cam.push(t0, t1, (0, -24.0, 4.0), 9.0, 7.0, yaw=170, pitch=10, lens=22)
    sfx(t0, "buzzer")


@S(6, 45, 50, "SOCIETY: Roller coasters have toddler and ant seatbelts")
def s06(t0, t1):
    W.sky(1.0)
    W.sun(4.0)
    cart = box("coaster_cart", (4.0, 6.0, 2.0), (0, 0, 1.0), mat("coaster_red", hexc("#d92828"), 0.4), 0.1)
    ant_seat = box("ant_seat", (0.3, 0.3, 0.2), (0.8, 1.2, 2.1), mat("yellow_belt", hexc("#f0c020"), 0.3), 0.02)
    cam = Cam()
    cam.push(t0, t1, (0, 0, 2.5), 5.5, 4.0, yaw=140, pitch=15, lens=28)
    sfx(t0, "click")


@S(7, 50, 67, "SOCIETY: Tiny uncle carried in bride's purse")
def s07(t0, t1):
    W.town(school=False)
    W.sun(4.0)
    bride = story.grandma(t0, t1, "joy")
    bride.pose(t0, loc=(0, -20.0, 0), rot=180)
    purse = box("purse", (1.4, 0.6, 1.2), (1.1, -20.2, 3.0), mat("purse_white", (0.95, 0.95, 0.95), 0.3), 0.05)
    unc = chars.Char("TinyUncle", skin="#e9c7a6", shirt="#e8b520", pants="#3b3f4a", hair="short", hair_color="#5a3a22", scale=0.18)
    unc.pose(t0, loc=(1.1, -20.2, 3.7), rot=180)
    story._live(unc, t0, t1, "gasp")
    cam = Cam()
    cam.push(t0, t1, (1.1, -20.0, 3.8), 3.8, 2.6, yaw=185, pitch=8, lens=30)
    sfx(t0, "aww")


# ================================================================== 2. THE BUT PIVOT & CHALLENGE
@S(8, 67, 77, "PIVOT: But I have allergies and love fizzy soda")
def s08(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = eddie(t0, t1, "neutral")
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    E.talk(t0, t1)
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 4.5), 5.5, 4.2, yaw=175, pitch=5, lens=26)


@S(9, 77, 88, "Bully Crusher Carl confronts Eddie in cafeteria")
def s09(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    C = carl(t0, t1, "angry", loc=(-1.5, 7.0, 0), rot=160, scale=1.3)
    E = eddie(t0, t1, "shock")
    E.pose(t0, loc=(1.5, 6.5, 0), rot=200)
    cam = Cam()
    cam.push(t0, t1, (0, 6.8, 4.8), 6.5, 5.0, yaw=180, pitch=8, lens=24)
    cam.crash(t0 + 0.1, 24, 30, 0.08)


@S(10, 88, 97, "Carl slams the 2-liter Mega-Fizz on the cafeteria table")
def s10(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    soda = soda_bottle("MegaBottle", (0, 6.0, 3.3), scale=2.5)
    C = carl(t0, t1, "smile", loc=(-2.0, 6.5, 0), rot=150, scale=1.3)
    E = eddie(t0, t1, "shock")
    E.pose(t0, loc=(2.0, 6.0, 0), rot=210)
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 4.2), 4.8, 3.6, yaw=180, pitch=12, lens=28)
    sfx(t0 + 0.2, "thud")


@S(11, 97, 105, "Eddie chugs it, slams bottle, whole cafeteria cheers!")
def s11(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = eddie(t0, t1, "joy")
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    soda = soda_bottle("EmptyBottle", (0.8, 6.0, 3.3), scale=2.2)
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 4.4), 5.5, 4.0, yaw=180, pitch=6, lens=26)
    sfx(w(97), "thud")
    sfx(w(103), "cheer")


# ================================================================== 3. ESCALATION LADDER (SHRINKING)
@S(12, 105, 109, "Eddie's throat tickles, big panic reaction")
def s12(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = eddie(t0, t1, "gasp")
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 4.6), 4.0, 2.8, yaw=180, pitch=8, lens=32)
    cam.crash(t0 + 0.1, 32, 42, 0.08)
    sfx(t0, "alarm")


@S(13, 109, 111, "HIC! POOF! First shrink!")
def s13(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    thic = w(109)
    tpoof = w(110)
    W2.poof("poof1", (0, 6.0, 3.0), tpoof, s=1.2)
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 3.5), 5.0, 4.0, yaw=180, pitch=10, lens=28)
    cam.crash(tpoof, 28, 38, 0.1)
    sfx(thic, "pop")
    sfx(tpoof, "poof")


@S(14, 111, 119, "Clothes collapse into giant circus tent! 3 feet tall")
def s14(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.6)
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    story._live(E, t0, t1, "shock")
    tent = box("TentClothes", (3.2, 3.2, 2.2), (0, 6.0, 1.1), mat("cloth_blue", hexc("#2a75d9"), 0.8), 0.2)
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 2.5), 5.5, 4.0, yaw=180, pitch=12, lens=26)


@S(15, 119, 124, "Eddie realizes: I am three feet tall!")
def s15(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.6)
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    story._live(E, t0, t1, "scream")
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 2.8), 3.2, 2.2, yaw=180, pitch=6, lens=32)


@S(16, 124, 126, "HIC! POOF! Second shrink!")
def s16(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    thic = w(124)
    tpoof = w(125)
    W2.poof("poof2", (0, 6.0, 1.5), tpoof, s=1.0)
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 2.0), 4.5, 3.5, yaw=180, pitch=15, lens=28)
    sfx(thic, "pop")
    sfx(tpoof, "poof")


@S(17, 126, 134, "Sneaker size! Looking up at towering chairs")
def s17(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.25)
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    story._live(E, t0, t1, "shock")
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 1.0), 3.0, 2.0, yaw=180, pitch=25, lens=24)


@S(18, 134, 143, "Carl laughs and points: Look at the tiny bug!")
def s18(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    C = carl(t0, t1, "joy", loc=(0, 4.0, 0), rot=0, scale=1.35)
    cam = Cam()
    cam.push(t0, t1, (0, 4.0, 5.2), 5.5, 4.2, yaw=0, pitch=4, lens=26)
    cam.crash(t0 + 0.1, 26, 34, 0.08)
    sfx(t0, "kids_laugh")


@S(19, 143, 152, "Giant boot raised high to stomp on tiny Eddie!")
def s19(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    bt = giant_boot("CarlBoot", (0, 6.0, 5.0), scale=2.5)
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.25)
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    story._live(E, t0, t1, "scream")
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 2.5), 5.0, 3.8, yaw=190, pitch=30, lens=24)


@S(20, 152, 163, "STOMP! Eddie dodges, shockwave blasts him through the air!")
def s20(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    tstomp = w(152)
    bt = giant_boot("CarlBootStomp", (0, 6.0, 0), scale=2.5)
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.25)
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    E.root.keyframe_insert("location", frame=F(tstomp))
    E.root.location = (4.0, 10.0, 3.5)
    E.root.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.push(t0, t1, (2.0, 8.0, 2.5), 6.5, 4.5, yaw=200, pitch=15, lens=24)
    cam.crash(tstomp, 24, 36, 0.1)
    sfx(tstomp, "stomp")
    sfx(tstomp + 0.1, "whoosh")


@S(21, 163, 171, "SPLAT! Right into a steaming bowl of cafeteria chili")
def s21(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    tsplat = w(163)
    bowl = chili_bowl("Chili", (0, 8.0, 3.3), scale=1.5)
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.15)
    E.pose(t0, loc=(0, 8.0, 3.8), rot=180)
    story._live(E, t0, t1, "shock")
    cam = Cam()
    cam.push(t0, t1, (0, 8.0, 4.0), 3.0, 2.0, yaw=180, pitch=45, lens=28)
    cam.crash(tsplat, 28, 38, 0.1)
    sfx(tsplat, "splat")


# ================================================================== 4. DANGER MULTIPLIER (DOG & FLEA)
@S(22, 171, 179, "HIC! POOF! Now 2 inches tall in the chili!")
def s22(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    thic = w(171)
    tpoof = w(172)
    bowl = chili_bowl("Chili2", (0, 8.0, 3.3), scale=2.0)
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.08)
    E.pose(t0, loc=(0, 8.0, 3.7), rot=180)
    story._live(E, t0, t1, "gasp")
    W2.poof("poof3", (0, 8.0, 3.8), tpoof, s=0.6)
    cam = Cam()
    cam.push(t0, t1, (0, 8.0, 4.0), 2.2, 1.5, yaw=180, pitch=35, lens=32)
    sfx(thic, "pop")
    sfx(tpoof, "poof")


@S(23, 179, 190, "Lunch lady lifts the giant soup ladle with Eddie in it")
def s23(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    LL = lunch_lady(t0, t1, "neutral", loc=(-1.0, 10.0, 0), rot=180)
    ladle = cyl("ladle_handle", 0.1, 4.0, (0, 8.5, 4.5), mat("metal_spoon", (0.8, 0.8, 0.8), 0.3, metal=0.8), rot=(45, 0, 0))
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.08)
    E.pose(t0, loc=(0, 8.2, 4.0), rot=180)
    story._live(E, t0, t1, "scream")
    cam = Cam()
    cam.push(t0, t1, (0, 8.5, 4.5), 3.5, 2.2, yaw=170, pitch=15, lens=28)


@S(24, 190, 201, "She dumps chili onto Buster the guard dog's tray")
def s24(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    B = dog_buster("Buster", loc=(0, 5.0, 0), rot=0)
    tray = box("DogTray", (3.0, 2.0, 0.3), (0, 6.5, 0.2), mat("tray_blue", hexc("#2855a8"), 0.5), 0.05)
    cam = Cam()
    cam.push(t0, t1, (0, 5.8, 2.0), 5.5, 3.8, yaw=180, pitch=25, lens=24)
    sfx(t0 + 0.3, "splat")


@S(25, 201, 212, "Buster sniffs, growls, giant pink tongue swoops down!")
def s25(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    B = dog_buster("Buster", loc=(0, 4.0, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 4.8, 2.2), 3.8, 2.0, yaw=0, pitch=15, lens=24)
    cam.crash(t0 + 0.2, 24, 34, 0.1)
    sfx(w(201), "snort")
    sfx(w(212), "whoosh")


@S(26, 212, 218, "HIC! POOF! Shrinks again to the size of a flea!")
def s26(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    thic = w(213)
    tpoof = w(214)
    B = dog_buster("Buster", loc=(0, 4.0, 0), rot=0)
    W2.poof("poof4", (0, 4.6, 2.4), tpoof, s=0.4)
    cam = Cam()
    cam.push(t0, t1, (0, 4.6, 2.4), 2.0, 1.2, yaw=0, pitch=10, lens=36)
    sfx(thic, "pop")
    sfx(tpoof, "poof")


@S(27, 218, 231, "Flea-sized Eddie clinging to Buster's giant wet nose")
def s27(t0, t1):
    W.sky(1.0)
    W.sun(4.0)
    nose = sphere("DogNoseMacro", 3.0, (0, 0, 0), mat("wet_nose", hexc("#1a1515"), 0.1, spec=1.0))
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.08)
    E.pose(t0, loc=(0, -2.8, 0.5), rot=0)
    story._live(E, t0, t1, "shock")
    cam = Cam()
    cam.push(t0, t1, (0, -2.8, 0.5), 1.8, 1.2, yaw=0, pitch=5, lens=40)
    cam.handheld(1.5)


# ================================================================== 5. THE TWIST & CLIMAX
@S(28, 231, 241, "Buster takes a giant breath, about to sneeze!")
def s28(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    B = dog_buster("Buster", loc=(0, 4.0, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 4.6, 2.5), 3.5, 2.2, yaw=0, pitch=12, lens=28)
    sfx(t0 + 0.2, "rise")


@S(29, 241, 259, "TWIST: Scaring away hiccups grows you back instantly! And black pepper!")
def s29(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    B = dog_buster("Buster", loc=(0, 4.0, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, 4.6, 2.5), 2.2, 1.5, yaw=0, pitch=15, lens=32)
    sfx(w(241), "sparkle")


@S(30, 259, 279, "Eddie tickles Buster's nose hair inside the nostril!")
def s30(t0, t1):
    W.sky(1.0)
    W.sun(4.0)
    cave = cyl("NostrilCave", 2.5, 4.0, (0, 0, 0), mat("nostril_dark", hexc("#201010"), 0.8), rot=(90, 0, 0))
    E = chars.Char("Eddie", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.2)
    E.pose(t0, loc=(0, 0, 0), rot=180)
    story._live(E, t0, t1, "smile")
    cam = Cam()
    cam.push(t0, t1, (0, 0, 0.5), 2.5, 1.6, yaw=180, pitch=10, lens=30)
    sfx(t0 + 0.3, "click")


@S(31, 279, 283, "AH... AH... CHOO! Monster sneeze!")
def s31(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    B = dog_buster("Buster", loc=(0, 4.0, 0), rot=0)
    tsneeze = w(282)
    W2.poof("SneezeBlast", (0, 4.8, 2.2), tsneeze, s=2.5)
    cam = Cam()
    cam.push(t0, t1, (0, 4.8, 2.5), 4.5, 3.0, yaw=0, pitch=10, lens=24)
    cam.crash(tsneeze, 24, 36, 0.1)
    sfx(tsneeze, "sneeze")


@S(32, 283, 295, "Rocket launch! Flea Eddie blasts toward Carl's face!")
def s32(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = chars.Char("EddieRocket", skin="#f2c8a0", shirt="#2a75d9", pants="#2b2d38", hair="spiky", hair_color="#5a3a22", scale=0.15)
    E.pose(t0, loc=(0, 4.0, 3.0), rot=180)
    E.root.keyframe_insert("location", frame=F(t0))
    E.root.location = (0, -10.0, 5.0)
    E.root.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.push(t0, t1, (0, -3.0, 4.0), 6.0, 3.5, yaw=180, pitch=10, lens=22)
    sfx(t0, "rocket")


@S(33, 295, 309, "Carl sees flying speck heading for his eye and screams in horror!")
def s33(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    C = carl(t0, t1, "scream", loc=(0, -10.0, 0), rot=0, scale=1.35)
    cam = Cam()
    cam.push(t0, t1, (0, -10.0, 5.2), 4.5, 2.5, yaw=0, pitch=4, lens=32)
    cam.crash(t0 + 0.1, 32, 44, 0.1)
    sfx(w(309), "gasp")


@S(34, 309, 316, "The scream cures the hiccups! BOOM! Mid-air airbag expansion!")
def s34(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    tboom = w(316)
    W2.poof("AirbagBoom", (0, -9.0, 4.5), tboom, s=3.5)
    E = eddie(t0, t1, "determined")
    E.pose(t0, loc=(0, -9.0, 3.5), rot=180)
    cam = Cam()
    cam.push(t0, t1, (0, -9.0, 4.5), 6.5, 4.2, yaw=180, pitch=10, lens=24)
    cam.crash(tboom, 24, 38, 0.12)
    sfx(tboom, "boom")


# ================================================================== 6. THE PAYOFF & BUTTON
@S(35, 316, 335, "Full size Eddie body-slams Carl into the trash can!")
def s35(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    E = eddie(t0, t1, "determined")
    E.pose(t0, loc=(0, -8.0, 0), rot=180)
    tc = trash_can("Can", (0, -11.0, 0))
    C = carl(t0, t1, "shock", loc=(0, -11.0, 1.5), rot=180, scale=1.1)
    cam = Cam()
    cam.push(t0, t1, (0, -9.5, 4.0), 7.5, 5.0, yaw=190, pitch=15, lens=22)
    cam.crash(t0 + 0.2, 22, 32, 0.1)
    sfx(t0 + 0.2, "bonk")


@S(36, 335, 341, "The entire cafeteria erupts in wild cheers!")
def s36(t0, t1):
    R, ks = class_scene(t0, t1, kids=8, board=BOARD)
    E = eddie(t0, t1, "joy")
    E.pose(t0, loc=(0, 6.0, 0), rot=180)
    story.confetti("cheer_confetti", (0, 6.0, 6.0), (4.0, 4.0, 2.0), t0, n=60)
    cam = Cam()
    cam.push(t0, t1, (0, 6.0, 4.5), 8.0, 6.0, yaw=180, pitch=10, lens=22)
    sfx(t0, "cheer")


@S(37, 341, 358, "Carl crawls out of the trash covered in noodles, glaring")
def s37(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    tc = trash_can("Can2", (0, -11.0, 0))
    C = carl(t0, t1, "angry", loc=(0, -11.0, 0), rot=0, scale=1.2)
    cam = Cam()
    cam.push(t0, t1, (0, -11.0, 3.8), 4.8, 3.2, yaw=0, pitch=8, lens=28)


@S(38, 358, 371, "Then Carl hiccuped! HIC! POOF! Carl shrinks to teacup size!")
def s38(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    thic = w(361)
    tpoof = w(362)
    W2.poof("CarlShrink", (0, -11.0, 0.8), tpoof, s=1.5)
    C = chars.Char("CarlMini", skin="#e8b894", shirt="#c8382b", pants="#2b2d38", hair="buzz",
                   hair_color="#2b231d", face="villain", scale=0.15)
    C.pose(t0, loc=(0, -11.0, 0), rot=0)
    story._live(C, t0, t1, "shock")
    cam = Cam()
    cam.push(t0, t1, (0, -11.0, 1.2), 3.5, 2.0, yaw=0, pitch=25, lens=32)
    cam.crash(tpoof, 32, 42, 0.1)
    sfx(thic, "pop")
    sfx(tpoof, "poof")


@S(39, 371, None, "BUTTON: Buster the dog walks over. Sit, tiny Carl. Good boy.")
def s39(t0, t1):
    W.classroom_day(board=BOARD)
    W.sun(4.0)
    B = dog_buster("BusterFinal", loc=(0, -8.0, 0), rot=180)
    C = chars.Char("CarlFinal", skin="#e8b894", shirt="#c8382b", pants="#2b2d38", hair="buzz",
                   hair_color="#2b231d", face="villain", scale=0.15)
    C.pose(t0, loc=(0, -10.5, 0), rot=0)
    story._live(C, t0, t1, "shock")
    cam = Cam()
    cam.push(t0, t1, (0, -9.5, 2.0), 5.0, 3.4, yaw=160, pitch=18, lens=26)
    cam.handheld(1.0)
    sfx(w(371), "meow")
    sfx(w(382), "ding")
