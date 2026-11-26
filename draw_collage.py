#!/usr/bin/env python3
"""Render the 26 November 2026 front page as a 1024x1024 PNG.

Everything on the page -- masthead, lead tariff story with its little
bar chart, the 36-story grid and the footer -- is drawn with PIL from
the story list below. Running this file regenerates entry.png next
to it.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
# Grid geometry: 12 rows of 63px with 6px gutters starting at y=190
# end at y=1012, leaving just enough room for the footer at y=1014.
GRID_TOP = 190
CELL_W, CELL_H = 330, 63
ROW_GAP = 6
NAVY = (10, 46, 92)
PALE_BLUE = (180, 200, 225)
LEAD_BG = (250, 250, 248)
RED = (185, 28, 28)
GREY_TEXT = (68, 68, 68)
FAINT_GREY = (120, 120, 120)
CELL_EDGE = (217, 217, 217)

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (region tag, accent colour, headline, one-line summary)
STORIES = [
    ("MIDDLE EAST", (180, 83, 9), "THREE TANKERS BURN IN HORMUZ",
     "Iran says ships hit naval mines; US blockade grinds on"),
    ("MIDDLE EAST", (180, 83, 9), "HOUTHIS HIT RIYADH TOWER AGAIN",
     "11 hurt in strike on financial district; India condemns"),
    ("CHINA", (185, 28, 28), "CHINA PROBES SHANGHAI PARTY CHIEF",
     "Politburo member Chen Jining investigated for violations"),
    ("SPACE", (67, 56, 202), "FIRST FOREIGN ASTRONAUT ON CHINA STATION",
     "Pakistani astronaut joins Shenzhou-24 crew"),
    ("TECH", (3, 105, 161), "S&P PUTS NVIDIA ON DOWNGRADE WATCH",
     "Board turmoil after Huang's exit and return"),
    ("SPACE", (67, 56, 202), "SPACEX WINS FCC NOD FOR 1M SATELLITES",
     "Approval clears orbital AI data centres"),
    ("MARKETS", (4, 120, 87), "DOW CLOSES ABOVE 50,000",
     "Nasdaq slides 1.5% as chip stocks retreat"),
    ("USA", (31, 78, 121), "SECOND JUDGE BLOCKS BIRTHRIGHT ORDER",
     "Trump citizenship curbs halted again in court"),
    ("HEALTH", (190, 18, 60), "MEASLES KILLS 9 IN US THIS YEAR",
     "CDC counts 6,039 cases in worst outbreak in decades"),
    ("EUROPE", (29, 78, 216), "UKRAINE HITS RUSSIAN AIR BASE",
     "Kyiv says 5 planes damaged; Moscow hits bridges"),
    ("AFRICA", (21, 128, 61), "EGYPT TANKER FIRE KILLS 30",
     "Fuel truck overturns and explodes on Cairo ring road"),
    ("ASIA", (15, 118, 110), "NEPAL QUAKE 5.4 RATTLES REGION",
     "Tremors felt across eastern India"),
    ("ASIA", (15, 118, 110), "BANGLADESH RAISES GARMENT PAY 36%",
     "Minimum wage lifted after weeks of protests"),
    ("ASIA", (15, 118, 110), "GRAMEEN BANK HIT BY ARSON WAVE",
     "100 attacks in 15 days, lender says"),
    ("AFRICA", (21, 128, 61), "S. AFRICA COURT VOIDS RAMAPHOSA REPORT",
     "Impeachment findings ruled unlawful"),
    ("LATIN AMERICA", (126, 34, 206), "WHO: END US FUEL BLOCKADE ON CUBA",
     "Health chief warns of crisis on the island"),
    ("EUROPE", (29, 78, 216), "NATO BOOSTS EASTERN AIR WATCH",
     "Surveillance stepped up after missile crashes"),
    ("ASIA", (15, 118, 110), "S. KOREA WARNS OFF RUSSIAN JETS",
     "Evacuation alert after aircraft approach"),
    ("INDIA", (194, 65, 12), "INDIA MARKS CONSTITUTION DAY",
     "IITs to add 6,000 seats in robotics, AI and space"),
    ("ASIA", (15, 118, 110), "INDIA, CHINA RESUME BORDER TALKS",
     "Military discussions restart in Arunachal"),
    ("INDIA", (194, 65, 12), "INDIA'S LABOUR CODES TAKE EFFECT",
     "Sweeping reforms begin despite union protests"),
    ("LATIN AMERICA", (126, 34, 206), "COLOMBIA FREES 20 HOSTAGES",
     "Police storm Cartagena supermarket after 17-hour siege"),
    ("EUROPE", (29, 78, 216), "RECORD MIGRANTS REACH CANARIES",
     "Nearly 2,000 land in Spain in a single day"),
    ("EUROPE", (29, 78, 216), "EUROSTAR AXES TRAINS IN STRIKE",
     "London-Paris-Brussels services cancelled"),
    ("UK", (55, 65, 81), "RAF HIDES JETS FROM DRONES",
     "Warplanes moved into hangars at night"),
    ("MIDDLE EAST", (180, 83, 9), "GAZA STRIKE KILLS HAMAS OFFICIAL",
     "Naim Abu Nahal among seven dead despite ceasefire"),
    ("USA", (31, 78, 121), "US JOBLESS CLAIMS FALL TO 189,000",
     "Labour market holds steady, data shows"),
    ("EUROPE", (29, 78, 216), "EU FINES FRAGRANCE CARTEL 472M EUROS",
     "Price-fixing penalty for global makers"),
    ("ASIA", (15, 118, 110), "INDIA, CANADA NEAR TRADE DEAL",
     "Negotiators 'very close' on partnership pact"),
    ("CHINA", (185, 28, 28), "CHINA'S TRADE SURPLUS TOPS $1 TRILLION",
     "Exports defy tariffs to hit new high"),
    ("WORLD", (71, 85, 105), "BRICS SPLIT OVER IRAN WAR",
     "Ministers end talks with no joint statement"),
    ("WORLD", (71, 85, 105), "UN: FIVE WOMEN KILLED EVERY HOUR",
     "47,000 murdered by partners or kin in 2025"),
    ("USA", (31, 78, 121), "THANKSGIVING IN AMERICA",
     "Trump pardons turkeys Freedom and Feathers"),
    ("USA", (31, 78, 121), "ARMY BLOWS UP LEAD AZIDE STOCKPILE",
     "9,500 lbs detonated in Iowa; no toxic plume found"),
    ("SPORT", (77, 124, 15), "GUKESH FACES SINDAROV FOR WORLD TITLE",
     "India's champion opens chess final in Geneva"),
    ("SPORT", (77, 124, 15), "IPL AUCTION DRAWS 1,220 PLAYERS",
     "Teen Sooryavanshi hits 204 off 53 balls vs UAE"),
]

# Reported proposed tariff rates for the lead-story chart.
TARIFF_BARS = [
    ("CHINA", 40, (185, 28, 28)),
    ("INDIA", 25, (234, 88, 12)),
    ("EU", 15, (29, 78, 216)),
]


def load_font(bold, size):
    """Return a DejaVu font of the requested weight and size."""
    return ImageFont.truetype(BOLD_PATH if bold else PLAIN_PATH, size)


def text_width(draw, text, font):
    """Pixel width of `text` in `font`."""
    return draw.textlength(text, font=font)


def wrap_words(draw, text, font, max_width, max_lines):
    """Greedy word wrap, capped at `max_lines` lines (last line gets …)."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if text_width(draw, trial, font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
        if len(lines) == max_lines:
            break
    if len(lines) < max_lines and current:
        lines.append(current)
    if len(lines) == max_lines and current and lines[-1] != current:
        # The headline ran past the line budget: ellipsize the last line.
        tail = lines[-1]
        while tail and text_width(draw, tail + " …", font) > max_width:
            tail = tail.rsplit(" ", 1)[0] if " " in tail else tail[:-1]
        lines[-1] = tail + " …"
    return lines


