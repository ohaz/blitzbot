import irc.bot
import irc.strings
import irc.client
import tweepy
import urllib.request
from urllib.request import Request
from urllib.parse import urlencode
import json
import re
import time
from threading import Thread
import feedparser
from jaraco.stream import buffer
import traceback
import sys
from py_expression_eval import Parser as MathParser

from config import google_api_key, twitter_access_token, twitter_access_key, twitter_oauth_key, twitter_oauth_token, owner_nick, nickserv_identify

__author__ = 'ohaz'


class IgnoreErrorsBuffer(buffer.DecodingLineBuffer):
    def handle_exception(self):
        pass

nuclear_char_id_to_name = {
    1: 'Fish',
    2: 'Crystal',
    3: 'Eyes',
    4: 'Melting',
    5: 'Plant',
    6: 'Y.V.',
    7: 'Steroids',
    8: 'Robot',
    9: 'Chicken',
    10: 'Rebel',
    11: 'Horror',
    12: 'Rogue'
}

nuclear_crown_id_to_name = {
    1: 'No Crown',
    2: 'Crown of Death',
    3: 'Crown of Life',
    4: 'Crown of Haste',
    5: 'Crown of Guns',
    6: 'Crown of Hatred',
    7: 'Crown of Blood',
    8: 'Crown of Destiny',
    9: 'Crown of Love',
    10: 'Crown of Risk',
    11: 'Crown of Curses',
    12: 'Crown of Luck',
    13: 'Crown of Protection'
}

nuclear_mutation_list = [
    'Heavy Heart',
    'Rhino Skin',
    'Extra Feet',
    'Plutonium Hunger',
    'Rabbit Paw',
    'Throne Butt',
    'Lucky Shot',
    'Bloodlust',
    'Gamma Guts',
    'Second Stomach',
    'Back Muscle',
    'Scarier Face',
    'Euphoria',
    'Long Arms',
    'Boiling Veins',
    'Shotgun Shoulders',
    'Recycle Gland',
    'Laser Brain',
    'Last Wish',
    'Eagle Eyes',
    'Impact Wrists',
    'Bolt Marrow',
    'Stress',
    'Trigger Fingers',
    'Sharp Teeth',
    'Patience',
    'Hammerhead',
    'Strong Spirit',
    'Open Mind'
]

