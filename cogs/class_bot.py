import io

import discord
import asyncio
import datetime
import traceback
import sys
import math
import easyimap

from tools import misc, lang, config, embeds, help, encryption, embeds
from discord.ext import commands, tasks

LESSON_TIMES = config.LESSON_TIMES
LESSON_TIMES_ENDS = config.LESSON_TIMES_ENDS

# should be 0
DEBUG_TIME_CHANGE = -3600

class Reminder:
    def __init__(self, r_time :int, embed, index=-1):
        self.r_time = r_time
        self.embed = embed
        self.index = index

    def __lt__(self, other):
        return self.r_time < other.r_time

class EmailChecker:

    def __init__(self, host, email, password, ssl, port, allow_addr):
        self.allow_addr = allow_addr
        self.immaper = easyimap.connect(host, email, password, 'INBOX', ssl=ssl, port=port)

    async def check(self, send_channel :discord.TextChannel):
        try:
            unseen_emails = self.immaper.unseen(limit=10)
            for mail in unseen_emails:
                to_addr = mail.to
                if self.allow_addr in to_addr:
                    embed = discord.Embed(
                        title=f'{mail.title} - {mail.from_addr}',
                        description=f'{mail.body.encode("UTF-8").decode("UTF-8")}',
                        color=config.v['EMAIL_COLOR']
                    )
                    await send_channel.send(embed=embed)
                    for attachment in mail.attachments:
                        f = discord.File(fp=io.BytesIO(attachment[1]))
                        f.filename = attachment[0].encode('UTF-8').decode('UTF-8')
                        await send_channel.send(file=f)

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