def shorten_to_fit(draw, text, font, max_width):
    """Cut `text` at a word boundary and add … so it fits one line."""
    if text_width(draw, text, font) <= max_width:
        return text
    words = text.split()
    kept = ""
    for word in words:
        trial = word if not kept else kept + " " + word
        if text_width(draw, trial + " …", font) <= max_width:
            kept = trial
        else:
            break
    return (kept + " …") if kept else text[:1] + "…"


def centred(draw, text, font, fill, y, cx=PAGE_W // 2):
    """Draw `text` horizontally centred on `cx` at height `y`."""
    w = text_width(draw, text, font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def paint_masthead(draw):
    """Navy band with the date and the paper's tagline."""
    draw.rectangle([0, 0, PAGE_W, 80], fill=NAVY)
    centred(draw, "THURSDAY, 26 NOVEMBER 2026",
            load_font(True, 40), (255, 255, 255), 8)
    centred(draw, "T H E   W O R L D   I N   O N E   I M A G E",
            load_font(False, 17), PALE_BLUE, 54)


def paint_lead(draw):
    """Lead story strip: tag, headline, sub-line and tariff chart."""
    draw.rectangle([0, 86, PAGE_W, 184], fill=LEAD_BG)
    draw.rectangle([0, 86, 6, 184], fill=RED)
    draw.text((18, 94), "TRADE · WASHINGTON",
              font=load_font(True, 12), fill=RED)
    draw.text((18, 112), "TRUMP UNVEILS NEW TARIFFS ON 14 PARTNERS",
              font=load_font(True, 27), fill=(0, 0, 0))
    draw.text((18, 152), "China faces the steepest rates, up to 40%; EU 15%",
              font=load_font(False, 15), fill=GREY_TEXT)
    paint_tariff_chart(draw)


def paint_tariff_chart(draw):
    """Three vertical bars for the proposed tariff rates, x from 800."""
    base_y = 156          # shared baseline the bars stand on
    tallest = 56          # height of the tallest (40%) bar
    slot_w = 68           # horizontal space per bar
    bar_w = 38
    start_x = 800
    top_val = max(value for _, value, _ in TARIFF_BARS)
    value_font = load_font(True, 11)
    name_font = load_font(True, 10)
    caption_font = load_font(False, 10)
    for i, (name, value, colour) in enumerate(TARIFF_BARS):
        slot_x = start_x + i * slot_w
        height = round(tallest * value / top_val)
        bar_x0 = slot_x + (slot_w - bar_w) // 2
        draw.rectangle([bar_x0, base_y - height,
                        bar_x0 + bar_w, base_y], fill=colour)
        label = f"{value}%"
        lw = text_width(draw, label, value_font)
        draw.text((bar_x0 + (bar_w - lw) / 2, base_y - height - 15),
                  label, font=value_font, fill=(0, 0, 0))
        nw = text_width(draw, name, name_font)
        draw.text((slot_x + (slot_w - nw) / 2, base_y + 4),
                  name, font=name_font, fill=GREY_TEXT)
    caption = "Proposed tariff rates, %"
    cw = text_width(draw, caption, caption_font)
    chart_cx = start_x + (len(TARIFF_BARS) * slot_w) / 2
    draw.text((chart_cx - cw / 2, 174), caption,
              font=caption_font, fill=FAINT_GREY)


def paint_cell(draw, x, y, story):
    """One grid cell: accent bar, region tag, headline, summary."""
    tag, colour, headline, summary = story
    w, h = CELL_W, CELL_H
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=CELL_EDGE, width=1)
    draw.rectangle([x, y, x + 4, y + h], fill=colour)
    inner_x = x + 12
    inner_w = w - 20
    draw.text((inner_x, y + 4), tag, font=load_font(True, 10), fill=colour)
    # Headline: start at 14px bold, step down until it fits in two lines.
    size = 14
    while size > 9:
        font = load_font(True, size)
        lines = wrap_words(draw, headline, font, inner_w, 2)
        joined = " ".join(lines).replace(" …", "")
        if joined == headline or size == 10:
            break
        size -= 1
    font = load_font(True, size)
    lines = wrap_words(draw, headline, font, inner_w, 2)
    line_h = size + 2
    for j, line in enumerate(lines):
        draw.text((inner_x, y + 19 + j * line_h), line,
                  font=font, fill=(0, 0, 0))
    summary_font = load_font(False, 11)
    clipped = shorten_to_fit(draw, summary, summary_font, inner_w)
    draw.text((inner_x, y + 48), clipped, font=summary_font, fill=GREY_TEXT)


def paint_grid(draw):
    """3 columns x 12 rows of story cells, starting at y=190."""
    xs = [8, 347, 686]
    for idx, story in enumerate(STORIES):
        col, row = idx % 3, idx // 3
        paint_cell(draw, xs[col], GRID_TOP + row * (CELL_H + ROW_GAP), story)


def paint_footer(draw):
    """Centred credit line at the bottom of the page."""
    centred(draw,
            "26 NOVEMBER 2026 · 37 STORIES · SOURCES: REUTERS, AP, AFP, "
            "AL JAZEERA, ECONOMIC TIMES",
            load_font(False, 10), FAINT_GREY, 1014)


def build_page():
    """Compose the whole front page and return the image."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), (255, 255, 255))
    draw = ImageDraw.Draw(page)
    paint_masthead(draw)
    paint_lead(draw)
    paint_grid(draw)
    paint_footer(draw)
    return page


def main():
    page = build_page()
    page.save(OUT_PATH, "PNG", optimize=True)
    size = os.path.getsize(OUT_PATH)
    print(f"Saved {OUT_PATH}: {page.size[0]}x{page.size[1]}, {size} bytes")


if __name__ == "__main__":
    main()
