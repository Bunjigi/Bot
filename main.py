import os
import discord
from discord.ext import commands
import random
import youtube_dl

bot = commands.Bot(command_prefix="$", description="Open service")
a = ["$hello", "$roll", "$ytb", "$tictactoe", "$frauduleux"]

musics = {}
ytdl = youtube_dl.YoutubeDL()
my_secret = os.environ['78']

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                     [2, 5, 8], [0, 4, 8], [2, 4, 6]]


async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        videoformat = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = videoformat["url"]

    def play_song(bot, song):
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url))

        bot.play(source)

    @bot.command
    async def play(ctx, v):
        if v.content.startswith('$ytb'):
            print("play")
            bot = ctx.guild.voice_client
            channel = ctx.author.voice.channel
            v = Video(v)
            musics[ctx.guild] = []
            bot = await channel.connect()
            await ctx.send("Play")
            bot.play_song(bot, v)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    @bot.command()
    async def tictactoe(ctx, p1: discord.Member, p2: discord.Member, message):
        if message.content.startswith("$tictactoe"):
            global count
            global player1
            global player2
            global turn
            global gameOver

            if gameOver:
                global board
                board = [
                    ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:",
                    ":white_large_square:"
                ]
                turn = ""
                gameOver = False
                count = 0

                player1 = p1
                player2 = p2

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                # determine who goes first
                num = random.randint(1, 2)
                if num == 1:
                    turn = player1
                    await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
                elif num == 2:
                    turn = player2
                    await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
                else:
                    await ctx.send(
                        "A game is already in progress! Finish it before starting a new one."
                    )

    @bot.command()
    async def place(ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                    else:
                        await ctx.send(
                            "Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile."
                        )
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send(
                "Please start a new game using the !tictactoe command.")

    def checkWinner(winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[
                    condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True

    @tictactoe.error
    async def tictactoe_error(ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "Please make sure to mention/ping players (ie. <@688534433879556134>)."
            )

    @place.error
    async def place_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")

    if message.content.startswith('$ytb'):

        class Video:
            def __init__(self, link):
                video = ytdl.extract_info(link, download=False)
                videoformat = video["formats"][0]
                self.url = video["webpage_url"]
                self.stream_url = videoformat["url"]

            def play_song(bot, song):
                source = discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(song.stream_url))
                bot.play(source)

        @bot.command
        async def play(ctx, v):
            if v.content.startswith('$ytb'):
                print("play")
                bot = ctx.guild.voice_client
                channel = ctx.author.voice.channel
                v = Video(v)
                musics[ctx.guild] = []
                bot = await channel.connect()
                await ctx.send("Play")
                bot.play_song(bot, v)

    if message.content.startswith('$frauduleux'):
        await message.channel.send('https://ultimate-t3.herokuapp.com/')

    if message.content.startswith('$help'):
        await message.channel.send('There is some commands :' + str(a))

    if message.content.startswith('$hello'):
        await message.channel.send(' salut')

    if message.content.startswith('$roll'):
        x = random.randint(0, 9999)
        if x == 1:
            await message.channel.send(
                'https://www.youtube.com/watch?v=oLUAjhXLLJY')
        if 1 < x and x <= 100:
            await message.channel.send(str(x))
            await message.channel.send(
                'https://www.youtube.com/watch?v=IBnq3fELuf8')
        if 101 <= x and x <= 3000:
            await message.channel.send(str(x))
            await message.channel.send('fine')
        if 3001 <= x and x <= 5449:
            await message.channel.send(str(x))
            await message.channel.send('MENTAL BOOM')
        if x >= 5501:
            await message.channel.send(str(x))

        if x >= 8250 and x <= 8350:
            await message.channel.send(str(x))
            await message.channel.send(
                "https://www.youtube.com/watch?v=21PxERIMYQw&list=PLkXhv9YYVUld4cycdwcZGjx1SoPEvVxPW&index=18"
            )

        if x >= 6500 and x <= 6700:
            await message.channel.send(str(x))
            await message.channel.send(
                "https://www.youtube.com/watch?v=JuaddpQA6Sw&list=PLkXhv9YYVUld4cycdwcZGjx1SoPEvVxPW&index=10"
            )

        if x >= 5450 and x <= 5500:
            await message.channel.send(str(x))
            await message.channel.send(
                'https://www.youtube.com/watch?v=oLUAjhXLLJY', "||get perm||")

        if x >= 9950:
            await message.channel.send(str(x))
            await message.channel.send(
                "https://www.youtube.com/watch?v=cba9yh_Jv6g&list=PLkXhv9YYVUld4cycdwcZGjx1SoPEvVxPW&index=5"
            )


bot.run(my_secret)