class SchoolClass:

    #region VARS
    name = ""
    reminders = []
    plan = []
    links = {}
    channel_id = 0
    channel = None
    pending_reminder = None
    edit_message = None
    email_checker = None
    #endregion

    def __init__(self, bot :commands.Bot):
        self.bot = bot

    #region FUNCS

    def run(self):
        self.channel = self.bot.get_channel(int(self.channel_id))
        if self.email_checker is not None:
            self.check_email.start()
        self.remind.start()
        self.rerun()

    def rerun(self):
        self.set_reminders()

    def set_reminders(self):
        LINK_COLOR = config.v['LINK_COLOR']
        HOLIDAY = config.v['HOLIDAY'] != 0
        try:
            now = misc.get_now()
            today = now.weekday()
            r_time = misc.get_now().timestamp()
            # for every lessons set in plan (eg. ["ANG, "INF])
            if HOLIDAY:
                return
            for i, lessons in enumerate(self.plan[today]):

                # if ["-"] (meaning no lesson)
                if len(lessons) == 1 and lessons[0] == "-":
                    continue

                # time to reminder
                r_time = datetime.datetime(
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=LESSON_TIMES[i][0],
                    minute=LESSON_TIMES[i][1]
                ).timestamp()

                r_time -= config.v['SECONDS_BEFORE_LINK']

                embed = discord.Embed(title="LINKS", color=LINK_COLOR)

                # for every lesson in lesson set
                for lesson in lessons:
                    if lesson in self.links.keys():
                        embed.add_field(
                            name=lesson,
                            value=self.links[lesson],
                        )
                    else:
                        raise ValueError(f"Lesson '{lesson}' doesn't exist! Bad JSON {self.name.upper()}.json")
                r = Reminder(int(r_time), embed, i)
                self.reminders.append(r)
            #add reminder after last lesson ("czas do konca lekcji" -> czas do tego remindera)
            self.reminders.append(Reminder(r_time + 45*60, None, -1))
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

    #endregion

    #region SCHOOL CLASS FUNCS

    def get_link(self, lesson=None):
        """
        :param lesson: lesson name (optional)
        :return: returns embed with link for current lesson or lesson in lesson param
        """
        LINK_COLOR = config.v['LINK_COLOR']
        HOLIDAY = config.v['HOLIDAY'] != 0
        # get link for next lesson
        if lesson is None:
            if HOLIDAY:
                embed_with_link = discord.Embed(title="WOLNE", color=LINK_COLOR)
            else:
                # if there are some reminders left
                if self.pending_reminder is not None:

                    # get time to first reminder in the sorted reminder list (in minutes)
                    time_left = int(math.ceil((self.pending_reminder.r_time - misc.get_now().timestamp() + DEBUG_TIME_CHANGE) / 60))

                    if self.pending_reminder.embed is not None:
                        embed_with_link = self.pending_reminder.embed.copy()
                        embed_with_link.title = f"Czas do lekcji: {time_left} {lang.get_pl_word('minut', time_left)}"
                    else:
                        # if reminder.embed is none it means its last lesson
                        embed_with_link = discord.Embed(title=f"Czas do konca lekcji: {time_left} {lang.get_pl_word('minut', time_left)}", color=LINK_COLOR)
                else:
                    embed_with_link = discord.Embed(title="WOLNE!", color=LINK_COLOR)
        else:
            #get specific link
            for link_key in self.links.keys():
                if link_key.lower() == lesson.lower():
                    embed_with_link = discord.Embed(title=lesson.upper(), description=self.links[link_key], color=LINK_COLOR)
                    break
            else:
                embed_with_link = discord.Embed(title=f"Nie ma lekcji {lesson}", color=LINK_COLOR)
        return embed_with_link

    def get_plan(self):
        """
        :return: embed with plan for today
        """
        LINK_COLOR = config.v['LINK_COLOR']
        now = misc.get_now()
        today = now.weekday()
        embed = discord.Embed(title="PLAN", color=LINK_COLOR)
        added = 0

        now_index = -1

        # if waiting for reminder
        if self.pending_reminder is not None:
            pending_index = self.pending_reminder.index - 1
            now = misc.get_now()
            # get pending reminder lesson end
            pending = datetime.datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=LESSON_TIMES_ENDS[pending_index][0],
                minute=LESSON_TIMES_ENDS[pending_index][1]
            ).timestamp()
            # set now_index accordingly
            if now.timestamp() - DEBUG_TIME_CHANGE < pending:
                now_index = pending_index
            else:
                now_index = pending_index + 1


        for i, lesson in enumerate(self.plan[today]):
            # if 'empty' lesson ["-"]
            if len(lesson) == 1 and lesson[0] == "-":
                continue

            time_start = str(LESSON_TIMES[i][0]).zfill(2) + ":" + str(LESSON_TIMES[i][1]).zfill(2)
            time_end = str(LESSON_TIMES_ENDS[i][0]).zfill(2) + ":" + str(LESSON_TIMES_ENDS[i][1]).zfill(2)

            # add :arrow: emojis only if now_index == i
            embed.add_field(name=(":arrow_forward: " if now_index == i else "")
                                 + " / ".join([x for x in lesson if x != "-"]).upper()
                                 +(" :arrow_backward:" if now_index == i else ""),
                            value=f"{time_start} - {time_end}",
                            inline=False)
            added += 1

        # if not added anything to plan
        if added == 0:
            embed.description = "WOLNE"

        return embed

    #endregion

    async def set_new_day(self):
        #check edit message
        if self.edit_message is not None:
            embed = self.get_link()
            await self.edit_message.edit(embed=embed)

    #region TASKS

    @tasks.loop(seconds=1)
    async def remind(self):
        self.reminders.sort()
        if len(self.reminders) > 0:
            reminder = self.reminders[0]
            #get time to next reminder
            waiting_time = reminder.r_time - misc.get_now().timestamp() + DEBUG_TIME_CHANGE
            if waiting_time > 0:
                self.pending_reminder = reminder
                if reminder.embed is not None:
                    self.bot.dispatch("pending_reminder_set", self.pending_reminder)
                    misc.log(f"Waiting... {waiting_time} {' / '.join([x.name for x in reminder.embed.fields])}")
                    # wait
                    await asyncio.sleep(waiting_time)
                    # send reminder
                    await self.channel.send(embed=reminder.embed)
                else:
                    misc.log(f"Waiting to end... {waiting_time}")
                    await asyncio.sleep(waiting_time)
            else:
                # if waiting time < 0 we should take next reminder
                # bc this reminder is late

                # reminder.embed is none if it is last reminder (look: set_reminders())
                if reminder.embed is not None:
                    misc.log(f"Skipping {' / '.join([x.name for x in reminder.embed.fields])}")
                else:
                    misc.log("Skipping 'THE END'")
            self.reminders.pop(0)
        else:
            # if no reminders left wait 30s
            self.pending_reminder = None
            await asyncio.sleep(30)

    @tasks.loop(minutes=3)
    async def check_email(self):
        await self.email_checker.check(self.channel)

    #endregion


