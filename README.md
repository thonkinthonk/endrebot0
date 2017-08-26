# endrebot0
Discord selfbot

## Setup
1. Install dependencies: `sudo pip3 install -u https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py` (Linux) / `pip install -u https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py[voice]` (Windows)
1. Write `config.json`:  
```JSON
{
	"token": ":discord_token",
	"fragments": [":fragment_start", ":fragment_end"],
	"afk_messages": [
		{"dest": ":channel_or_user_id", "afk_message": ":afk_command", "unafk_message": ":unafk_command"},
		{"dest": "1234567890", "afk_message": "!afk {0}", "unafk_message": "unafk"}
	],
	"emoji": {
		"shrug": "¯\\\\\\_(ツ)\\_/¯",
		"zws": "\u200B"
	}
}
```
1. Run: `python3 run.py` (Linux) / `py run.py` (Windows)

## Fragments / What's the prefix?
endrebot0 is not your typical selfbot. Commands are designed to fit into normal messages, rather than requiring a message of their own.

Normal selfbot: `!servers` would reply with "I'm in X servers!", or a list of all servers you're in, in a specific format. It's impossible, or difficult, to get a different format.

endrebot0: `I'm in {{ len(ctx.bot.guilds) }} servers!` The bot will evaluate everything between the `{{` and `}}` as Python, and replace that block with the result of the evaluation. For example, `I'm in {{ len(ctx.bot.guilds) }} guilds: {{ ', '.join(map(str, ctx.bot.guilds)) }}` would print the quantity and names of your servers.

Because of this, endrebot0 is far more flexible than other selfbots at the expense of requiring a working knowledge of Python and discord.py (rewrite).

## Commands/How does the eval work?
endrebot0 doesn't simply call `eval()` with your code. That would prevent the user from utilizing discord.py at all, as every call is a coroutine which can't be used outside of coroutine functions. When you send a message and endrebot0 recognizes it contains a code fragment, it:  
1. Strips whitespace and backticks off of the fragment content. (You can use formatted code blocks inside fragments.)
1. Wraps the code in a coroutine function. If the code is one line and is not a statement, `return` is prepended to it (so you can actually get the value of the evaluation).
1. `exec()`s the wrapped code with the globals and locals of `CommandFragment.invoke`. This includes `ctx`, which is similar to the discord.py command framework's context, as well as all bot commands (which are really just Python functions). Executing the wrapped code puts the coroutine function in the locals, so it can be referenced outside of `exec`.
1. Calls the wrapped function, and awaits the result.
1. If the result is a coroutine function, calls it with no arguments and awaits the result. (This allows running simple commands like `zws()` without parentheses.)
1. If the result is a coroutine object, awaits it. (This allows calling coroutine functions like `ctx.send` or commands without explicitly `await`ing them.)
1. Converts the result to a string and returns that as the content to replace the code fragment with.

This process is complicated, but allows for much simpler use and much broader abilities. Besides allowing commands to be coroutines and allowing other discord.py coroutines to be used, it simplifies `{{ await zws() }}` to simply `{{zws}}`. (Commands look up the callstack to find the context, so passing it is not allowed or required. Thus commands like `zws()` take zero arguments.)

## AFK Configuration
endrebot0 supports going into and coming out of AFK in multiple locations, on multiple bots, with one command. The config's `afk_messages` key is a list of objects, with three keys:  
- `dest` is the channel id that the message will be sent to. It can also be a user ID to DM that user.
- `afk_message` is the message that will be sent when `afk` is called. The arguments passed into `afk()` are used to format this message (see the [`str.format`](https://docs.python.org/3.4/library/stdtypes.html#str.format) docs for more information).
- `unafk_message` is the message that will be sent when `unafk` is sent. The arguments passed into `unafk()` are used to format this message.

For example, with the above configuration, calling `afk('sleep')` would send the message `!afk sleep` to the user/channel with ID 1234567890. Calling `unafk()` will send `unafk` to the same place.

## Emoji
The `emoji` config is an object. The keys are names of your custom text emojis, and the values are the text that replaces them. With the example config, `:zws:` would be replaced with a zero-width space in any message. `: shrug :` would be replaced by the ASCII shrugging face. (Spaces are optional on all emoji, but required for this one to not conflict with the builtin shrug emoji.)

If the special key `_enclosure` is defined, its value is used instead of colons to mark what encloses a custom emoji. The enclosure can use regular expressions. For example, to allow semicolons in addition to colons, you would add `"_enclosure": [:;]` to your config. (Spacing is handled separately from the enclosure and always enabled.)