nuclear_weapon_id_to_name = {
    0: 'N/A',
    1: 'Revolver',
    2: 'Triple Machinegun',
    3: 'Wrench',
    4: 'Machinegun',
    5: 'Shotgun',
    6: 'Crossbow',
    7: 'Grenade Launcher',
    8: 'Double Shotgun',
    9: 'Minigun',
    10: 'Auto Shotgun',
    11: 'Auto Crossbow',
    12: 'Super Crossbow',
    13: 'Shovel',
    14: 'Bazooka',
    15: 'Sticky Launcher',
    16: 'SMG',
    17: 'Assault Rifle',
    18: 'Disk Gun',
    19: 'Laser Pistol',
    20: 'Laser Rifle',
    21: 'Slugger',
    22: 'Gatling Slugger',
    23: 'Assault Slugger',
    24: 'Energy Sword',
    25: 'Super Slugger',
    26: 'Hyper Rifle',
    27: 'Screwdriver',
    28: 'Laser Minigun',
    29: 'Blood Launcher',
    30: 'Splinter Gun',
    31: 'Toxic Bow',
    32: 'Sentry Gun',
    33: 'Wave Gun',
    34: 'Plasma Gun',
    35: 'Plasma Cannon',
    36: 'Energy Hammer',
    37: 'Jackhammer',
    38: 'Flak Cannon',
    39: 'Golden Revolver',
    40: 'Golden Wrench',
    41: 'Golden Machinegun',
    42: 'Golden Shotgun',
    43: 'Golden Crossbow',
    44: 'Golden Grenade Launcher',
    45: 'Golden Laser Pistol',
    46: 'Chicken Sword',
    47: 'Nuke Launcher',
    48: 'Ion Cannon',
    49: 'Quadruple Machinegun',
    50: 'Flamethrower',
    51: 'Dragon',
    52: 'Flare Gun',
    53: 'Energy Screwdriver',
    54: 'Hyper Launcher',
    55: 'Laser Cannon',
    56: 'Rusty Revolver',
    57: 'Lightning Pistol',
    58: 'Lightning Rifle',
    59: 'Lightning Shotgun',
    60: 'Super Flak Cannon',
    61: 'Sawed Off Shotgun',
    62: 'Splinter Pistol',
    63: 'Super Splinter Gun',
    64: 'Lightning SMG',
    65: 'Smart Gun',
    66: 'Heavy Crossbow',
    67: 'Blood Hammer',
    68: 'Lightning Cannon',
    69: 'Pop Gun',
    70: 'Plasma Rifle',
    71: 'Pop Rifle',
    72: 'Toxic Launcher',
    73: 'Flame Cannon',
    74: 'Lightning Hammer',
    75: 'Flame Shotgun',
    76: 'Double Flame Shotgun',
    77: 'Auto Flame Shotgun',
    78: 'Cluster Launcher',
    79: 'Grenade Shotgun',
    80: 'Grenade Rifle',
    81: 'Rogue Rifle',
    82: 'Party Gun',
    83: 'Double Minigun',
    84: 'Gatling Bazooka',
    85: 'Auto Grenade Shotgun',
    86: 'Ultra Revolver',
    87: 'Ultra Laser Pistol',
    88: 'Sledgehammer',
    89: 'Heavy Revolver',
    90: 'Heavy Machinegun',
    91: 'Heavy Slugger',
    92: 'Ultra Shovel',
    93: 'Ultra Shotgun',
    94: 'Ultra Crossbow',
    95: 'Ultra Grenade Launcher',
    96: 'Plasma Minigun',
    97: 'Devastator',
    98: 'Golden Plasma Gun',
    99: 'Golden Slugger',
    100: 'Golden Splinter Gun',
    101: 'Golden Screwdriver',
    102: 'Golden Bazooka',
    103: 'Golden Assault Rifle',
    104: 'Super Disk Gun',
    105: 'Heavy Auto Crossbow',
    106: 'Heavy Assault Rifle',
    107: 'Blood Cannon',
    108: 'Dog Bullet',
    109: 'Dog Missile',
    110: 'Incinerator',
    111: 'Super Plasma Cannon',
    112: 'Seeker Pistol',
    113: 'Seeker Shotgun',
    114: 'Eraser',
    115: 'Guitar',
    116: 'Bouncer SMG',
    117: 'Bouncer Shotgun',
    118: 'Hyper Slugger',
    119: 'Super Bazooka',
    120: 'Frog Pistol',
    121: 'Black Sword',
    120120120: 'Golden Frog Pistol'
}

irc.client.ServerConnection.buffer_class = IgnoreErrorsBuffer