class LessonBot(commands.Cog):
    school_classes = []

    def __init__(self, bot :commands.Bot):
        self.bot = bot
        self.refresh.start()

    #region FUNCS

    def get_class_index_from_channel_id(self, channel_id):
        for i, sc in enumerate(self.school_classes):
            if channel_id == sc.channel_id:
                return i
        return -1

    def get_class_index_from_name(self, name):
        name = name.lower()
        for i, sc in enumerate(self.school_classes):
            if name == sc.name.lower():
                return i
        return -1

    def resolve_link_cmd(self, ctx, args):
        """
        :param ctx: ctx of link cmd
        :param args: args of link cmd
        :return: (class index, lesson name)
        """
        """
        class index:
         -1 if cmd in non school class channel;
         -2 if can't identify class name
        """
        channel_id = ctx.message.channel.id
        index_from_channel = self.get_class_index_from_channel_id(channel_id)
        if len(args) == 0:
            if index_from_channel == -1:
                return -1, None # if only 'link' and can't find class channel
            else:
                return index_from_channel, None # if only 'link' and found class channel
        else:
            index_from_name = self.get_class_index_from_name(args[0])
            if index_from_name == -1:
                if index_from_channel == -1:
                    return -2, None # if 'link <sth>' and can't identify <sth> as class name and also can't fin class channel
                else:
                    return index_from_channel, args[0] # if 'link <lesson name>' can identify class channel and can't class name'
            elif len(args) == 1:
                return index_from_name, None # if 'link <class name>' can identify class name
            else:
                return index_from_name, args[1] # if 'link <class name> <lesson name>' can identify class name

    def resolve_plan_cmd(self, ctx, args):
        """
        :param ctx: ctx of link cmd
        :param args: args of link cmd
        :return: class_index

        """
        """
        class_index:
         -1 if cmd on non class channel;
         -2 if can't identify class name
        """
        channel_id = ctx.message.channel.id
        index_from_channel = self.get_class_index_from_channel_id(channel_id)
        if len(args) == 0:
            if index_from_channel == -1:
                return -1 # if only 'plan' and cant find channel
            else:
                return index_from_channel # if only 'plan' and can find channel
        else:
            index_from_name = self.get_class_index_from_name(args[0])
            if index_from_name == -1:
                if index_from_channel == -1:
                    return -2 #  if 'plan <class name>' and cant find class channel and class name
                else:
                    return index_from_channel # if 'plan <class name>' and cant find class name but can class channel
            return index_from_name  # if 'plan <class name>' and can find class name

    async def set_current_date(self):
        now = misc.get_now()
        date = f"📅Data: {str(now.day).zfill(2)}.{str(now.month).zfill(2)}.{now.year}"  # change channel name to current date
        channel = self.bot.get_channel(config.v['DATE_CHANNEL'])
        if channel is not None:
            await channel.edit(name=date)

    #endregion

    #region TASKS

    @tasks.loop(hours=24)
    async def refresh_next_day(self):
        # wait to whole minute
        now = misc.get_now()
        now_ = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute, second=1)
        whole = (now_ + datetime.timedelta(minutes=1)).timestamp()
        waiting_time = whole - now.timestamp()
        await asyncio.sleep(waiting_time)
        while True:
            # call check_everything() function
            for sc in self.school_classes:
                await sc.set_new_day()

            await asyncio.sleep(60)

    @tasks.loop(hours=24)
    async def refresh(self):
        await self.bot.wait_until_ready()
        now = misc.get_now()
        await self.set_current_date()
        midnight = int(86400 - (now.hour * 3600 + now.minute * 60 + now.second)) #seconds to midnight
        await asyncio.sleep(midnight)
        await self.set_current_date()
        for sc in self.school_classes: # reset school classes
            sc.rerun()

    #endregion

    #region EVENTS
    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        self.refresh_next_day.start()
        for sc in self.school_classes:
            sc.run()

    #endregion

    #region CMD
    @commands.command(name="link")
    async def send_link_cmd(self, ctx, *args):
        await ctx.message.delete()

        LINK_COLOR = config.v['LINK_COLOR']

        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "link"))
            return

        school_class_index, link = self.resolve_link_cmd(ctx, args)

        if school_class_index == -1:
            await ctx.send(embed=embeds.school_class_cmd_on_different_channel)

        elif school_class_index == -2:
            await ctx.send(
                embed = discord.Embed(
                    title = f"Nie ma klasy '{args[0]}'",
                    color = LINK_COLOR
                )
            )
        else:
            school_class = self.school_classes[school_class_index]
            embed = school_class.get_link(link)
            msg = await ctx.send(embed=embed)
            if school_class.edit_message is not None and link is None:
                await school_class.edit_message.delete()
                school_class.edit_message = msg


    @commands.command(name="plan")
    async def send_plan_cmd(self, ctx, *args):
        await ctx.message.delete()

        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "plan"))
            return

        LINK_COLOR = config.v['LINK_COLOR']

        school_class_index = self.resolve_plan_cmd(ctx, args)
        if school_class_index == -1:
            await ctx.send(embed=embeds.school_class_cmd_on_different_channel)
        elif school_class_index == -2:
            await ctx.send(
                embed=discord.Embed(
                    title=f"Nie ma klasy '{args[0]}'",
                    color=LINK_COLOR
                )
            )
        else:
            embed = self.school_classes[school_class_index].get_plan()
            await ctx.send(embed=embed)


    #endregion

