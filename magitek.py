# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import dill as pickle

TOKEN = 'NDQ0MjM0MDk4NjgxMTg0MjY2.DdY-UA.yedICpvbcXVLIgT8RcAz_dWPFHM'
COMMAND_DB = 'commands.pkl'
client = discord.Client()

class Command(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func

commands = {}

# Load commands
with open(COMMAND_DB, "rb") as db:
    while True:
        try:
            cmd = pickle.load(db)
            commands[cmd.name] = cmd
        except EOFError:
            break

# Permanent commands. These cannot be overwritten!
commands['addcommand'] = Command('addcommand',
    lambda args, user: new_text_cmd(args.pop(0), ' '.join(args))
)
commands['rmcommand'] = Command('rmcommand',
    lambda args, user: rm_text_command(args.pop(0), user)
)
commands['help'] = Command('help',
    lambda args, user: help_cmd()
)

def new_text_cmd(name, text):
    if name in commands:
        return "There already exists a command by that name!"
    cmd = Command(name, lambda args, user: text)
    commands[cmd.name] = cmd
    with open(COMMAND_DB, "ab") as db:
        pickle.dump(cmd, db, pickle.HIGHEST_PROTOCOL)
    return "New command !" + name + " registered!"

def rm_text_command(name, user):
    if "Admin" in user.roles or "Council of Elders" in user.roles:
        if name in commands:
            commands.pop(name)
            open(COMMAND_DB, "wb").close()
            with open(COMMAND_DB, "ab") as db:
                for cmd in commands:
                    pickle.dump(cmd, db, pickle.HIGHEST_PROTOCOL)
            return "Removed command !" + name + "!"
        else:
            return "Couldn't find command !" + name + "."
    else:
        return "Not an admin"

def help_cmd():
    msg = "I'm a bot custom-made for the FFWiki. I support links: try typing {{navbox FFVI}} or [[Jenova]]!"
    msg += "\n\nI also support the following custom commands:\n"
    for cmd in commands:
        msg += "!" + cmd + "   "
    msg += "\n\nAnyone can add a command (!addcommand <cmdname> <output text>) but only admins can remove commands."
    return msg



# Runtime
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    msg = ''

    # Links
    if "[[" in message.content and "]]" in message.content:
        article = message.content[message.content.find("[[") + 2:message.content.find("]]")]
        msg += article + '\nhttp://finalfantasy.wikia.com/wiki/' + article.replace(' ', '_') + '\n\n'

    # Templates
    if "{{" in message.content and "}}" in message.content:
        article = message.content[message.content.find("{{") + 2:message.content.find("}}")]
        msg += article + '\nhttp://finalfantasy.wikia.com/wiki/Template:' + article.replace(' ', '_') + '\n\n'

    # Commands
    if message.content.startswith('!'):
        cmd_text = message.content.split('!')[1].split(' ')
        if cmd_text[0] in commands:
            cmd = commands[cmd_text.pop(0)]
            msg += cmd.func(cmd_text, message.author)
    
    if msg != '':
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)