class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.groups = []  # [{'owner': 'a', 'time': 123, 'members': ['b', 'c']}]
        self.twitter_auth = tweepy.OAuthHandler(twitter_oauth_key, twitter_oauth_token)
        self.twitter_auth.set_access_token(twitter_access_key, twitter_access_token)
        self.twitter_api = tweepy.API(self.twitter_auth)
        self.rss_last_timestamp = time.time()
        self.rss_channel = channel
        self.rss_thread = Thread(target=self.rss_thread)
        self.rss_thread.start()
        self.math_parser = MathParser()
        self.check_functions = [self.check_blitz_file, self.check_blitz_post, self.check_blitz_topic,
                                self.check_steam_store, self.check_twitch, self.check_twitter, self.check_youtube,
                                self.check_imdb]
        self.patterns = {
            'youtube': re.compile(
                r"https*:\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-]+)(&(amp;)?[\w\?=]*)?"),
            'youtu.be': re.compile(r"^.*(youtu.be\/|list=)([^#\&\?]*).*"),
            'twitter': re.compile(r"https?:\/\/twitter\.com\/(?:#!\/)?\w+\/status[es]?\/(\d+)"),
            'blitz_post': re.compile(r"https*:\/\/(?:www\.)?blitzforum.de\/forum\/viewtopic.php\?p=([0-9]*)[#0-9]*"),
            'blitz_topic': re.compile(r"https*:\/\/(?:www\.)?blitzforum.de\/forum\/viewtopic.php\?t=([0-9]*)[#0-9]*"),
            'blitz_file': re.compile(r"https*:\/\/(?:www\.)?blitzforum.de\/upload\/file.php\?id=([0-9]*)[#0-9]*"),
            'steam_store': re.compile(r'https*:\/\/store\.steampowered\.com\/app\/(\d*)\/*'),
            'twitch': re.compile(r'https*://w{0,3}\.*twitch.tv/(\S*)'),
            'imdb': re.compile(r'https*://www.imdb.com/title/(tt\d{7})/')
        }
        self.nuc_throne = {}
        self.reload_nuc_throne()

    def rss_thread(self):
        try:
            time.sleep(10)
        except:
            pass
        while True:
            try:
                d = feedparser.parse('http://www.blitzforum.de/forum/rss.php')
                sorted_entries = sorted(d['entries'], key=lambda element: time.mktime(element['published_parsed']))
                for e in sorted_entries:
                    if time.mktime(e['published_parsed']) > self.rss_last_timestamp:
                        self.rss_last_timestamp = time.mktime(e['published_parsed'])
                        self.connection.privmsg(self.rss_channel,
                                                'Blitzforum: {} by {} ({})'.format(e['title'], e['author'], e['link']))
                time.sleep(60 * 5)
            except Exception as e:
                print(e)
                traceback.print_exc(file=sys.stdout)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)
        c.privmsg('NICKSERV', nickserv_identify)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_join(self, c, e):
        self.manage_groups(c, e)

    def check_youtube(self, c, e):
        vid = self.patterns['youtube'].search(e.arguments[0])
        if vid is not None:
            vid1 = vid.group(1)
            f = urllib.request.urlopen(
                'https://www.googleapis.com/youtube/v3/videos?key=' + google_api_key + '&part=snippet,statistics,contentDetails&id=' + vid1)
            json_text = json.loads(f.read().decode('utf-8'))
            length = json_text['items'][0]['contentDetails']['duration']
            length = length.replace('PT', '')
            length = length.replace('S', '')
            length = length.replace('M', ':')
            length = length.replace('H', ':')
            t = length.split(':')
            n = [(lambda x: str(x) if len(x) > 1 else '0' + str(x))(x) for x in t]
            length = ':'.join(n)
            if 'likeCount' not in json_text['items'][0]['statistics']:
                json_text['items'][0]['statistics']['likeCount'] = 0
            if 'dislikeCount' not in json_text['items'][0]['statistics']:
                json_text['items'][0]['statistics']['dislikeCount'] = 0
            c.privmsg(e.target, 'Youtube: {} - {} [+{}, -{}]'.format(
                json_text['items'][0]['snippet']['title'], length, json_text['items'][0]['statistics']['likeCount'],
                json_text['items'][0]['statistics']['dislikeCount']))
        pl = self.patterns['youtu.be'].search(e.arguments[0])
        if pl is not None:
            plid = pl.group(2)
            f = urllib.request.urlopen(
                'https://www.googleapis.com/youtube/v3/playlists?key=' + google_api_key + '&part=snippet&id=' + plid)
            json_text = json.loads(f.read().decode('utf-8'))
            c.privmsg(e.target, 'Youtube Playlist: {}'.format(json_text['items'][0]['snippet']['title']))

    def check_twitter(self, c, e):
        tweet = self.patterns['twitter'].search(e.arguments[0])
        if tweet is not None:
            twid = tweet.group(1)
            tw_status = self.twitter_api.get_status(twid)
            text = tw_status.text.replace('\r', '')
            text = text.replace('\n', ' | ')
            c.privmsg(e.target, '{}(@{}): {}'.format(tw_status.author.name, tw_status.author.screen_name, text))

    def check_blitz_post(self, c, e):
        blitz = self.patterns['blitz_post'].search(e.arguments[0])
        if blitz is not None:
            blid = blitz.group(1)
            f = urllib.request.urlopen('http://www.blitzforum.de/api.php?p=' + blid)
            json_text = json.loads(f.read().decode('utf-8'))
            c.privmsg(e.target, 'Blitzforum: {} in "{}" von {} ({} Antworten, {} Views)'.format(
                json_text['post']['username'],
                json_text['post']['topic'][
                    'title'],
                json_text['post']['topic'][
                    'username'],
                json_text['post']['topic'][
                    'replies'],
                json_text['post']['topic'][
                    'views']))

    def check_blitz_topic(self, c, e):
        blitz = self.patterns['blitz_topic'].search(e.arguments[0])
        if blitz is not None:
            blid = blitz.group(1)
            f = urllib.request.urlopen('http://www.blitzforum.de/api.php?t=' + blid)
            json_text = json.loads(f.read().decode('utf-8'))
            c.privmsg(e.target, 'Blitzforum: "{}" von {} ({} Antworten, {} Views)'.format(
                json_text['topic'][
                    'title'],
                json_text['topic']['username'],
                json_text['topic'][
                    'replies'],
                json_text['topic'][
                    'views']))

    def check_blitz_file(self, c, e):
        blitz = self.patterns['blitz_file'].search(e.arguments[0])
        if blitz is not None:
            blid = blitz.group(1)
            f = urllib.request.urlopen('http://www.blitzforum.de/api.php?file=' + blid)
            json_text = json.loads(f.read().decode('utf-8'))
            c.privmsg(e.target, 'Blitzforum: "{}" von {} ({}, DL: {})'.format(
                json_text['file'][
                    'title'],
                json_text['file']['username'],
                json_text['file'][
                    'size'],
                json_text['file'][
                    'downloads']))

    def check_steam_store(self, c, e):
        steam = self.patterns['steam_store'].search(e.arguments[0])
        if steam is not None:
            stid = steam.group(1)
            f = urllib.request.urlopen('http://store.steampowered.com/api/appdetails?appids={}'.format(stid))
            json_text = json.loads(f.read().decode('utf-8'))
            game = json_text[stid]
            if game['success']:
                if game['data']['is_free']:
                    price = 'Free'
                else:
                    pr = '{},{}'.format(int(game['data']['price_overview']['final'] / 100),
                                        game['data']['price_overview']['final'] % 100)
                    price = pr + ' ' + game['data']['price_overview']['currency']
                    price += ' (-{}%)'.format(game['data']['price_overview']['discount_percent'])
                platforms = [key for key, value in game['data']['platforms'].items() if value]
                c.privmsg(e.target, 'Steam: "{}" -- Preis: {} Systeme: {}'.format(game['data']['name'], price,
                                                                                  ', '.join(platforms)))

    def check_twitch(self, c, e):
        twitch = self.patterns['twitch'].search(e.arguments[0])
        if twitch is not None:
            twid = twitch.group(1)
            r = Request('https://api.twitch.tv/kraken/streams/{}'.format(twid))
            r.add_header('Client-ID', 'gq4wx6vlabu02b71dh3cn1q4si38l3e')
            f = urllib.request.urlopen(r)
            json_text = json.loads(f.read().decode('utf-8'))
            if 'error' in json_text:
                c.privmsg(e.target, 'Twitch: {}'.format(json_text['message']))
            else:
                if json_text['stream'] is not None:
                    tw_chan = json_text['stream']['channel']
                    c.privmsg(e.target, 'Twitch: {} playing {}: {}'.format(tw_chan['display_name'], tw_chan['game'],
                                                                           tw_chan['status']))

    def check_imdb(self, c, e):
        imdb = self.patterns['imdb'].search(e.arguments[0])
        if imdb is not None:
            imdb_id = imdb.group(1)
            f = urllib.request.urlopen('http://www.omdbapi.com/?i={}&plot=short&r=json'.format(imdb_id))
            json_text = json.loads(f.read().decode('utf-8'))
            c.privmsg(e.target,
                      'IMDB: {} ({}) Runtime: {} Genre: [{}] imdbRating: {}'.format(json_text['Title'],
                                                                                    json_text['Year'],
                                                                                    json_text['Runtime'],
                                                                                    json_text['Genre'],
                                                                                    json_text['imdbRating']))

    def on_pubmsg(self, c, e):
        try:
            if e.arguments[0].startswith('!'):
                cmd = ((e.arguments[0].split(' '))[0]).replace('!', '')
                self.do_command(e, cmd)
            for check in self.check_functions:
                check(c, e)
        except Exception as e:
            print(e)
            traceback.print_exc(file=sys.stdout)
        return

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection
        cmds = {'disconnect': self.do_disconnect, 'die': self.do_die, 'a': self.code_archive, 'h': self.help_blitz,
                'g': self.group_finder, 'help': self.help_bot, 'u': self.upload_page, 'ud': self.urban_dictionary,
                'reload': self.reload, 'nc': self.nuclear_throne, 'm': self.math}
        if cmd in cmds:
            cmds[cmd](e)

    def math(self, e):
        s = e.arguments[0].split(' ', 1)[1]
        ms = s.split('with')
        d = {}
        if len(ms) > 1:
            splits = ms[1].split(',')
            for split in splits:
                ns = split.split('=')
                d[ns[0].strip()] = int(ns[1].strip())
        self.connection.privmsg(e.target, self.math_parser.parse(ms[0]).evaluate(d))

    def reload(self, e):
        if not e.source.nick == owner_nick:
            return
        s = []
        if not self.reload_nuc_throne():
            s.append('Could not load Nuclear Throne JSON')
        if len(s):
            self.connection.privmsg(e.target, 'Error: '+' | '.join(s))

    def nuclear_throne(self, e):
        s = e.arguments[0].split(' ')
        if len(s) < 2:
            self.connection.privmsg(e.target, 'Nick required!')
            return
        if s[1] in self.nuc_throne:
            char = self.nuc_throne[s[1]]
            with urllib.request.urlopen(
                    'https://tb-api.xyz/stream/get?s={}&key={}'.format(char['steam64'], char['key'])) as response:
                run = json.loads(response.read().decode('utf-8'))
                current = run['current']
                if current:
                    crown_string = ', Crown: ' + nuclear_crown_id_to_name[current['crown']] if current['crown'] != 1 else ''
                    self.connection.privmsg(e.target, '{}: Mit {} (lvl: {}, HP: {}) in {}-{} | {} Kills, Waffen: {} | {}{}'.format(
                        s[1], nuclear_char_id_to_name[int(current['char'])], current['charlvl'], current['health'],
                        current['world'], current['level'], current['kills'],
                        nuclear_weapon_id_to_name[int(current['wepA'])], nuclear_weapon_id_to_name[int(current['wepB'])],
                        crown_string
                    ))
                else:
                    self.connection.privmsg(e.target, s[1] + ' spielt gerade kein Nuclear Throne!')
        else:
            self.connection.privmsg(e.target, s[1] + ' ist nicht in meiner Liste! Schicke die passende Steam64 ID und den Stream Key an '+owner_nick+'!')

    def reload_nuc_throne(self):
        try:
            with open('nuc_throne.json') as f:
                self.nuc_throne = json.loads(f.read())
                return True
        except:
            return False

    def help_bot(self, e):
        self.connection.privmsg(e.target, 'Bekannte Befehle: !a (Code Archive), !h <blitz befehl> (Hilfe), '
                                          '!g <user1> <user2> ... (Gruppensuche), !u (Upload Page), '
                                          '!ud <query> (Urban Dictionary), !help (Diese Hilfe), !nc <nick>, !m <expr> [with x=3,y=4]')

    def group_finder(self, e):
        already = len([x for x in self.groups if x['owner'] == e.source.nick])
        members = (e.arguments[0].split(' '))[1:]
        if already < 2:
            self.groups.append({'owner': e.source.nick, 'time': time.time(), 'members': members})

    def hamming(self, s1, s2):
        return 1 - float(sum(el1 != el2 for el1, el2 in zip(s1, s2))) / min(len(s1), len(s2))

    def manage_groups(self, c, e):
        to_delete = []
        t = time.time()
        difference = 60 * 60 * 4
        for group in self.groups:
            if group['time'] - t > difference:
                to_delete.append(group)
                continue
            for ch in self.channels:
                channel = self.channels[ch]
                users_here = []
                for member in group['members']:
                    for user in channel.users():
                        next_u = False
                        if self.hamming(member, user) >= 0.75:
                            users_here.append(user)
                            next_u = True
                        if next_u:
                            break
                if len(users_here) == len(group['members']):
                    c.privmsg(ch, 'Hey ' + ', '.join(users_here) + ': ' + group[
                        'owner'] + ' hat auf euch gewartet!')
                    to_delete.append(group)
        for group in to_delete:
            self.groups.remove(group)

    def urban_dictionary(self, e):
        c = self.connection
        req = e.arguments[0].split(' ')[1:]
        c.privmsg(e.target, 'http://www.urbandictionary.com/define.php?' + urlencode({'term': ' '.join(req)}))

    def upload_page(self, e):
        c = self.connection
        c.privmsg(e.target, 'http://www.blitzforum.de/upload/upload.php')

    def help_blitz(self, e):
        c = self.connection
        req = e.arguments[0].split(' ')[1]
        c.privmsg(e.target, 'http://www.blitzforum.de/help/' + req)

    def code_archive(self, e):
        c = self.connection
        c.privmsg(e.target, 'http://www.blitzforum.de/upload/newcode.php')

    def do_disconnect(self, e):
        if e.source.nick == owner_nick:
            self.disconnect()

    def do_die(self, e):
        if e.source.nick == owner_nick:
            self.die()
            exit()


def main():
    b = Bot("#basic", "PBB", "blitzforum.de")
    b.start()


if __name__ == "__main__":
    main()