#region SETUP
def load_school_classes(bot):
    school_classes = []
    for school_class, data in misc.get_every_school_class_json():
        # check if file is correct
        missing = misc.check_dict(['plan', 'links', 'channel_id'], data)
        if len(missing) > 0:
            misc.log(f"Bad JSON '{school_class}.json'! {len(missing)} missing values: {', '.join(missing)}")
            continue
        # add SchoolClass object
        sc = SchoolClass(bot)
        sc.name = school_class
        sc.plan = data['plan']
        sc.links = data['links']
        sc.channel_id = data['channel_id']
        if 'email' in data.keys():
            host = encryption.decrypt(data['email']['host'].encode("ASCII"))
            email = encryption.decrypt(data['email']['mail'].encode("ASCII"))
            password = encryption.decrypt(data['email']['password'].encode("ASCII"))
            ssl = data['email']['ssl']
            port = data['email']['port']
            allow_addr = data['email']['allow_addr']
            sc.email_checker = EmailChecker(host, email, password, ssl, port, allow_addr)
        school_classes.append(sc)
        misc.log(f"Loaded {sc.name}")
    return school_classes


def setup(bot :commands.Bot):
    ls = LessonBot(bot)
    ls.school_classes = load_school_classes(bot)
    bot.add_cog(ls)
#endregion